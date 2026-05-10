import chromadb
import requests
import json
from langchain_huggingface import HuggingFaceEmbeddings # Updated this for you!

def ask_ai(question):
    # 1. Setup
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    client = chromadb.PersistentClient(path="./my_db")
    client = chromadb.PersistentClient(path="./my_db")
    
    # Check if the collection exists first
    try:
        collection = client.get_collection(name="youtube_video")
    except:
        return "Please build the knowledge base in the sidebar first!", []

    # ... rest of your retrieval code ...
    
    # 2. RETRIEVAL
    results = collection.query(query_texts=[question], n_results=3)
    
    # --- IMPORTANT: DEFINE SNIPPETS HERE ---
    snippets = results['documents'][0] if results['documents'] else []
    context = " ".join(snippets)
    
    # 3. PROMPT (The "Inference" Version)
    # We remove the "Say I don't know" part to encourage the AI to speak
    prompt = f"""
    <start_of_turn>user
    You are a helpful AI assistant. Use the following snippets from a video transcript to answer the question in a friendly way.
    
    VIDEO SNIPPETS:
    {context}
    
    USER QUESTION: 
    {question}
    
    Please provide a helpful answer based on the snippets above. If the information is even partially there, try to summarize it.
    <end_of_turn>
    <start_of_turn>model
    """
    
    # 4. GENERATION
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "gemma:2b",
        "prompt": prompt,
        "stream": False
    }
    
    try:
        # Increase timeout just in case it's slow
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status() 
        answer = json.loads(response.text)['response']
        
        # Return both now that we are sure snippets exists
        return answer, snippets
        
    except Exception as e:
        # Return the error and the snippets (even if empty)
        return f"AI Error: {e}", snippets

if __name__ == "__main__":
    query = input("Ask a question about the video: ")
    print(f"\nAI Response:\n{ask_ai(query)}")