import os
from src.ui.text_styling import TextStyling

class ITU_MainMenu:
    def __init__(self):
        """Initialize the integrated terminal UI."""
        self.text_styling = TextStyling()
        self.options = [
            "Launch Vinman", 
            "Generate New Personality", 
            f"Activate Double Texting {self.text_styling.text_color('RED')}(Unstable Feature){self.text_styling.text_color('RESET')}"
        ]

    def run(self):
        """Run the integrated terminal UI."""
        self.clear_terminal()
        print(f"{self.text_styling.text_formatting('UNDERLINE')}{self.text_styling.text_formatting('BOLD')}{self.text_styling.text_color('YELLOW')}Vinman Menu Options{self.text_styling.text_formatting('RESET')}\n")
        return self.show_options()

    def show_options(self):
        """Print the options and take input to run the command."""
        while True:
            for idx, option in enumerate(self.options, start=1):
                print(f"{idx}) {option}")
            choice = input("\nSelect an option: ")
            if choice.lower().strip() == 'exit':
                print(f"\n{self.text_styling.text_color('RED')}Ending program...{self.text_styling.text_color('RESET')}\n")
                return None
            if not choice.isdigit() or int(choice) not in range(1, len(self.options) + 1):
                self.clear_terminal()
                print(f"{self.text_styling.text_color('RED')}Invalid choice.{self.text_styling.text_color('RESET')}\n")
                print(f"{self.text_styling.text_formatting('UNDERLINE')}{self.text_styling.text_formatting('BOLD')}{self.text_styling.text_color('YELLOW')}Vinman Menu Options{self.text_styling.text_formatting('RESET')}\n")
                continue
            return self.run_command(int(choice))

    def run_command(self, choice):
        """Run the command based on the selected option."""
        self.clear_terminal()
        if choice == 1:
            return 1
        elif choice == 2:
            return 2
        elif choice == 3:
            return 3
        else:
            print("Invalid option selected.")

    def clear_terminal(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')