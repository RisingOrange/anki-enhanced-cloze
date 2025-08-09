from pathlib import Path
import subprocess

PROJECT_ROOT = Path(__file__).parent.parent
BUNDLE_FILE = PROJECT_ROOT / "bundle.txt"
LIB_TARGET = PROJECT_ROOT / "src/enhanced_cloze/lib"

LIB_TARGET.mkdir(exist_ok=True)
subprocess.run(
    [
        "pip",
        "install",
        *BUNDLE_FILE.read_text().strip().splitlines(),
        "--target",
        str(LIB_TARGET),
    ],
    check=True,
)
