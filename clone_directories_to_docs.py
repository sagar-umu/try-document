import os
import shutil

REPO_ROOT = "."
DOCS_DIR = "docs"
INCLUDE_DIRS = {"nextflow", "pipeline", "src", "templates", "testDIR"}

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

 
    for entry in INCLUDE_DIRS:
        src_path = os.path.join(REPO_ROOT, entry)
          # Rename 'templates' → 'Templates' only
        dst_folder_name = "WTF" if entry == "templates" else entry
        dst_path = os.path.join(DOCS_DIR, entry)

        if os.path.isdir(src_path):
            print(f"Cloning folder: {entry} -> {dst_path}")
            safe_copytree(src_path, dst_path)
        else:
            print(f"Skipped missing folder: {entry}")

if __name__ == "__main__":
    clone_repo_dirs()
    