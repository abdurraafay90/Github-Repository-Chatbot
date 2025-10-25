🧠 GitHub Repository Chatbot (with LangChain + Chainlit)

This project lets you chat with any public GitHub repository.
Just send a GitHub repo link, and the chatbot will fetch the files, create embeddings using FAISS, and let you ask natural-language questions about the code or documentation.

It uses LangChain, OpenAI embeddings, and Chainlit for an interactive, streamed chat experience.

🚀 Features

📦 Analyze any public GitHub repository

🧩 Understand code, docs, and comments

⚡ Real-time streaming answers (word-by-word)

🔎 Uses FAISS vector search for retrieval

💬 Runs locally via Chainlit web UI

🪶 Built using LangChain’s Runnable architecture

🛠️ Tech Stack
Component	Description
Python 3.10+	Programming language
Chainlit	Frontend chat UI
LangChain	For RAG and pipeline composition
FAISS	Vector similarity search
OpenAI	Embeddings + Chat model (GPT-4o-mini used)
Requests	To fetch GitHub repo contents
⚙️ Installation

Clone this repository

git clone https://github.com/yourusername/github-repo-chatbot.git
cd github-repo-chatbot


Create and activate a virtual environment

uv venv
uv pip install -r requirements.txt


Set up your .env file
Create a file named .env in the root directory and add your OpenAI key:

OPENAI_API_KEY=your_openai_api_key


Run the chatbot

uv run chainlit run app.py


Open your browser and go to:
👉 http://localhost:8000

🧩 Example Usage

Start the app.

Paste a GitHub repo link, e.g.

https://github.com/psf/requests


After it loads, ask questions like:

“What does this project do?”

“How is authentication handled?”

“Which file contains the main entry point?”

🧠 How It Works

Fetches repo contents using GitHub API

Splits code and docs into chunks using RecursiveCharacterTextSplitter

Generates embeddings with text-embedding-3-small

Stores embeddings in FAISS for fast retrieval

Uses GPT-4o-mini for question answering

Streams responses in real-time via Chainlit

📂 Project Structure
📦 github-repo-chatbot
├── app.py                 # Main chatbot logic
├── requirements.txt       # Dependencies
├── .env                   # OpenAI key (not committed)
└── README.md              # Documentation
