# 🤖 YouTube Video Intelligence Agent (Local RAG)

An end-to-end **Retrieval-Augmented Generation (RAG)** system that allows users to chat with any YouTube video transcript in real-time. This project uses a completely local AI stack to ensure data privacy and zero API costs.

---

## 🚀 Features
* **Dynamic URL Ingestion:** Paste any YouTube link and the agent will fetch, clean, and index the transcript on the fly.
* **Semantic Search:** Uses vector embeddings to find the most relevant "evidence" from the video to answer your questions.
* **Local Inference:** Powered by **Ollama (Gemma-2B)** and **ChromaDB**—no data ever leaves your machine.
* **Evidence Tracking:** Displays the specific transcript snippets used by the AI to generate its response, ensuring transparency and reducing hallucinations.

---

## 🛠️ Technical Stack
* **Frontend:** [Streamlit](https://streamlit.io/) (Session state management & dynamic UI)
* **Orchestration:** Python
* **Embeddings:** [HuggingFace](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) (`all-MiniLM-L6-v2`)
* **Vector Database:** [ChromaDB](https://www.trychroma.com/)
* **LLM Engine:** [Ollama](https://ollama.com/) (Gemma-2B)
* **Data Source:** YouTube Transcript API

---

## 🏗️ System Architecture
1.  **Ingestion:** Extracts Video ID and fetches transcripts via `youtube-transcript-api`.
2.  **Processing:** Splits text into semantic chunks using `RecursiveCharacterTextSplitter`.
3.  **Indexing:** Converts chunks into vectors and stores them in a local persistent **ChromaDB** collection.
4.  **Retrieval:** Performs a similarity search for relevant context based on user queries.
5.  **Generation:** Passes the context and query to **Gemma-2B** for a grounded, accurate response.

---

## 💻 Installation & Setup

### 1. Prerequisites
* Python 3.10+
* [Ollama](https://ollama.com/) installed and running.

### 2. Clone the Repository
```bash
git clone [https://github.com/your-username/youtube-rag-explorer.git](https://github.com/your-username/youtube-rag-explorer.git)
cd youtube-rag-explorer 
```
### 3. Install Dependencies
```bash
pip install streamlit chromadb ollama youtube-transcript-api langchain-huggingface langchain-text-splitters
```
### 4. Pull the AI Model
```bash
ollama pull gemma:2b
```
### 5. Run the App
```bash
streamlit run app.py
```

## 📝 Usage
* Launch the app via Streamlit.

* Paste a YouTube URL in the sidebar.

* Click "Build Knowledge Base".

* Once indexed, ask any question in the chat box!

## Developed by Imaan Zahra

