import streamlit as st
import os
import openai

# Load the document
def load_document(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return file.read()
    else:
        return None

# Split the document into manageable chunks
def chunk_text(text, max_length=500):
    words = text.split()
    return [' '.join(words[i:i + max_length]) for i in range(0, len(words), max_length)]

# Get answer from OpenAI API
def get_openai_response(question, context):
    try:
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" for better performance if available
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context."},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit app layout
st.title("Thena Docs Chatbot (Powered by ChatGPT)")
st.write("Ask questions about the `thena_docs.md` document!")

# Load the document
document_path = "thena_docs.md"
document_text = load_document(document_path)

if not document_text:
    st.error("Document not found. Please ensure the `thena_docs.md` file is in the same directory as this app.")
else:
    # Preprocess the document into chunks
    chunks = chunk_text(document_text)

    # User input
    user_question = st.text_input("Enter your question:")

    if user_question:
        # Find the most relevant chunk (basic implementation)
        relevant_chunk = max(chunks, key=lambda x: user_question in x)
        
        # Get the answer from OpenAI
        st.write("Generating answer...")
        answer = get_openai_response(user_question, relevant_chunk)
        st.write(f"**Answer:** {answer}")

    # Optional: Display the document content
    if st.checkbox("Show document content"):
        st.text_area("Document Content", document_text, height=400)


    # Optional: Display the document content
    if st.checkbox("Show document content"):
        st.text_area("Document Content", document_text, height=400)
