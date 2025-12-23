from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.containers import ScrollableContainer

# import ascii logo
from Kimino.components.ascii_art import logo

# import Textual all required widgets
from textual.widgets import Label, Footer

# import Kimino's current version
from Kimino import __version__

# import short license text
from Kimino.components.license_text import license_short_text

class AboutScreen(ModalScreen):
    CSS_PATH = "./about.tcss"
    BINDINGS = [("escape", "escape_screen", "Escape About Screen")]

    def compose(self) -> ComposeResult:
        with ScrollableContainer(id="about_container"):
            yield Label(f"{logo}", id="about_logo")
            yield Label(f"[b yellow]Kimino is a blazingly fast, easy to use Linux desktop entry creator.[/b yellow]", id="description")
            yield Label("[b blueviolet]Created by [b italic orange]Ahum Maitra[/b italic orange][/b blueviolet]", id="creator")
            yield Label(f"[b italic red]Version : [b italic skyblue]v{__version__}[/b italic skyblue][/b italic red]", id="current_version")
            yield Label(f"{license_short_text}", id="license_short_text")

        yield Footer() #For showing bindings



    #escape the About Screen
    def action_escape_screen(self):
        self.dismiss()
