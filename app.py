import streamlit as st
import chatbot
import database
import ingest

st.set_page_config(page_title="YouTube AI Explorer", layout="wide")

# --- SIDEBAR: The Input Zone ---
with st.sidebar:
    st.title("Video Url")
    # This is the box where the user enters the URL on the UI
    user_url = st.text_input("1. Paste YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")
    
    if st.button("2. Build Knowledge Base"):
        if user_url:
            with st.spinner("Processing video..."):
                # 1. Fetch transcript (from ingest.py)
                text = ingest.get_video_transcript(user_url)
                
                if text:
                    # 2. Slice into chunks
                    chunks = ingest.split_text(text)
                    
                    # 3. Create the fresh database
                    database.create_vector_db(chunks)
                    
                    # 4. Clear chat history for the new video
                    st.session_state.messages = []
                    
                    # --- THE IMPORTANT PART ---
                    st.success("Analysis Complete!")
                    st.rerun()  # This forces the app to restart and see the NEW database
                else:
                    st.error("Could not find a transcript.")
        else:
            st.warning("Please enter a URL first!")

# --- MAIN AREA: The Chat Zone ---
st.title("🤖 Chat with the Video")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Chat Input
if prompt := st.chat_input("Ask a question about the video:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # This calls chatbot.py which searches the fresh DB
        answer, snippets = chatbot.ask_ai(prompt)
        st.markdown(answer)
        
        with st.expander("View Evidence Snippets"):
            for i, snip in enumerate(snippets):
                st.info(f"Snippet {i+1}: {snip}")
    
    st.session_state.messages.append({"role": "assistant", "content": answer})