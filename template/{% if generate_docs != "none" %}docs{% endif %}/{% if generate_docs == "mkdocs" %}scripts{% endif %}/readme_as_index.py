"""Use the root README as index in case there is no docs/index.md yet."""

from pathlib import Path

import mkdocs_gen_files

root = Path(__file__).parent.parent.parent

if not Path(root, "docs", "index.md").exists():
    with mkdocs_gen_files.open("index.md", "w") as index:
        with open(root / "README.md") as readme:
            index.writelines(readme.readlines())
