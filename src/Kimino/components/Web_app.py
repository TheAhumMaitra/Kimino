# SPDX-FileCopyrightText: 2025-present Ahum Maitra theahummaitra@gmail.com
#
# SPDX-License-Identifier: 	GPL-3.0-or-later


import os

from textual import on
from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label


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
