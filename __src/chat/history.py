def chat_history_reset():

    global rotating_history
    rotating_history = []

def chat_history_store(user_input_text = None, vinman_output_text = None):

    assert user_input_text or vinman_output_text, "At least one input must be provided."

    if user_input_text:
        rotating_history.append(f"Input: {user_input_text}")

    if vinman_output_text:
        rotating_history.append(f"Output: {vinman_output_text}")