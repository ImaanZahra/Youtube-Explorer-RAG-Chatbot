import chromadb
from langchain_huggingface import HuggingFaceEmbeddings

def create_vector_db(chunks):
    print("--- Step 3: Creating Vector Database ---")
    
    # 1. Initialize the Embedding Model
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    
    # 2. Create the ChromaDB client
    client = chromadb.PersistentClient(path="./my_db")
    collection_name = "youtube_video"
    
    # 3. FRESH START: Delete and recreate the collection
    try:
        # Check if it exists before deleting
        existing = [c.name for c in client.list_collections()]
        if collection_name in existing:
            client.delete_collection(name=collection_name)
            print(f"🗑️ Old video data wiped from memory.")
    except Exception as e:
        print(f"Note: Cleanup skipped ({e})")
    
    # Create the fresh collection
    collection = client.create_collection(name=collection_name)
    
    # 4. BULK ADD: This is faster and more reliable than a for-loop
    print(f"📥 Indexing {len(chunks)} new chunks...")
    
    # Create a list of IDs: ["id_0", "id_1", "id_2"...]
    ids = [f"id_{i}" for i in range(len(chunks))]
    
    # Add everything in one single command
    collection.add(
        ids=ids,
        documents=chunks
    )
    
    print("✅ Database updated with the NEW video!")
    return collection

# You can keep the 'if __name__ == "__main__"' part or delete it. 
# It won't affect the Streamlit UI.