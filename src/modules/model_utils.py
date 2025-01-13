import json
import os
import subprocess

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
    def save_chosen_model(model_name):
        config_path = os.path.join(os.path.dirname(__file__), '../../data/config/active_models.json')
        with open(config_path, 'w') as file:
            json.dump({"active_model": model_name}, file)
    
    @staticmethod
    def load_chosen_model():
        config_path = os.path.join(os.path.dirname(__file__), '../../data/config/active_models.json')
        if os.path.exists(config_path):
            with open(config_path, 'r') as file:
                data = json.load(file)
                return data.get('active_model')
        return None
    
# Example usage:
# model_utils = ModelUtils('llama3.2')
# model_utils.check_model_installed()
# ModelUtils.save_chosen_model('llama3.2')
# chosen_model = ModelUtils.load_chosen_model()