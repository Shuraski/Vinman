# Standard Imports
import json
import os
import random
import time
import subprocess

# Third Party Imports
import ollama

BLUE = '\033[94m'
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
UNDERLINE = '\033[4m'
BOLD = '\033[1m'
RESET = '\033[0m'

file_path = ""

# Checking Whether the Model is Installed
def check_model_installed(model_name):
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if model_name not in result.stdout:
            print(f"Model '{model_name}' not found. Installing...")
            subprocess.run(['ollama', 'pull', model_name], check=True)
            print(f"Model '{model_name}' installed successfully.")
        else:
            print(f"Model '{model_name}' is already installed.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while checking or installing the model: {e}")
        exit(1)

### NOT IMPLEMENTED YET ###
# Saving Chosen Model
def save_chosen_model():
    if os.path.exists('chosen_model.txt'):
        with open('chosen_model.txt', 'r') as file:
            return file.read()
    return None

### NOT IMPLEMENTED YET ###
# Implement function to load chosen model from saved file
def load_chosen_model(model_name):
    if os.path.exists('chosen_model.txt'):
        with open('chosen_model.txt', 'r') as file:
            first_line = file.readline().strip()
            if first_line == model_name:
                return first_line
            else:
                return None
    return None

### NOT IMPLEMENTED YET ###
# Checking Whether (chosen_model) Has Content
def check_model_content(check_model):
    return chosen_model if chosen_model else 'llama3.2'

# Response Delay Function
def response_delay(delay_text,delay_time):

    for char in delay_text:
        time.sleep(0.01)
    time.sleep(delay_time)

# Chat History Functions
def chat_history_reset():

    global rotating_history
    rotating_history = []

def chat_history_store(user_input_text = None, vinman_output_text = None):

    assert user_input_text or vinman_output_text, "At least one input must be provided."

    if user_input_text:
        rotating_history.append(f"Input: {user_input_text}")

    if vinman_output_text:
        rotating_history.append(f"Output: {vinman_output_text}")

double_texting_binary = 0  # Default state: OFF

# Double Texting Switch
def double_texting_switch(on=None):

    global double_texting_binary

    if on is None:
        double_texting_binary = 1 - double_texting_binary
    elif on == True: 
        double_texting_binary = 1
    elif on == False:
        double_texting_binary = 0
    else:
        print("Invalid input. Use True, False, or no argument to toggle.")

    return double_texting_binary

# Double Text Function
def double_text():
    
    with open("_double_text_system_instructions.txt",
          "r", encoding='UTF-8') as double_text_system_instructions_file:
        double_text_system_instruction = double_text_system_instructions_file.read().replace("\n", " ")

    modelfile = f'''
    FROM {chosen_model}
    SYSTEM {double_text_system_instruction}'''

    ollama.create(model='vinman_converse', modelfile=modelfile)

    if not rotating_history:
        return
    
    latest_message = rotating_history[-1].split(": ", 1)[1]
    random_wait = random.randint(2,4)
    time.sleep(random_wait)
    print('Typing...')
    time.sleep(1)
    response = ollama.chat(model='vinman_converse', messages=[
            {
                'role': 'user',
                'content': f'Add on to this message, do not respond to it: {latest_message}',
            }
        ])
    
    response_delay(response['message']['content'],2)
    print(f"\n{YELLOW}{response['message']['content']}{RESET}\n")

# Custom Instruction Generator
def custom_instruction_generator(memory_input = None):

    with open("_system_writer_system_instructions.json", "r", encoding='UTF-8') as sys_writer_system_instruction_file:
        sys_writer_system_instruction = json.load(sys_writer_system_instruction_file)

    modelfile = f'''
    FROM {chosen_model}
    SYSTEM {sys_writer_system_instruction}'''

    ollama.create(model='vinman_converse', modelfile=modelfile)

    if memory_input:

        with open("_history_writer_system_instructions.json", "r", encoding='UTF-8') as history_writer_system_instruction_file:
            history_writer_system_instruction = json.load(history_writer_system_instruction_file)

        with open("vinman_custom_instructions.txt",
          "r", encoding='UTF-8') as vinman_personality_instruction_file:
            vinman_personality_instruction = vinman_personality_instruction_file.read().replace("\n", " ")

        modelfile = f'''
        FROM {chosen_model}
        SYSTEM Core personality: {vinman_personality_instruction} Chat log: {history_writer_system_instruction} I want you to build on top of the core personality based off of what is inside the chat log.'''

        ollama.create(model='vinman_converse', modelfile=modelfile)

        response = ollama.chat(model='vinman_converse', messages=[
                {
                    'role': 'user',
                    'content': f'Analyze the following chat log and extract key details, including significant information and personality traits. {memory_input}',
                }
            ])
        
        with open("vinman_custom_instructions.txt", "a", encoding="UTF-8") as file:
            file.write(f"\n{response['message']['content']}")
            return

    print(f"\n{BLUE}Enter {RESET}{RED}'exit'{RESET} {BLUE}to end the instruction builder, or for more options, enter '?' for instruction prompt examples\nDefine the AI's personality or behavior (e.g., tone, style, purpose): {RESET}\n")
    while True:
        user_input = input("Enter personality: ")

        if user_input.lower() == 'exit':
            print(f"\n{RED}Ending chat...{RESET}")
            break

        elif user_input.strip() == '?':
            print(f'''\n{BLUE}You're currently in the process of creating a personality for the Converse Bot. Don't worry about making your request perfect; feel free to keep it as rough or messy as you like. Just include a name and some personality traits to guide how the bot should behave.
                  \nHere are some prompt examples:\n* A grumpy old man named Terry who hates loud noise\n* Larry, a happy boy who likes to dance\n* Amy, responds with a lot of text acronyms{RESET}\n''')

        elif user_input.strip() != '?':
            print(f"\nGenerating personality...")
            response = ollama.chat(model='vinman_converse', messages=[
                {
                    'role': 'user',
                    'content': user_input,
                }
            ])

            print(f'\n{GREEN}Personality generated{RESET}')
            with open("vinman_custom_instructions.txt", "w", encoding="UTF-8") as file:
                file.write(f"{response['message']['content']}")
            
            if os.path.exists('vinman_custom_instructions.txt'):
                break

# Vinman Converse Main Chat Function
def chat():

    with open("_vinman_system_instructions.json", "r", encoding='UTF-8') as vinman_system_instruction_file:
        vinman_system_instruction = json.load(vinman_system_instruction_file)
    
    with open("vinman_custom_instructions.txt",
          "r", encoding='UTF-8') as vinman_personality_instruction_file:
        vinman_personality_instruction = vinman_personality_instruction_file.read().replace("\n", " ")

    modelfile = f'''
    FROM {chosen_model}
    SYSTEM This is your base system instruction: {vinman_system_instruction} This is your personality: {vinman_personality_instruction}'''

    ollama.create(model='vinman_converse', modelfile=modelfile)

    conversation_history = [
        {"role": "system", "content": f"These are your base system instructions: {vinman_system_instruction} Consider this as your personality: {vinman_personality_instruction}"}
    ]

    print(f"{BLUE}Enter {RED}'exit'{BLUE} to end the chat{RESET}\n")
    while True:
        user_input = input(f"Enter message: ")
        if user_input.lower() == 'exit':
            while True:
                personality_update = input("\nWould you like to update this personality with the new details? Y/N (enter '?' for more details or 'C' to resume this chat): ")
                
                if personality_update.lower().strip() == 'exit':
                    print(f"\n{RED}Ending chat...{RESET}")
                    return

                elif personality_update.lower().strip() == 'y':
                    print("\nUpdating Personality...")
                    custom_instruction_generator(rotating_history)
                    print(f"\n{GREEN}Personality Updated{RESET}")
                    return
                
                elif personality_update.lower().strip() == 'n':
                    print(f"\n{RED}Ending chat...{RESET}")
                    return

                elif personality_update.lower().strip() == 'c':
                    print(f"\n{GREEN}Chat Resumed{RESET}\n")
                    break

                elif personality_update.lower().strip() == '?':
                    print(f"\n{BLUE}Additional information:\n\nEach chat is saved in a temporary history, allowing the Converse Bot to understand the context of your conversation.\nIf you discuss something specific, you can save the chat as a personality update so the Converse Bot remembers it for future interactions.\nFor example, if you specify or change the Converse Bot's last name, it will retain that update.{RESET}")
                
                else:
                    print(f"\n{RED}Invalid choice. Please enter Y/N, or C to resume this chat.{RESET}")   
            continue

        response = ollama.chat(model='vinman_converse', messages=[
            {
                'role': 'user',
                'content': user_input,
            }
        ])

        conversation_history.append({"role": "user", "content": user_input})

        response = ollama.chat(model='vinman_converse', messages=conversation_history)
        model_reply = response['message']['content']
        conversation_history.append({"role": "assistant", "content": model_reply})
        
        chat_history_store(user_input)
        chat_history_store(vinman_output_text = model_reply)

        response_delay(user_input,0)
        print('\nTyping...')
        response_delay(response['message']['content'],2)
        print(f"\n{YELLOW}{response['message']['content']}{RESET}\n")

        if double_texting_binary == 1:
            double_text()

# Main Program Loop
while True:
    if not os.path.exists('vinman_custom_instructions.txt'):
        
        global current_model

        print(f"\n{UNDERLINE}{BOLD}Recommended: llama3.2{RESET}\n"
            f"Parameter Size: 3b\n"
            f"Required Storage: 2.0 GB\n")
        
        print(f"{UNDERLINE}{BOLD}dolphin-mistral:latest{RESET}\n"
              f"Parameter Size: 7b\n"
              f"Required Storage: 4.1 GB\n")

        chosen_model = input(f"{BLUE}Choose a model to install: {RESET}")

        if chosen_model.lower().strip() == "llama3.2":
            check_model_installed(chosen_model)
            current_model =  chosen_model
            custom_instruction_generator()
        
        elif chosen_model.lower().strip() == "dolphin-mistral:latest":
            check_model_installed(chosen_model)
            current_model = chosen_model
            custom_instruction_generator()
        
        elif chosen_model.lower().strip() == 'exit':
            print(f"\n{RED}Ending program...{RESET}\n")
            break

        else:
            print(f"{RED}Invalid choice. Please enter a valid model name.{RESET}")
            continue

    else:
        print(f"\n{BLUE}Enter{RESET}{RED} 'exit' {RESET}{BLUE}to quit\nConverse Bot Menu Options:{RESET}\n")
        print("1) Launch Converse Bot")
        print("2) Generate a New Personality")

        if double_texting_binary == None:
            print(f"3) Activate Double Texting {RED}(Unstable Feature){RESET}")
        elif double_texting_binary == True:
            print(f"3) De-Activate Double Texting {RED}(Unstable Feature){RESET}")
        elif double_texting_binary == False:
            print(f"3) Activate Double Texting {RED}(Unstable Feature){RESET}")

        choice = input("\nEnter your choice (1-3): ")

        if choice.lower().strip() == 'exit':
            print(f"\n{RED}Ending program...{RESET}\n")
            break

        elif choice.lower().strip() == '1':
            print(f"\n{GREEN}Conversation Launched{RESET}\n")
            chat_history_reset()
            chat()

        elif choice.lower().strip() == '2':
            print(f"\n{GREEN}Personality Creation Launched{RESET}")
            
            print(f"\n{RED}Warning: Generating a new personality will overwrite the current personality{RESET}")
            custom_instruction_generator()
        
        elif choice.lower().strip() == '3':
            
            if double_texting_binary == None:
                print(f"\n{GREEN}Double Texting Activated{RESET}")
                double_texting_switch(on=True)

            elif double_texting_binary == True:
                print(f"\n{GREEN}Double Texting De-Activated{RESET}")
                double_texting_switch(on=False)

            elif double_texting_binary == False:
                print(f"\n{GREEN}Double Texting Activated{RESET}")
                double_texting_switch(on=True)

        else:
            print(f"\n{RED}Invalid choice. Please enter a number between 1 and 3, or type 'exit' to quit.{RESET}")