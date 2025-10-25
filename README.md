🧠 GitHub Repository Chatbot

A conversational GitHub repository assistant built using LangChain, OpenAI, and Chainlit.
Simply paste a public GitHub repo link, and the chatbot will fetch all readable files, build embeddings, and let you ask questions about the repository’s code, documentation, or structure — just like ChatGPT for GitHub!

🚀 Features

🔗 Accepts any public GitHub repository link

📂 Automatically fetches all .py, .js, .html, .css, .md, and .txt files

🧩 Splits and processes repository content using LangChain Text Splitters

🧮 Embeds file chunks using text-embedding-3-small

🧠 Stores embeddings in a local FAISS vectorstore

💬 Answers user queries contextually using OpenAI GPT models

⚡ Streams responses live via Chainlit chat interface

🔁 Simple, modular, and extensible pipeline — perfect for experimenting with RAG

🧰 Tech Stack
Component	Library
Framework	Chainlit

LLM	OpenAI GPT (via LangChain)

Embeddings	text-embedding-3-small
Vector Store	FAISS

Repo Fetching	requests (GitHub REST API)
Environment	.env for API keys
⚙️ Installation & Setup
1️⃣ Clone the repository
```
git clone https://github.com/your-username/github-chatbot.git
```
```
cd github-chatbot
```

2️⃣ Create a virtual environment
```
python -m venv .venv
```
```
.\.venv\Scripts\activate
```

3️⃣ Install dependencies

🧩 Option 1 — Using pip
```
pip install -r requirements.txt
```

⚡ Option 2 — Using uv (recommended)
```
uv pip install -r requirements.txt
```
4️⃣ Set up environment variables

Create a .env file in your project root directory and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```
5️⃣ Run the chatbot

🧠 Using uv (recommended)
```
uv run chainlit run app.py
```

🐍 Or using Python directly
```
chainlit run app.py
```

Once the server starts, open the provided local URL in your browser —
your GitHub Repository Chatbot will be live! 🎉

🧠 How It Works

You provide a GitHub repo link.

The app fetches all code and text files via the GitHub API.

LangChain splits each file into smaller, meaningful chunks.

Each chunk is embedded using OpenAI embeddings and stored in FAISS.

When you ask a question, the app retrieves the most relevant chunks.

OpenAI GPT generates a context-aware answer in real-time.

📜 License

This project is licensed under the MIT License —
you’re free to use, modify, and distribute it with attribution.
