import shutil

from aqt.gui_hooks import profile_did_open

from pathlib import Path
import aqt

# Name of the jQuery file in the resources folder.
# This has to be the same filename as the card template uses.
# The underscore in the front prevents Anki from cleaning up the file when Check Media is run.
JQUERY_FILE_NAME = "_jquery.min.js"
JQUERY_PATH = Path(__file__).parent / "resources" / JQUERY_FILE_NAME


def setup_maybe_add_jquery_to_media_folder() -> None:
    profile_did_open.append(_maybe_add_jquery_to_media_folder)


def _maybe_add_jquery_to_media_folder() -> None:
    media_folder = Path(aqt.mw.col.media.dir())
    media_folder_jquery_path = media_folder / JQUERY_FILE_NAME
    if not media_folder_jquery_path.exists():
        shutil.copy(JQUERY_PATH, media_folder_jquery_path)
