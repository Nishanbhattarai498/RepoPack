from pathlib import Path

from src.repopack import pack_repository

if __name__ == "__main__":
    source = Path(__file__).resolve().parent
    destination = source / "project_bundle.md"
    pack_repository(source, destination)
    print(f"Packaged files to {destination}")
