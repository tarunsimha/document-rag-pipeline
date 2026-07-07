import streamlit as st
from chromadb_handler import search
from sentence_transformers import SentenceTransformer
import ollama

st.set_page_config(
    page_title="Document RAG pipeline",
    page_icon="🧠",
    layout="wide"
)

@st.cache_resource
def load_embedding_model():
    print("Loading embedding model...")
    return SentenceTransformer("all-MiniLM-L6-v2")


model = load_embedding_model()

st.title("Document RAG pipeline")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input(
    "Ask anything about your files..."
)

if user_prompt:
    with st.chat_message("user"):
        st.markdown(user_prompt)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    results = search(user_prompt, model, n_results=2)

    # Handle no results
    if (
        not results
        or not results["documents"]
        or not results["documents"][0]
    ):
        response_text = (
            "I could not find any relevant "
            "documents in the index."
        )

        with st.chat_message("assistant"):
            st.markdown(response_text)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response_text
            }
        )

        st.stop()

    sources = []

    for metadata in results["metadatas"][0]:
        sources.append(metadata["filename"])

    context = "\n\n".join(
        results["documents"][0]
    )

    prompt = f"""
Please give as much detail as possible, you can add your own answers but it should
be 100% true. Don't tell the user that you have recieved any context (like based on the context etc). Be confident in your answers.

Context:
{context}

Question:
{user_prompt}
""".strip()
    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        full_response = ""

        stream = ollama.chat(
            model="pkb-assistant:latest",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            stream=True
        )

        for chunk in stream:

            full_response += chunk["message"]["content"]

            response_placeholder.markdown(
                full_response + "▌"
            )

        response_placeholder.markdown(
            full_response
        )

        st.divider()

        st.subheader("📄 Sources")

        unique_sources = sorted(
            set(sources)
        )

        for source in unique_sources:
            st.write(f"📄 {source}")

    # Save assistant response to history
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response
        }
    )