from src.chat import CustomInstructionGenerator
from src.ui.itu_main_menu import ITU_MainMenu

itu = ITU_MainMenu()

itu_result = itu.run()

if itu_result == 1:
    print('This feature is currently being refactored')
elif itu_result == 2:
    cig = CustomInstructionGenerator(chosen_model='llama3.2')
    cig._interactive_instruction_builder()
elif itu_result == 3:
    print('This feature is currently being refactored')