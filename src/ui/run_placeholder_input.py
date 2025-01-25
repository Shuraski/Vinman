from placeholder_input import PlaceholderInput
from text_styling import TextStyling

text_styling = TextStyling()

def main():
    placeholder_input = PlaceholderInput(f'{text_styling.text_color('GRAY')}Test Text{text_styling.reset_text_formatting('RESET')}')
    user_input = placeholder_input.get_input()
    print(f"User input: {user_input}")

if __name__ == "__main__":
    main()