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
from textual.app import ComposeResult
from textual.widgets import Label, Input, Button
from textual import on
from textual.screen import ModalScreen
from textual.containers import ScrollableContainer


class WebAppLauncher(ModalScreen):
    BINDINGS = [("escape", "escape_screen", "Escape this screen")]

    def compose(self) -> ComposeResult:
        with ScrollableContainer(id="webapp"):
            yield Label("[b yellow] Press ESC to exit this screen [/b yellow]")
            yield Label("Write App Name:", classes="a")
            yield Input(placeholder="Enter app name", id="app_name", classes="a")

            yield Label("Enter Website URL:")
            yield Input(placeholder="https://example.com", id="web_url", classes="a")

            yield Label(
                "Enter Browser Name (firefox, brave, chromium, chrome, etc.):",
                classes="a",
            )
            yield Input(placeholder="firefox", id="browser_name", classes="a")

            yield Label("Enter icon path (optional):", classes="a")
            yield Input(placeholder="Icon Path", id="icon_path", classes="a")

            yield Button("Create Launcher", id="done_btn", variant="success")

    # -------- CREATE DESKTOP FILE ----------
    def create_web_launcher(self, app_name, url, browser, icon_path):
        # Path for Hyprland / Wayland desktop entries
        desktop_path = os.path.expanduser(
            f"~/.local/share/applications/{app_name}.desktop"
        )

        # Desktop entry template
        content = f"""[Desktop Entry]
Type=Application
Name={app_name}
Exec={browser} "{url}"
Icon={icon_path}
Terminal=false
Categories=Network;WebBrowser;
StartupNotify=true
"""

        # Write the launcher
        with open(desktop_path, "w") as file:
            file.write(content)

        # Make it executable
        os.chmod(desktop_path, 0o755)

        return desktop_path

    # -------- BUTTON HANDLER ----------
    @on(Button.Pressed, "#done_btn")
    def handle_done(self, event):
        app_name = self.query_one("#app_name", Input).value.strip()
        url = self.query_one("#web_url", Input).value.strip()
        browser = self.query_one("#browser_name", Input).value.strip()
        icon_path = self.query_one("#icon_path", Input).value.strip()

        if not app_name or not url or not browser:
            self.mount(Label("❌ Error: App name, URL, and Browser must be filled!"))
            return

        path = self.create_web_launcher(app_name, url, browser, icon_path)

        self.mount(Label(f"✔ Web App launcher created!\n{path}"))

    def action_escape_screen(self):
        self.dismiss()
