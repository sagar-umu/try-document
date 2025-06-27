# Hosting documentation using Read the Docs or Github-pages

This guide defines steps for hosting your GitHub repository using Read the Docs and or GitHub Pages. We will use MkDocs material theme for visual upgrades. MkDocs uses markdown (.md) files as input. 
---

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
    >Both Read the Docs and MkDocs use a `/docs` as their source directory by default.
3. If you want to use an existing `README.md` file as the landing page for your documentation, move it to `/docs`, otherwise create an `index.md` file in `/docs`. 
    >MkDocs can use both `README.md` and `index.md` to render the html, however, if both files are present in a `/dir`, it will use the `index.md` file.
4. Create a `requirements.txt` file in the root directory and copy this code to it
    ```mkdocs>=1.5
        mkdocs-material
        mkdocs-awesome-pages-plugin
        mkdocs-git-revision-date-localized-plugin
        mike
        mkdocs-macros-plugin

> [!NOTE]
> If you want directories (and their contents) from your repository to be visible on the webpage, they will need 
>   1. to be in the `docs` directory
>   2. an `index.md` file of their own

5. 