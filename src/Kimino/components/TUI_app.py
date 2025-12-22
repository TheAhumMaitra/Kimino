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


import os
from types import LambdaType
from textual.app import ComposeResult
from textual.widgets import Label, Input, Button
from textual import on
from textual.screen import ModalScreen
from textual.containers import ScrollableContainer


class TuiAppLauncher(ModalScreen):
    BINDINGS = [("escape", "escape_screen", "Escape this screen")]

    def compose(self) -> ComposeResult:
        with ScrollableContainer(id="tuiapp"):
            yield Label("[b yellow] Press ESC to exit this screen [/b yellow]")
            yield Label("Write App Name:")
            yield Input(placeholder="Enter app name", id="app_name")

            yield Label("Enter TUI Command (ex: nvim, htop, yazi, code):")
            yield Input(placeholder="tui-command", id="tui_command")

            yield Label(
                "Enter Terminal Launcher (ex: kitty -e, foot -e, alacritty -e):"
            )
            yield Input(placeholder="terminal -e", id="terminal_cmd")

            yield Label("Enter icon path (optional):")
            yield Input(placeholder="Icon Path", id="icon_path")

            yield Button("Create Launcher", id="done_btn", variant="success")

    # -------- CREATE DESKTOP FILE ----------
    def create_tui_launcher(self, app_name, command, terminal, icon_path):
        desktop_path = os.path.expanduser(
            f"~/.local/share/applications/{app_name}.desktop"
        )

        # Build Exec command using provided terminal
        exec_cmd = f'{terminal} "{command}"'

        content = f"""[Desktop Entry]
Type=Application
Name={app_name}
Exec={exec_cmd}
Icon={icon_path}
Terminal=true
Categories=Utility;ConsoleOnly;
StartupNotify=false
"""

        # Write file
        with open(desktop_path, "w") as file:
            file.write(content)

        os.chmod(desktop_path, 0o755)
        return desktop_path

    # -------- BUTTON HANDLER ----------
    @on(Button.Pressed, "#done_btn")
    def handle_done(self, event):
        app_name = self.query_one("#app_name", Input).value.strip()
        command = self.query_one("#tui_command", Input).value.strip()
        terminal = self.query_one("#terminal_cmd", Input).value.strip()
        icon_path = self.query_one("#icon_path", Input).value.strip()

        if not app_name or not command or not terminal:
            self.mount(
                Label("❌ Error: App name, command, and terminal must be filled!")
            )
            return

        path = self.create_tui_launcher(app_name, command, terminal, icon_path)

        self.mount(Label(f"✔ TUI launcher created!\n{path}"))

    def action_escape_screen(self):
        self.dismiss()
