import os
from textual.app import ComposeResult
from textual.widgets import Label, Static, Input, Button
from textual import on


class WebAppLauncher(Static):

    def compose(self) -> ComposeResult:
        yield Label("Write App Name:")
        yield Input(placeholder="Enter app name", id="app_name")

        yield Label("Enter Website URL:")
        yield Input(placeholder="https://example.com", id="web_url")

        yield Label("Enter Browser Name (firefox, brave, chromium, chrome, etc.):")
        yield Input(placeholder="firefox", id="browser_name")

        yield Label("Enter icon path (optional):")
        yield Input(placeholder="Icon Path", id="icon_path")

        yield Button("Create Launcher", id="done_btn", variant="success")


    # -------- CREATE DESKTOP FILE ----------
    def create_web_launcher(self, app_name, url, browser, icon_path):
        # Path for Hyprland / Wayland desktop entries
        desktop_path = os.path.expanduser(f"~/.local/share/applications/{app_name}.desktop")

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
