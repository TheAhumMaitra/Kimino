from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.screen import ModalScreen
from textual.widgets import Footer, Label

from Kimino.components.license_text import full_license_text


class FullLicense(ModalScreen):
    CSS_PATH = "./license.tcss"
    BINDINGS = [("escape", "escape_screen", "Escape Full License Screen")]

    def compose(self) -> ComposeResult:
        yield ScrollableContainer(Label(f"{full_license_text}", id="license_text"))

        # render footer
        yield Footer()

    def action_escape_screen(self):
        self.dismiss()
