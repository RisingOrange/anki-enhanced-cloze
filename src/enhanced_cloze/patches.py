from anki.notes import Note
from aqt import mw
from aqt.editor import Editor
from aqt.gui_hooks import add_cards_will_add_note
from aqt.utils import tr

from .constants import ANKI_VERSION, MODEL_NAME
from .lib.packaging.version import Version


def setup_prevent_warnings_about_clozes() -> None:
    if ANKI_VERSION == Version("2.1.26"):
        from anki.models import ModelManager

        original_availableClozeOrds = (
            ModelManager._availClozeOrds  # pylint: disable=protected-access
        )

        def new_availClozeOrds(self, m, flds: str, allowEmpty: bool = True):
            if m["name"] != MODEL_NAME:
                return original_availableClozeOrds(self, m, flds, allowEmpty)

            # the exact value is not important, it has to be an non-empty array
            return [0]

        ModelManager._availClozeOrds = (  # type: ignore  # pylint: disable=protected-access
            new_availClozeOrds
        )
    elif ANKI_VERSION < Version("2.1.45"):
        original_cloze_numbers_in_fields = Note.cloze_numbers_in_fields

        def new_cloze_numbers_in_fields(self):
            if self.note_type()["name"] != MODEL_NAME:
                return original_cloze_numbers_in_fields(self)

            # the exact value is not important, it has to be an non-empty array
            return [0]

        Note.cloze_numbers_in_fields = (  # type: ignore # pylint: disable=protected-access
            new_cloze_numbers_in_fields
        )
    else:
        from anki.notes import NoteFieldsCheckResult

        original_update_duplicate_display = (
            Editor._update_duplicate_display  # pylint: disable=protected-access
        )

        def _update_duplicate_display_ignore_cloze_problems_for_enh_clozes(
            self, result
        ) -> None:
            if self.note.note_type()["name"] == MODEL_NAME:
                if result == NoteFieldsCheckResult.NOTETYPE_NOT_CLOZE:
                    result = NoteFieldsCheckResult.NORMAL
                if result == NoteFieldsCheckResult.FIELD_NOT_CLOZE:
                    result = NoteFieldsCheckResult.NORMAL
            original_update_duplicate_display(self, result)

        Editor._update_duplicate_display = (  # type: ignore  # pylint: disable=protected-access
            _update_duplicate_display_ignore_cloze_problems_for_enh_clozes
        )

        def ignore_some_cloze_problems_for_enh_clozes(problem, note):
            if note.note_type()["name"] != MODEL_NAME:
                return problem

            if problem == tr.adding_cloze_outside_cloze_notetype():
                return None
            elif problem == tr.adding_cloze_outside_cloze_field():
                return None
            else:
                return problem

        add_cards_will_add_note.append(ignore_some_cloze_problems_for_enh_clozes)

        # the warning about no clozes in the field will still show up in version lower 2.1.45
        original_fields_check = Note.fields_check

        def new_fields_check(self):
            result = original_fields_check(self)

            if mw.col.models.get(self.mid)["name"] != MODEL_NAME:
                return result

            if result == NoteFieldsCheckResult.MISSING_CLOZE:
                return None
            else:
                return result

        Note.fields_check = new_fields_check  # type: ignore
