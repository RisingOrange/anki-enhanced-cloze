# flake8: noqa: E402
from aqt.gui_hooks import profile_did_open

from .compat import add_compatibility_aliases
from .config import setup_config
from .editor import setup_editor
from .setup_jquery import setup_maybe_add_jquery_to_media_folder
from .menu import setup_enhanced_cloze_menu
from .model import setup_maybe_update_model_on_startup
from .patches import setup_prevent_warnings_about_clozes

profile_did_open.append(add_compatibility_aliases)

setup_config()
setup_maybe_add_jquery_to_media_folder()
setup_maybe_update_model_on_startup()
setup_editor()
setup_enhanced_cloze_menu()
setup_prevent_warnings_about_clozes()
