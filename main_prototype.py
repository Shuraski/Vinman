from src.chat import ModelUtils

def loadmodel(model_name):
    model_utils = ModelUtils(model_name)
    model_utils.check_model_installed()
    ModelUtils.save_chosen_model(model_name)
    chosen_model = ModelUtils.load_chosen_model()

loadmodel('')