import streamlit as st
import requests
import os

# Change this if your backend is hosted elsewhere
BACKEND_URL = "https://rag-chatbot-backend-j9qx.onrender.com" #"http://127.0.0.1:8000"
DOCS_FOLDER = "documents"  # if needed for display or info

def upload_document():
    st.sidebar.header("Upload Document")
    uploaded_file = st.sidebar.file_uploader("Select a text file", type=["txt"])
    if uploaded_file is not None:
        if st.sidebar.button("Upload File"):
            # Create files payload for the API
            files = {
                "file": (uploaded_file.name, uploaded_file, "text/plain")
            }
            try:
                response = requests.post(f"{BACKEND_URL}/upload", files=files)
                if response.status_code == 200:
                    st.sidebar.success(response.json()["message"])
                else:
                    st.sidebar.error(f"Error: {response.json().get('detail')}")
            except Exception as e:
                st.sidebar.error(f"Upload failed: {e}")

def delete_document():
    st.sidebar.header("Delete Document")
    filename_to_delete = st.sidebar.text_input("Filename to delete (e.g., example.txt)")
    if st.sidebar.button("Delete File"):
        if filename_to_delete:
            try:
                response = requests.delete(f"{BACKEND_URL}/delete/{filename_to_delete}")
                if response.status_code == 200:
                    st.sidebar.success(response.json()["message"])
                else:
                    st.sidebar.error(f"Error: {response.json().get('detail')}")
            except Exception as e:
                st.sidebar.error(f"Deletion failed: {e}")
        else:
            st.sidebar.warning("Please enter a filename.")

def chat_interface():
    st.header("Chat with Your Documents")
    query = st.text_input("Ask your question:")
    if st.button("Send Query"):
        if query.strip():
            try:
                payload = {"query": query}
                response = requests.post(f"{BACKEND_URL}/chat", json=payload)
                if response.status_code == 200:
                    answer = response.json().get("answer", "No answer returned.")
                    st.write("**Answer:**", answer)
                else:
                    st.error(f"Error: {response.json().get('detail')}")
            except Exception as e:
                st.error(f"Chat request failed: {e}")
        else:
            st.warning("Please enter a query.")

def main():
    st.title("RAG Chatbot Frontend")
    st.write("Use this interface to upload documents, delete them, and chat with your document-based system.")
    
    # Sidebar functions for document management
    upload_document()
    delete_document()
    
    # Main chat interface
    chat_interface()

if __name__ == "__main__":
    main()
