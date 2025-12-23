# SPDX-FileCopyrightText: 2025-present Ahum Maitra theahummaitra@gmail.com
#
# SPDX-License-Identifier: 	GPL-3.0-or-later

# Textual necessary sub-packages
import argparse

# for CLI interface
import subprocess

# for cli
from rich import print

# import all textual things
from textual import on
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer

# Import All Textual Widgets
from textual.widgets import Footer, Header, Label, Select

# import current Kimino version
from Kimino import __version__
from Kimino.components.ascii_art import logo  # import Kimino ascii-art logo
from Kimino.components.BashFile_app import (
    BashAppLauncher,  # for creating bash file app entry
)

# import short license notice
from Kimino.components.license_text import license_short_text

# Import all components
from Kimino.components.TUI_app import (
    TuiAppLauncher,  # for creating TUI App desktop entry
)
from Kimino.components.Web_app import (
    WebAppLauncher,  # for creating web app desktop entry
)

# import About screen
from Kimino.pages.About import AboutScreen


# Main app class
class Kimino(App):
    BINDINGS = [("^q", "quit", "Quit the app"), ("a", "about_screen", "About Kimino")]
    CSS_PATH = "./style.tcss"

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        yield Label(f"{logo}", id="logo")  # render main ascii logo

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

    def action_about_screen(self) -> None:
        self.push_screen(AboutScreen())

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


# main function for CLI interface
def main():
    parser = argparse.ArgumentParser(
        prog="Kimino",
        description="Easy to use desktop app entry creator",
        epilog="Thanks for using Kimino!",
    )

    parser.add_argument("--version", action="store_true")
    parser.add_argument("--about", action="store_true")

    args = parser.parse_args()

    if args.version:
        subprocess.run(["clear"])

        print(f"v{__version__}")
        return

    if args.about:
        subprocess.run(["clear"])
        print(f"{logo}\n\n")

        print("[purple bold]Created by Ahum Maitra[/]")

        print(f"[yellow]{license_short_text}[/]")

        return

    # run app
    app: Kimino = Kimino()
    app.run()
