import os
import shutil

REPO_ROOT = "."
DOCS_DIR = "docs"

EXCLUDE = {
    DOCS_DIR, ".git", ".github", "__pycache__", "site", "venv", ".venv", "mkdocs.yml",
    "clone_directories_to_docs.py", "requirements.txt"
}

def clone_repo_dirs():
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)

    for entry in os.listdir(REPO_ROOT):
        src = os.path.join(REPO_ROOT, entry)
        dst = os.path.join(DOCS_DIR, entry)

        if os.path.isdir(src) and entry not in EXCLUDE:
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"Copied folder: {entry}")
        elif os.path.isfile(src) and entry.endswith(".md") and entry not in EXCLUDE:
            shutil.copy(src, os.path.join(DOCS_DIR, entry))
            print(f"Copied file: {entry}")

if __name__ == "__main__":
    clone_repo_dirs()
