"""Generate the code reference pages and navigation.

From https://mkdocstrings.github.io/recipes/
"""

from pathlib import Path

import mkdocs_gen_files

readme = Path("README.md").open("r")
with mkdocs_gen_files.open("index.md", "w", encoding="utf-8") as index_file:
    index_file.writelines(readme.read())
