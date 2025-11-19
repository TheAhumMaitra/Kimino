from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer, Container
from textual import on

# Import All Textual Widgets
from textual.widgets import Footer, Header, Label, Select

# Import all components
from components.TUI_app import TuiAppLauncher
from components.BashFile_app import BashAppLauncher
from components.Web_app import WebAppLauncher

class Kimino(App):
    BINDINGS = [("^q", "quit", "Quit the app")]
    CSS_PATH = "./styles/style.tcss"

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        Options = ["TUI", "Web App", "Bash file"]
        try:
            yield ScrollableContainer(
                Select.from_values(Options, id="select_mode"),

                ScrollableContainer(
                    id="add_details"
                )
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

        if User_selected_option == "TUI":
            add.mount(TuiAppLauncher())
        elif User_selected_option == "Web App":
            add.mount(WebAppLauncher())
        elif User_selected_option == "Bash file":
            add.mount(BashAppLauncher())
        else:
            add.mount(Label("Invalid option or nothing selected, it can be an unexpected error."))




if __name__ == "__main__":
    try:
        Kimino().run()

    except Exception as UnexpectedError:
        error = UnexpectedError
        with open("Error_log.txt", "a") as Error_Log:
                Error_Log.write(f"THE APP DIDN'T RUN SUCCESSFULLY \n \n ERROR : \n\n {error}")
                quit()
