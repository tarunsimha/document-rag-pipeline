import argparse

parser = argparse.ArgumentParser(
    prog="Document RAG Pipeline",
    description="A simple document RAG pipeline with document indexing, semantic search, and metadata extraction for non-text files.",
)

parser.add_argument("operation")
parser.add_argument("-p", "--path")
parser.add_argument("-t", "--text")
parser.add_argument("-n", "--n_results")

args = parser.parse_args()
operation = args.operation
path = args.path
text = args.text
n_results = args.n_results

if operation == "scan":
    from file_scanner import scan_all_files
    if path is None:
        scan_all_files()
    else:
        scan_all_files(path)
elif operation == "remove_data":
    import db_handler
    try:
        db_handler.delete_table()
    except:
        print("Could not delete the table, you can manually delete the database.")
elif operation == "remove_embeds":
    import os
    try:
        os.rmdir("chroma_db")
        print("Successfuly removed the embeddings")
    except OSError as e:
        print(e)
elif operation == "embed":
    import embedder
    embedder.embed_data()
elif operation == "search":
    from chromadb_handler import search
    from sentence_transformers import SentenceTransformer

    import warnings
    warnings.filterwarnings("ignore")

    model = SentenceTransformer("all-MiniLM-L6-v2", model_kwargs={"ignore_mismatched_sizes": True, "low_cpu_mem_usage": True})
    if n_results is None:
        results = search(text, model)
    else:
        results = search(text, model, n_results=n_results)

    print("\n\n".join(results["documents"][0]))
else:
    parser.print_help()
