import random
import time
import ollama

class DoubleTexting:
    def __init__(self):
        self.double_texting_binary = 0  # Default state: OFF

    def double_texting_switch(self, on=None):
        if on is None:
            self.double_texting_binary = 1 - self.double_texting_binary
        elif on == True: 
            self.double_texting_binary = 1
        elif on == False:
            self.double_texting_binary = 0
        else:
            print("Invalid input. Use True, False, or no argument to toggle.")
        return self.double_texting_binary

    def double_text(self, rotating_history):
        with open("_double_text_system_instructions.txt", "r", encoding='UTF-8') as double_text_system_instructions_file:
            double_text_system_instruction = double_text_system_instructions_file.read().replace("\n", " ")

        modelfile = f'''
        FROM llama3.2:latest
        SYSTEM {double_text_system_instruction}'''

        ollama.create(model='vinman_converse', modelfile=modelfile)

        if not rotating_history:
            return

        latest_message = rotating_history[-1].split(": ", 1)[1]
        random_wait = random.randint(2, 4)
        time.sleep(random_wait)
        print('Typing...')
        time.sleep(1)
        response = ollama.chat(model='vinman_converse', messages=[
                {
                    'role': 'user',
                    'content': f'Add on to this message, do not respond to it: {latest_message}',
                }
            ])

        self.response_delay(response['message']['content'], 2)
        print(f"\n{YELLOW}{response['message']['content']}{RESET}\n")

    def response_delay(self, message, delay):
        time.sleep(delay)
        print(message)

# Example usage:
# double_texting = DoubleTexting()
# double_texting.double_texting_switch(True)
# double_texting.double_text(rotating_history)