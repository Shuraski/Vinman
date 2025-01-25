class TextStyling:

    def text_color(self, choose_color):
        colors = {
            "BLUE": '\033[94m',
            "GREEN": '\033[92m',
            "RED": '\033[91m',
            "YELLOW": '\033[93m',
            "GRAY": '\033[90m',
        }

        if choose_color in colors:
            return colors[choose_color]
        else:
            raise ValueError(f"Invalid color: {choose_color}")

    def text_formatting(self, choose_format):
        formats = {
            "UNDERLINE": '\033[4m',
            "BOLD": '\033[1m',
            "ITALIC": '\033[3m',
        }

        if choose_format in formats:
            return formats[choose_format]
        else:
            raise ValueError(f"Invalid format: {choose_format}")
        
    def reset_text_formatting(self, reset):
        reset_text = {
            "RESET": '\033[0m'
        }

        if reset in reset_text:
            return reset_text[reset]
        else:
            raise ValueError(f"Invalid reset: {reset}")