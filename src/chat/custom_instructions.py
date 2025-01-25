import json
import ollama
import os
from src.ui import LoadingAnimation, TextStyling, PlaceholderInput

class CustomInstructionGenerator:
    def __init__(self, chosen_model, memory_input=None):
        self.chosen_model = chosen_model
        self.memory_input = memory_input
        self.text_styling = TextStyling()

    def generate_instructions(self):
        with open("_system_writer_system_instructions.json", "r", encoding='UTF-8') as sys_writer_system_instruction_file:
            sys_writer_system_instruction = json.load(sys_writer_system_instruction_file)

        modelfile = f'''
        FROM {self.chosen_model}
        SYSTEM {sys_writer_system_instruction}'''

        ollama.create(model='vinman_converse', modelfile=modelfile)

        if self.memory_input:
            self._process_memory_input()
        else:
            self._interactive_instruction_builder()

    def _process_memory_input(self):
        with open("_history_writer_system_instructions.json", "r", encoding='UTF-8') as history_writer_system_instruction_file:
            history_writer_system_instruction = json.load(history_writer_system_instruction_file)

        with open("vinman_custom_instructions.txt", "r", encoding='UTF-8') as vinman_personality_instruction_file:
            vinman_personality_instruction = vinman_personality_instruction_file.read().replace("\n", " ")

        modelfile = f'''
        FROM {self.chosen_model}
        SYSTEM Core personality: {vinman_personality_instruction} Chat log: {history_writer_system_instruction} I want you to build on top of the core personality based off of what is inside the chat log.'''

        ollama.create(model='vinman_converse', modelfile=modelfile)

        response = ollama.chat(model='vinman_converse', messages=[
                {
                    'role': 'user',
                    'content': f'Analyze the following chat log and extract key details, including significant information and personality traits. {self.memory_input}',
                }
            ])
        
        with open("vinman_custom_instructions.txt", "a", encoding="UTF-8") as file:
            file.write(f"\n{response['message']['content']}")

    def _interactive_instruction_builder(self):
        print(f"{self.text_styling.text_color('BLUE')}Enter {self.text_styling.reset_text_formatting('RESET')}{self.text_styling.text_color('RED')}'exit'{self.text_styling.reset_text_formatting('RESET')} {self.text_styling.text_color('BLUE')}to end the instruction builder, or for more options, enter '?' for instruction prompt examples\nDefine the AI's personality or behavior (e.g., tone, style, purpose)\n{self.text_styling.reset_text_formatting('RESET')}")
        while True:
            text_styling = TextStyling()
            placeholder_input = PlaceholderInput(f'{text_styling.text_color('GRAY')}Enter "exit" to end instruction builder or "?" for more details {text_styling.reset_text_formatting('RESET')}')
            user_input = placeholder_input.get_input()

            if user_input.lower() == 'exit':
                print(f"\n{self.text_styling.text_color('RED')}Ending chat...{self.text_styling.reset_text_formatting('RESET')}\n")
                break

            elif user_input.strip() == '?':
                print(f"""\n{self.text_styling.text_color('BLUE')}You're currently in the process of creating a personality for the Vinman. Don't worry about making your request perfect; feel free to keep it as rough or messy as you like. Just include a name and some personality traits to guide how the Vinman should behave.
                      \nHere are some prompt examples:\n* A grumpy old man named Terry who hates loud noise\n* Larry, a happy boy who likes to dance\n* Amy, responds with a lot of text acronyms\n{self.text_styling.reset_text_formatting('RESET')}""")

            elif user_input.strip() != '?':
                print('\n')
                animation = LoadingAnimation()
                animation.start("Generating Personality")

                response = ollama.chat(model='vinman_converse', messages=[
                    {
                        'role': 'user',
                        'content': user_input,
                    }
                ])

                animation.stop(f'{self.text_styling.text_color('GREEN')}Personality generated{self.text_styling.reset_text_formatting('RESET')}\n')
                with open("vinman_custom_instructions.txt", "w", encoding="UTF-8") as file:
                    file.write(f"{response['message']['content']}")
                
                if os.path.exists('vinman_custom_instructions.txt'):
                    break