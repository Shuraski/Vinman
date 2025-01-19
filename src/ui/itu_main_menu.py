import os
from src.ui import text_color

class ITU_MainMenu:
    def __init__(self):
        """Initialize the integrated terminal UI."""
        self.options = ["Launch Vinman", "Generate New Personality", f"Activate Double Texting {text_color("RED")}(Unstable Feature){text_color("RESET")}"]

    def run(self):
        """Run the integrated terminal UI."""
        print(f"\n{text_color('BLUE')}Enter {text_color('RED')}'exit'{text_color('RESET')} {text_color('BLUE')}to quit \nConverse Bot Menu Options{text_color('RESET')}\n")
        return self.show_options()

    def show_options(self):
        """Print the options and take input to run the command."""
        while True:
            for idx, option in enumerate(self.options, start=1):
                print(f"{idx}) {option}")
            choice = input("\nSelect an option: ")
            if choice.lower().strip() == 'exit':
                print(f"\n{text_color('RED')}Ending program...{text_color('RESET')}\n")
                return None
            if choice.lower().strip() == 'clear':
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"{text_color('BLUE')}Enter {text_color('RED')}'exit'{text_color('RESET')} {text_color('BLUE')}to quit \nConverse Bot Menu Options{text_color('RESET')}\n")
                continue
            if not choice.isdigit() or int(choice) not in range(1, len(self.options) + 1):
                print(f"\n{text_color('RED')}Invalid choice.{text_color('RESET')}\n")
                continue
            return self.run_command(int(choice))

    def run_command(self, choice):
        """Run the command based on the selected option."""
        if choice == 1:
            print(f"\n{text_color('GREEN')}Conversation Launched{text_color('RESET')}\n")
            return 1
        elif choice == 2:
            print(f"\n{text_color('GREEN')}Personality Creator Launched{text_color('RESET')}\n")
            return 2
        elif choice == 3:
            print(f"\n{text_color('GREEN')}Double Texting Activated{text_color('RESET')}\n")
            return 3
        else:
            print("Invalid option selected.")