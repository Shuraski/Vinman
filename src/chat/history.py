class ChatHistory:
    def __init__(self):
        """Initialize the chat history."""
        self.rotating_history = []

    def reset(self):
        """Reset the chat history."""
        self.rotating_history = []
    
    def store(self, user_input_text=None, vinman_output_text=None):
        """Store a message in the chat history.
        
        Args:
            user_input_text (str): The user's input text.
            vinman_output_text (str): The Vinman's output text."""
        assert user_input_text or vinman_output_text, "At least one input must be provided."

        if user_input_text:
            self.rotating_history.append(f"Input: {user_input_text}")

        if vinman_output_text:
            self.rotating_history.append(f"Output: {vinman_output_text}")

# Example usage:
# chat_history = ChatHistory()
# chat_history.store(user_input_text="Hello", vinman_output_text="Hi there!")
# print(chat_history.rotating_history)