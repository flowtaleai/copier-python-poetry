from pathlib import Path
import mkdocs_gen_files

root = Path(__file__).parent.parent.parent

if not Path(root / "index.md").exists():
    with mkdocs_gen_files.open("index.md", "w") as index:
        with open(root / "README.md") as readme:
            index.writelines(readme.readlines())
