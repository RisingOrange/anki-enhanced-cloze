import re
from typing import Callable, List, Tuple

from anki.hooks import note_will_flush
from anki.notes import Note
from aqt.editor import Editor
from aqt.gui_hooks import editor_did_init_shortcuts
from aqt.qt import Qt

from .constants import ANKI_VERSION, MODEL_NAME
from .lib.packaging.version import Version  # type: ignore


# this is needed so the no-cloze mode works
def maybe_fill_in_or_remove_cloze99(note: Note) -> None:
    def in_use_clozes():
        cloze_start_regex = r"{{c\d+::"
        cloze_start_matches = re.findall(cloze_start_regex, note["Content"])
        return [int(re.sub(r"\D", "", x)) for x in set(cloze_start_matches)]

    if note and note.note_type()["name"] == MODEL_NAME:
        if in_use_clozes():
            note["Cloze99"] = ""
        else:
            note["Cloze99"] = "{{c1::.}}"


def make_cloze_shortcut_start_at_cloze1(shortcuts: List[Tuple], editor: Editor) -> None:
    original_onCloze = Editor.onCloze

    # code adapted from original onCloze and _onCloze
    def myOnCloze(self) -> None:
        if self.note.note_type()["name"] == MODEL_NAME:
            self.call_after_note_saved(lambda: _myOnCloze(editor), keepFocus=True)
        else:
            original_onCloze(self)

    def _myOnCloze(self) -> None:
        # find the highest existing cloze
        highest = 0
        val = self.note["Content"]
        m = re.findall(r"\{\{c(\d+)::", val)
        if m:
            highest = max(highest, sorted([int(x) for x in m])[-1])
        # reuse last?
        if not self.mw.app.keyboardModifiers() & Qt.KeyboardModifier.AltModifier:
            highest += 1
        # must start at 1
        highest = max(1, highest)
        self.web.eval("wrap('{{c%d::', '}}');" % highest)

    replace_shortcut(shortcuts, "Ctrl+Shift+C", lambda: myOnCloze(editor))
    replace_shortcut(shortcuts, "Ctrl+Shift+Alt+C", lambda: myOnCloze(editor))


def replace_shortcut(
    shortcuts: List[Tuple],
    key_combination: str,
    func: Callable[[], None],
) -> None:
    existing = next((x for x in shortcuts if x[0] == key_combination), None)
    if existing is not None:
        shortcuts.remove(existing)
    shortcuts.append((key_combination, func))


def setup_editor() -> None:
    note_will_flush.append(maybe_fill_in_or_remove_cloze99)
    if ANKI_VERSION < Version("2.1.50"):
        editor_did_init_shortcuts.append(make_cloze_shortcut_start_at_cloze1)
