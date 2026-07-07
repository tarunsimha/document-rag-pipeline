import ollama
import subprocess
from pathlib import Path

client = ollama.Client()

def ensure_qwen():
    installed = [m.model for m in client.list().models]

    if any("qwen3:4b" in model for model in installed):
        print("qwen3:4b already installed")
        return

    print("Downloading qwen3:4b...")
    client.pull("qwen3:4b")
    print("Done")

# Ensure Personal Knowledge Base model
def ensure_pkb_model():
    installed = [m.model for m in client.list().models]

    if any("pkb-assistant" in model for model in installed):
        print("pkb-assistant already exists")
        return

    print("Creating pkb-assistant...")

    subprocess.run(
        [
            "ollama",
            "create",
            "pkb-assistant",
            "-f",
            str(Path("ModelFile"))
        ],
        check=True
    )

    print("Done")


ensure_qwen()
ensure_pkb_model()