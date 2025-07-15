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

### Set-up

1. On your local machine clone your GitHub repository of interest using the Clone Git Repository option.

2. Create a `/docs` directory in your repository.

    !!! info
        Both Read the Docs and MkDocs use `/docs` as their source directory by default.

3. If you want to use an existing `README.md` file as the landing page for your documentation, move it to `/docs`, otherwise create an `index.md` file in `/docs`.

    !!! info
        MkDocs can use both `README.md` and `index.md` to render the HTML.  
        However, if both files are present in a directory, it will use `index.md` as the default.

4. Create a `requirements.txt` file in the root directory and copy this code into it:

    ```txt
    mkdocs>=1.5
    mkdocs-material
    mkdocs-awesome-pages-plugin
    mkdocs-git-revision-date-localized-plugin
    mike
    mkdocs-macros-plugin
    ```

5.  If you want directories (and their contents) from your repository to be visible on the webpage, they will need:  
        - to be in the `docs` directory  
        - an `index.md` file of their own
    You can either copy the directories/files of interest to the `/docs` directory or

    !!! tip
        You can automate the cloning of directories using the following script:

        <details>
        <summary><i>Show Python code</i></summary>

        ```python
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

        def remove_excluded_dirs_from_docs():
            if not os.path.exists(DOCS_DIR):
                return

            existing_docs_dirs = os.listdir(DOCS_DIR)
            for excluded in EXCLUDE_DIRS:
                excluded_name = os.path.basename(excluded)
                full_path = os.path.join(DOCS_DIR, excluded_name)
                if excluded_name in existing_docs_dirs and os.path.isdir(full_path):
                    print(f"Removing excluded dir from docs: {full_path}")
                    shutil.rmtree(full_path)

        def clone_repo_dirs():
            os.makedirs(DOCS_DIR, exist_ok=True)
            remove_excluded_dirs_from_docs()

            for entry in os.listdir(REPO_ROOT):
                src_path = os.path.join(REPO_ROOT, entry)
                if entry in EXCLUDE_DIRS or entry in EXCLUDE_FILES or entry.startswith("."):
                    continue

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

6. Create a `mkdocs.yml` file in the root and add the following content:

    <details>
    <summary><i>Show mkdocs.yml</i></summary>

    ```yaml
    site_name: UPSCb Common Documentation
    site_url: https://your-username.github.io/Documentation_example/

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

    markdown_extensions:
      - admonition
      - pymdownx.details
      - pymdownx.superfences
    ```
    </details>

7. Set up **GitHub Pages** deployment:
    - In your root directory, create: `/.github/workflows/`
    - Inside that, create a file `ci.yml` with the following contents:

    <details>
    <summary><i>Show ci.yml</i></summary>

    ```yaml
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
    </details>

8. Configuration file for **ReadtheDocs**
    If you want to host the documentation on ReadtheDocs you will also need a `.readthedocs.yml` file. You can create this file and copy the code below to it. 

    <details>
    <summary><i>Show .readthedocs.yml</i></summary>

    ```yml
        version: 2

        build:
          os: ubuntu-22.04
          tools:
           python: "3.10"

        python:
          install:
            - requirements: requirements.txt
        
        mkdocs:
          configuration: mkdocs.yml
    ```
    </details>

9. You are now ready to build your webpage.

### Building and deploying webpage

1. **Using mkdocs to deploy locally for testing.** This is a great way of visaulizing how your webpage will look once rendered. Follow these steps:  
    - Navigate to the repository directory on your local machine
    - Create a virtual python environment by `python -m venve venv`
    - Activate the environemnt: `source venv/bin/activate`
    - Install required plug-ins from the requiremnts.txt file: `pip install -r requirements.txt`
    - OPTIONAL: If you are copying the directories into the `/docs` dir. using the python script you can do that now by running the script. 
    - Build and serve your webpage: `python -m mkdocs serve`
    - Your webpage should be available on localhost `http://127.0.0.1:8000/....`

2. **Hosting on GHPages.** Hosting on GHPages involves taking the following steps:
    - Make sure that you have committed and pushed the additional changes and iles to your GH repository (repo).
    - Once your repo is up-to-date navigate to your repo and navigate to *Settings > Pages* and select `Deploy from a branch` under the **Build and Deployment** menu. 
    - Under *Branch* select `gh-pages` and `/root` from the drop-down menus and click save
    - Once you have done these steps, a link to your webpage should appear on top of the same page. You can visit your site from there.

3. ***Using Read the Docs**
    - Follow the tutorial [here](https://docs.readthedocs.com/platform/stable/tutorial/index.html)
    - You already have all the files you need, so the webpage should build automatically.

