from src.chat import CustomInstructionGenerator
from src.ui import ITU_MainMenu

### Currently unfunctional with this release

itu = ITU_MainMenu()

itu_result = itu.run()

if itu_result == 1:
    print('This feature is currently being refactored\n')

elif itu_result == 2:
    cig = CustomInstructionGenerator(chosen_model='llama3.2')
    cig._interactive_instruction_builder()

elif itu_result == 3:
    print('This feature is currently being refactored\n')