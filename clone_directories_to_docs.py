import os
import shutil

REPO_ROOT = "."
DOCS_DIR = "docs"

EXCLUDE_DIRS = {
    DOCS_DIR, ".git", ".github", "site", "venv", ".venv", "__pycache__", ".mypy_cache"
}
EXCLUDE_FILES = {
    "mkdocs.yml", "requirements.txt", "readthedocs.yml", "clone_directories_to_docs.py"
}

def should_copy(src, dst):
    return not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst)

def safe_copytree(src, dst):
    for root, dirs, files in os.walk(src):
        rel_path = os.path.relpath(root, src)
        dst_root = os.path.join(dst, rel_path) if rel_path != '.' else dst

        os.makedirs(dst_root, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dst_root, file)

            if file.endswith(".md"):
                if should_copy(src_file, dst_file):
                    shutil.copy2(src_file, dst_file)
                    print(f"Updated .md file: {dst_file}")
                else:
                    print(f"Skipped unchanged .md: {dst_file}")
            else:
                shutil.copy2(src_file, dst_file)
                print(f"Copied file: {dst_file}")

def clone_repo_dirs():
    os.makedirs(DOCS_DIR, exist_ok=True)

    for entry in os.listdir(REPO_ROOT):
        src_path = os.path.join(REPO_ROOT, entry)

        # Handle only folders and .md files at top level
        if entry in EXCLUDE_DIRS or entry in EXCLUDE_FILES or entry.startswith("."):
            continue

        # Rename 'templates' → 'Templates' only
        dst_folder_name = "Templates" if entry == "templates" else entry
        dst_path = os.path.join(DOCS_DIR, dst_folder_name)

        if os.path.isdir(src_path):
            print(f"Cloning folder: {entry} -> {dst_folder_name}/")
            safe_copytree(src_path, dst_path)
        elif os.path.isfile(src_path) and entry.endswith(".md"):
            dst_file = os.path.join(DOCS_DIR, entry)
            if should_copy(src_path, dst_file):
                shutil.copy2(src_path, dst_file)
                print(f"Copied root .md file: {entry}")
            else:
                print(f"Skipped unchanged root .md: {entry}")

if __name__ == "__main__":
    clone_repo_dirs()
