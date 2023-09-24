import sys
import os
import yaml
import logging
from pathlib import Path
import chromadb

FILE = Path(__file__).resolve()
ROOT = FILE.parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

CONFIG = yaml.safe_load(open(os.path.join(ROOT, "config.yml"), encoding="utf-8"))


def getOrCreateChromaDb():
    """Check if chromadb exists by looking for the users collection. If not, we set it up."""

    logging.info("Checking for Chromadb.")

    try:
        chromadb.PersistentClient(
            path=os.path.join(ROOT, CONFIG["ChromaDBPath"])
        ).get_collection(name="users")

    except ValueError:
        logging.info(
            "ChromaDb does not exist. Start initializing, this can take a few minutes"
        )
        from utils import init_db

        init_db()
