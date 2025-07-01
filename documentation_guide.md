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
> ??? tip "this python code"

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
          key: ${{ github.ref }}
          path: .cache

      - run: pip install -r requirements.txt
      - run: python clone_directories_to_docs.py
      - run: mkdocs gh-deploy --force
