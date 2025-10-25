import os
import chainlit as cl
import requests
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

def get_repo_content(repo_url: str):
    """Fetch all readable text files from a public GitHub repository."""
    try:
        if repo_url.endswith("/"):
            repo_url = repo_url[:-1]
        repo_api = repo_url.replace("github.com", "api.github.com/repos") + "/contents"
        return fetch_files(repo_api)
    except Exception as e:
        print(f"Error fetching repo: {e}")
        return []


def fetch_files(api_url: str):
    """Recursively fetch all file contents from the GitHub API."""
    files_text = []
    response = requests.get(api_url)
    if response.status_code != 200:
        print(f"Failed to fetch: {api_url}")
        return files_text

    for item in response.json():
        if item["type"] == "file":
            if any(item["name"].endswith(ext) for ext in [".py", ".js", ".html", ".css", ".md", ".txt"]):
                file_resp = requests.get(item["download_url"])
                if file_resp.status_code == 200:
                    files_text.append({"path": item["path"], "content": file_resp.text})
        elif item["type"] == "dir":
            files_text.extend(fetch_files(item["url"]))
    return files_text


def build_vectorstore(repo_files):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    texts = [f"File: {f['path']}\n\n{f['content']}" for f in repo_files]
    docs = splitter.create_documents(texts)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4})


def create_chain(retriever):
    llm = ChatOpenAI(model="gpt-4o-mini", streaming=True, temperature=0.3)

    prompt = PromptTemplate(
        template="""
        You are a software assistant that helps users understand GitHub repositories.

        Use ONLY the following context (code, docs, and comments) to answer.
        If the context does not contain enough info, reply with:
        "I don't have enough information from the repository to answer that.
        Only provide the code snippets that are in the context. Do not make up new code.
        In case of any errors the user ive you while using the code from the context, help them debug using only the context."

        Context:
        {context}

        Question:
        {question}
        """,
        input_variables=["context", "question"]
    )

    def format_docs(retrieved_docs):
        return "\n\n".join(doc.page_content for doc in retrieved_docs)

    parallel_chain = RunnableParallel({
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough()
    })

    parser = StrOutputParser()
    return parallel_chain | prompt | llm | parser



@cl.on_chat_start
async def start():
    await cl.Message(content=" Send me a GitHub repo link to start analyzing it!").send()


@cl.on_message
async def handle_message(message: cl.Message):
    content = message.content.strip()

    # --- User asking a question ---
    if not content.startswith("http"):
        chain = cl.user_session.get("chain")
        if not chain:
            await cl.Message(content=" Send a GitHub repository link first.").send()
            return

        msg = cl.Message(content="💭 Thinking...")
        await msg.send()

        # Stream the output live
        async for chunk in chain.astream(content):
            if chunk:
                msg.content += chunk
                await msg.update()

        await msg.update()  # finalize
        return

    # --- User sent a repo link ---
    await cl.Message(content="Fetching repository files...").send()

    repo_files = get_repo_content(content)
    if not repo_files:
        await cl.Message(content="Could not fetch repository or it's empty.").send()
        return

    retriever = build_vectorstore(repo_files)
    chain = create_chain(retriever)

    cl.user_session.set("chain", chain)
    await cl.Message(content=f"Repository loaded with {len(repo_files)} files! Ask me anything about it.").send()
