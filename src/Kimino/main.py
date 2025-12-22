#   Copyright (C) 2025  Ahum Maitra

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>

# Textual
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer, Container
from textual import on

# Import All Textual Widgets
from textual.widgets import Footer, Header, Label, Select

# Import all components
from Kimino.components.TUI_app import TuiAppLauncher
from Kimino.components.BashFile_app import BashAppLauncher
from Kimino.components.Web_app import WebAppLauncher


# Main app class
class Kimino(App):
    BINDINGS = [("^q", "quit", "Quit the app")]
    CSS_PATH = "./style.tcss"

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        yield Label(
            "[b yellow] Welcome to Kimino, This app helps you to create desktop entry easily![/b yellow]",
            id="weltext",
        )

        Options = ["TUI", "Web App", "Bash file"]
        try:
            yield ScrollableContainer(
                Select.from_values(Options, id="select_mode"),
                ScrollableContainer(id="add_details"),
            )

            # Label to show selected value

        except Exception as Unexpected_Error:
            with open("Error_log.txt", "a") as Error_Log:
                Error_Log.write(f"{Unexpected_Error}")
            quit()
        yield Footer()

    @on(Select.Changed)
    def show(self, event: Select.Changed):
        User_selected_option = event.value
        add = self.query_one("#add_details")

        match User_selected_option:
            case "TUI":
                self.push_screen(TuiAppLauncher())
            case "Bash file":
                self.push_screen(BashAppLauncher())
            case "Web App":
                self.push_screen(WebAppLauncher())

def main():
    app: Kimino = Kimino()
    Kimino().run()


if __name__ == "__main__":
    app: Kimino = Kimino()
    Kimino().run()
