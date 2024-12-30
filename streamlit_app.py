import streamlit as st
from transformers import pipeline
import os

# Load the document
def load_document(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return file.read()
    else:
        return "Document not found. Please ensure the file is in the same directory as the app."

# Split the document into manageable chunks
def chunk_text(text, max_length=500):
    words = text.split()
    return [' '.join(words[i:i + max_length]) for i in range(0, len(words), max_length)]

# Initialize the QA pipeline
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# Streamlit app layout
st.title("Thena Docs Chatbot")
st.write("Ask questions about the `thena_docs.md` document!")

# Load the document
document_path = "thena_docs.md"
document_text = load_document(document_path)

if document_text == "Document not found. Please ensure the file is in the same directory as the app.":
    st.error(document_text)
else:
    # Preprocess the document into chunks
    chunks = chunk_text(document_text)

    # User input
    user_question = st.text_input("Enter your question:")

    if user_question:
        # Find the most relevant chunk (basic implementation)
        relevant_chunk = max(chunks, key=lambda x: user_question in x)
        
        # Get the answer using the QA pipeline
        response = qa_pipeline({'question': user_question, 'context': relevant_chunk})
        st.write(f"**Answer:** {response['answer']}")

    # Optional: Display the document content
    if st.checkbox("Show document content"):
        st.write(document_text)

