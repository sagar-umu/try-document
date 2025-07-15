# Building Documentation

This guide defines steps for hosting your GitHub repository using Read the Docs or GitHub Pages. We will use MkDocs material theme for visual upgrades. MkDocs uses markdown (.md) files as input. 

## Resources

   1. [Read the Docs](https://docs.readthedocs.com/platform/stable/)
   2. [MkDocs](https://www.mkdocs.org/)
   3. [GitHub Pages](https://pages.github.com/)
---

## Prerequisites

   1. Python
   2. An integrated development environment like [VSCode](https://code.visualstudio.com/)

## Steps 

1. Clone your GitHub repository of interest using the [Clone Git Repository...](<Screenshot 2025-06-27 at 10.25.21-1.png>) option. 
2. Create a `/docs` directory in your repository. 
    >Both Read the Docs and MkDocs use `/docs` as their source directory by default.
3. If you want to use an existing `README.md` file as the landing page for your documentation, move it to `/docs`, otherwise create an `index.md` file in `/docs`. 
    >MkDocs can use both `README.md` and `index.md` to render the html, however, if both files are present in a `/dir`, it will use the `index.md` file.
4. Create a `requirements.txt` file in the root directory and copy this code to it
    ```txt
        mkdocs>=1.5
        mkdocs-material
        mkdocs-awesome-pages-plugin
        mkdocs-git-revision-date-localized-plugin
        mike
        mkdocs-macros-plugin

> [!NOTE]
> If you want directories (and their contents) from your repository to be visible on the webpage, they will need 
>   1. to be in the `docs` directory
>   2. an `index.md` file of their own

> [!TIP]
> You can automate the cloning of directories from root to `/docs` by using 
> <details><summary> <i> this python code </i> </summary> 

```python
import os
import shutil

REPO_ROOT = "."
DOCS_DIR = "docs"

# Folders in the repo root to exclude from cloning
EXCLUDE_DIRS = {
    DOCS_DIR, ".git", ".github", "site", "venv", ".venv", "__pycache__", ".mypy_cache" 
    }

# Files to exclude from cloning
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

def remove_excluded_dirs_from_docs():
    if not os.path.exists(DOCS_DIR):
        return

    existing_docs_dirs = os.listdir(DOCS_DIR)

    for excluded in EXCLUDE_DIRS:
        excluded_name = os.path.basename(excluded)
        if excluded_name in existing_docs_dirs:
            full_path = os.path.join(DOCS_DIR, excluded_name)
            if os.path.isdir(full_path):
                print(f"Removing excluded dir from docs: {full_path}")
                shutil.rmtree(full_path)

def clone_repo_dirs():
    os.makedirs(DOCS_DIR, exist_ok=True)

    # First clean up excluded dirs if already in docs/
    remove_excluded_dirs_from_docs()

    for entry in os.listdir(REPO_ROOT):
        src_path = os.path.join(REPO_ROOT, entry)

        if entry in EXCLUDE_DIRS or entry in EXCLUDE_FILES or entry.startswith("."):
            continue

        # Optional renaming logic
        dst_name = "Templates" if entry == "templates" else entry
        dst_path = os.path.join(DOCS_DIR, dst_name)

        if os.path.isdir(src_path):
            print(f"Cloning folder: {entry} → {dst_name}/")
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
```
</details>

 5. Create a `mkdocs.yml` file and copy this code to it
```yml
site_name: NAME OF YOUR WEBPAGE
site_url: https://your-url.github.io/your-document/
docs_dir: docs
site_dir: site

theme:
name: material
language: en
palette:
- scheme: default
toggle:
icon: material/toggle-switch-off-outline
name: Switch to dark mode
primary: light blue
accent: purple
- scheme: slate
toggle:
icon: material/toggle-switch
name: Switch to light mode
primary: indigo
accent: deep purple
features:
- navigation.tabs
- navigation.tabs.sticky
- navigation.sections
- toc.follow
- search.suggest
- search.highlight
- content.tabs.link
- content.code.annotation
- content.code.copy
extra:
version:
provider: mike

plugins:
- search
- awesome-pages
- git-revision-date-localized:
type: date
- mike
- macros
```
 6.  Setup for **GitHub Pages**:
- In your root directory create `/.github/workflows/`
- In the workflows directory create a file `ci.yml` and paste the following code to it 
```yml
name: ci

on:
  push:
    branches: 
      - main
      - master
permissions:
  contents: write
jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - uses: actions/cache@v3
        with:
          key: {% raw %}${{ github.ref }}{% endraw %}
          path: .cache

      - run: pip install -r requirements.txt
      - run: python clone_directories_to_docs.py
      - run: mkdocs gh-deploy --force
```
 7. 