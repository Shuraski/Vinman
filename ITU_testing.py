from src.ui.itu_main_menu import IntegratedTerminalUI, text_color
from src.chat.model_utils import ModelUtils

itu = IntegratedTerminalUI()

if itu.run() == 1:
    ModelUtils