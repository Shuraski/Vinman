def text_color(choose_color):
    colors = {
        "BLUE": '\033[94m',
        "GREEN": '\033[92m',
        "RED": '\033[91m',
        "YELLOW": '\033[93m',
        "RESET": '\033[0m'
    }

    if choose_color in colors:
        return colors[choose_color]
    else:
        raise ValueError(f"Invalid color: {choose_color}")