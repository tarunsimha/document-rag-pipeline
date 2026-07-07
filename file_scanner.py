import os
import db_handler

MAX_FILE_SIZE = 30 * 1024 * 1024 # 30 MB

# Iterative DFS for file indexing - To avoid recursion limits
stack = [os.path.expanduser("~")]
text_types = {"pdf", "docx", "pptx", "xlsx", "txt", "md", "py", "cpp", "c", "rs", "html", "css", "js"}
metadata_types = {"zip", "7z", "jpg", "png", "mp4", "mkv", "exe"}
ignore_directories = {"node_modules", "__pycache__", "snapd", "venv", "appdata", "programdata", "nltk_data"}

directories_visited = 0
files_scanned = 0
files_indexed = 0

db_handler.create_table()

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
                        size = os.path.getsize(full_path)
                        if size > MAX_FILE_SIZE:
                            continue
                        else:
                            file_attrs["size"] = size
                        file_attrs["modified"] = os.path.getmtime(full_path) # Seconds since epoch
                    except OSError:
                        file_attrs["size"] = None
                        file_attrs["modified"] = None

                    if extension in text_types:
                        file_attrs["file_type"] = "text"
                    else:
                        file_attrs["file_type"] = "metadata"

                    db_handler.add_to_db(file_attrs)
                    files_indexed += 1

    except PermissionError:
        continue

db_handler.commit_changes()

for row in db_handler.debug_data():
    print(row[0], row[1])

print("\nDirectories visited:", directories_visited)
print("Files scanned:", files_scanned)
print("Files indexed:", files_indexed)

db_handler.close_db()