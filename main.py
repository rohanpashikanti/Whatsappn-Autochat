import pyautogui
import time
import pyperclip
import requests
from hashlib import md5

# Hugging Face API Configuration
API_URL = "https://api-inference.huggingface.co/models/deepseek-ai/DeepSeek-R1"  # Replace 'gpt2' with your desired model
API_TOKEN = "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"  # Replace with your actual API token

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

# Variables for response control
last_response = None  # Store the last sent response to prevent repetition
last_hash = None  # Store the hash of the last processed chat history


def query_huggingface_api(prompt, max_length=150):
    """
    Send a request to the Hugging Face API with the given prompt.
    """
    payload = {"inputs": prompt, "parameters": {"max_length": max_length}}
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return "Error: Unable to generate response."


def is_last_message_from_sender(chat_log, sender_name="Rohan Pashikanti"):
    """
    Check if the last message in the chat log is from the sender.
    """
    try:
        messages = chat_log.strip().split("/2025] ")[-1]
        return sender_name in messages
    except Exception as e:
        print(f"Error in checking sender: {e}")
        return False


def truncate_chat_history(chat_history, max_messages=5):
    """
    Keep only the last few messages from the chat history.
    """
    messages = chat_history.split("\n")
    return "\n".join(messages[-max_messages:])


def get_chat_hash(chat_history):
    """
    Generate a hash of the chat history to detect changes.
    """
    return md5(chat_history.encode()).hexdigest()


def main():
    global last_response, last_hash

    # Step 1: Open the application (e.g., Chrome at specific coordinates)
    pyautogui.click(857, 738)  # Adjust coordinates as per your screen
    time.sleep(1)

    while True:
        try:
            time.sleep(5)

            # Step 2: Select and copy chat history
            pyautogui.moveTo(450, 120)  # Adjust coordinates as per your screen
            pyautogui.dragTo(1220, 656, duration=1.5, button='left')
            pyautogui.hotkey('command', 'c')  # Use 'ctrl' for Windows
            time.sleep(2)
            chat_history = pyperclip.paste()

            # Truncate chat history
            truncated_history = truncate_chat_history(chat_history, max_messages=5)

            # Check if chat history has changed
            current_hash = get_chat_hash(truncated_history)
            if current_hash == last_hash:
                print("No new messages. Skipping response generation.")
                continue

            last_hash = current_hash  # Update the last processed hash

            # Print the truncated chat history for verification
            print("Truncated Chat History:\n", truncated_history)

            if is_last_message_from_sender(truncated_history):
                # Generate response using Hugging Face API
                prompt = (
                    " am Rohan Pashikanti, a BTech student in Computer Science & Engineering at SR University. I am passionate about web development, cloud, and data science. Here to assist with your questions or chat about tech, music, or movies!"
                    "You are from Warangal and you are a student. You analyze chat history and reply to people in a funny way. "
                    "Output should be the next chat response (text message only).\n"
                    f"Chat History:\n{truncated_history}"
                )
                response = query_huggingface_api(prompt, max_length=100)

                # Prevent repetitive responses
                if response == last_response:
                    print("Avoiding repetitive response.")
                    continue

                last_response = response

                # Copy the response to the clipboard
                pyperclip.copy(response)

                # Step 3: Paste the response and send it
                pyautogui.click(537, 662)  # Adjust coordinates as per your screen
                time.sleep(1)
                pyautogui.hotkey('command', 'v')  # Use 'ctrl' for Windows
                time.sleep(1)
                pyautogui.press('enter')

        except KeyboardInterrupt:
            print("Exiting program.")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()