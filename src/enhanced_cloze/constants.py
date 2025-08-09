from pathlib import Path

from anki.buildinfo import version as anki_version
from .lib.packaging.version import Version

MODEL_NAME = "Enhanced Cloze 2.1 v2"
ANKI_VERSION = Version(anki_version)
NOTE_TYPE_DIR = Path(__file__).parent / "note_type"


UPDATE_MSG = f"""\
Do you want to update the <b>{MODEL_NAME}</b> note type?<br><br>\
The changes include:
<ul>
<li>Adding and editing notes on mobile works now (except for adding notes without clozes)</li>
<li>New shortcuts for reavaling clozes (configurable):
<ul>
<li>J           - Reveal Next Genuine Cloze</li>
<li>Shift+J     - Toggle All Genuine Clozes</li>
<li>N           - Reveal Next Pseudo Cloze</li>
<li>Shift+N     - Toggle All Pseudo Clozes</li>
</ul>
<li>A new option to disable scrolling to a cloze when it is revealed</li>
<li>All Cloze1, Cloze2, ... fields except for Cloze99 are not longer necessary and were removed \
(also the data field)</li>
<li>Some fixes</li>
</ul>

This will require a full sync to AnkiWeb (if you use synchronization).<br><br>

If you have made changes to the note type and don\'t want to loose them you can duplicate the note type first \
(Tools->Manage Note Types->Add).
<br><br>
If you don't want to update you can get the previous version of the add-on from \
<a href="https://github.com/RisingOrange/anki-enhanced-cloze/releases/tag/1.1.4">here</a>.
<br><br>
<b>Note:</b> If you choose "No" this notice will show up the next time you open Anki."""
