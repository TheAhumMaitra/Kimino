import os
from textual.app import ComposeResult
from textual.widgets import Label, Static, Input, Button
from textual import on


class BashAppLauncher(Static):


    def compose(self) -> ComposeResult:
        yield Label("Write App Name:")
        yield Input(placeholder="Enter app name", id="app_name")

        yield Label("Enter Bash File Path:")
        yield Input(placeholder="/home/user/run.sh", id="bash_path")

        yield Label("Enter Terminal Launcher (ex: kitty -e, foot -e, alacritty -e):")
        yield Input(placeholder="terminal -e", id="terminal_cmd")

        yield Label("Enter icon path (optional):")
        yield Input(placeholder="Icon Path", id="icon_path")

        yield Button("Create Launcher", id="done_btn", variant="success")


    # -------- CREATE DESKTOP FILE ----------
    def create_bash_launcher(self, app_name, bash_path, terminal, icon_path):
        desktop_path = os.path.expanduser(
            f"~/.local/share/applications/{app_name}.desktop"
        )

        # Ensure bash file is executable
        try:
            os.chmod(bash_path, 0o755)
        except:
            pass

        # Final Exec command
        exec_cmd = f'{terminal} "{bash_path}"'

        # Desktop entry content
        content = f"""[Desktop Entry]
Type=Application
Name={app_name}
Exec={exec_cmd}
Icon={icon_path}
Terminal=true
Categories=Utility;
StartupNotify=false
"""

        # Write the file
        with open(desktop_path, "w") as file:
            file.write(content)

        os.chmod(desktop_path, 0o755)
        return desktop_path


    # -------- BUTTON HANDLER ----------
    @on(Button.Pressed, "#done_btn")
    def handle_done(self, event):

        app_name = self.query_one("#app_name", Input).value.strip()
        bash_path = self.query_one("#bash_path", Input).value.strip()
        terminal = self.query_one("#terminal_cmd", Input).value.strip()
        icon_path = self.query_one("#icon_path", Input).value.strip()

        if not app_name or not bash_path or not terminal:
            self.mount(Label("❌ Error: App name, Bash path, and terminal must be filled!"))
            return

        path = self.create_bash_launcher(app_name, bash_path, terminal, icon_path)

        self.mount(Label(f"✔ Bash App launcher created!\n{path}"))

