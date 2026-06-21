import os

# Iterative DFS for file indexing - To avoid recursion limits
stack = [os.path.expanduser("~")]
text_types = {"pdf", "docx", "pptx", "xlsx", "txt", "md", "py", "cpp", "c", "rs", "html", "css", "js"}
metadata_types = {"zip", "7z", "jpg", "png", "mp4", "mkv", "exe"}
ignore_directories = {"node_modules", "__pycache__", "snapd", "venv", "AppData", "ProgramData"}

directories_visited = 0
files_scanned = 0
files_indexed = 0

files = []

while stack:
    current = stack.pop()

    try:
        for item in os.listdir(current):
            full_path = os.path.join(current, item)

            if os.path.islink(full_path):
                continue

            if os.path.isdir(full_path):
                if not item.startswith(".") and item.lower() not in ignore_directories:
                    directories_visited += 1
                    stack.append(full_path)
            else:
                files_scanned += 1
                extension = item.split(".")
                if len(extension) == 1:
                    extension = None
                else:
                    extension = extension[-1].lower()

                if extension in text_types or extension in metadata_types:
                    file_attrs = {}
                    file_attrs["path"] = full_path
                    file_attrs["filename"] = item
                    file_attrs["extension"] = extension
                    try:
                        file_attrs["size"] = os.path.getsize(full_path)
                        file_attrs["modified"] = os.path.getmtime(full_path) # Seconds since epoch
                    except OSError:
                        file_attrs["size"] = None
                        file_attrs["modified"] = None
                    files.append(file_attrs)
                    files_indexed += 1

    except PermissionError:
        continue

for file in files:
    print(file["filename"])

print("\nDirectories visited:", directories_visited)
print("Files scanned:", files_scanned)
print("Files indexed:", files_indexed)