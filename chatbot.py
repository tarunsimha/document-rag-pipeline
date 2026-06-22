import ollama
from chromadb_handler import search
from sentence_transformers import SentenceTransformer

print("Initializing models..")
model = SentenceTransformer("all-MiniLM-L6-v2")

user_prompt = input("Enter the prompt: ")

results = search(user_prompt, model, n_results=2)

prompt = []
prompt.append(f"User prompt: {user_prompt}\nResults obtained from RAG pipeline:\n")

for i, doc in enumerate(results["documents"][0]):
    prompt.append(f"\nResult {i + 1}")
    prompt.append("-" * 50)

    prompt.append("File:")
    prompt.append(results["metadatas"][0][i]["filename"])

    prompt.append(doc)

prompt = '\n'.join(prompt)

stream = ollama.chat(
    model="pkb-assistant:latest",
    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ],
    stream=True
)

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)