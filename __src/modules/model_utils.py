import subprocess
import os

class ModelUtils:
    def __init__(self, model_name):
        self.model_name = model_name

    def check_model_installed(self):
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            if self.model_name not in result.stdout:
                print(f"Model '{self.model_name}' not found. Installing...")
                subprocess.run(['ollama', 'pull', self.model_name], check=True)
                print(f"Model '{self.model_name}' installed successfully.")
            else:
                print(f"Model '{self.model_name}' is already installed.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while checking or installing the model: {e}")
            exit(1)
    
    @staticmethod
    def save_chosen_model():
        if os.path.exists('chosen_model.txt'):
            with open('chosen_model.txt', 'r') as file:
                return file.read()
        return None
    
# Example usage:
# model_utils = ModelUtils('llama3.2')
# model_utils.check_model_installed()
# chosen_model = ModelUtils.save_chosen_model()
# print(chosen_model)