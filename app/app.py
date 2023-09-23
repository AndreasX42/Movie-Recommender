import sys
from pathlib import Path

# add root directory to sys path so that utils is importable
FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]  # root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from utils import init_db

init_db()
