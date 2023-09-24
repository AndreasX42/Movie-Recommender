import sys
import os
import yaml
from pathlib import Path
import chromadb

FILE = Path(__file__).resolve()
ROOT = FILE.parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

CONFIG = yaml.safe_load(open(os.path.join(ROOT, "config.yml"), encoding="utf-8"))

client = chromadb.PersistentClient(path=os.path.join(ROOT, CONFIG["ChromaDBPath"]))
movie_collection = client.get_collection(name="movies")
user_collection = client.get_collection(name="users")
