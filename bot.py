import requests
import pyautogui
import time
import pyperclip
from hashlib import md5

API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
API_TOKEN = "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"  # Replace with your actual API token
headers = {"Authorization": f"Bearer {API_TOKEN}"}

# Store the last response to prevent repetition
last_response = None
# Store the hash of the last processed chat history to detect changes
last_hash = None

def query_huggingface_api(prompt, max_length=50):
    """
    Send a request to the Hugging Face API with the given prompt, truncating inputs if necessary.
    """
    payload = {
        "inputs": prompt,
        "options": {"use_cache": False},
        "parameters": {
            "max_new_tokens": max_length,
            "truncation": "only_first"  # Add truncation parameter
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()[0]['generated_text']
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return "Error: Unable to generate response."

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

def is_last_message_from_sender(chat_log, sender_name="Sushma:"):
    """
    Check if the last message in the chat log is from the specified sender.
    """
    try:
        messages = chat_log.strip().split("/2025] ")[-1]
        return sender_name in messages
    except Exception as e:
        print(f"Error in checking sender: {e}")
        return False

def main():
    global last_response, last_hash  # Declare global variables

    # Step 1: Open the application at specific coordinates
    pyautogui.click(1064,986) 
    time.sleep(1)

    while True:
        try:
            time.sleep(5)

            # Step 2: Select and copy the chat history
            pyautogui.moveTo(492, 178)
            pyautogui.dragTo(1618,887, duration=1.5, button='left')
            pyautogui.hotkey('command', 'c')  # Use 'command' for Mac
            time.sleep(2)
            chat_history = pyperclip.paste()

            # Keep only the last 5 messages
            truncated_history = truncate_chat_history(chat_history)

            # Check for changes in the chat history
            current_hash = get_chat_hash(truncated_history)
            global last_hash

            # Print the truncated chat history
            print("Truncated Chat History:\n", truncated_history)

            # Here, we check if the last message was from the specified sender and respond
            if is_last_message_from_sender(truncated_history) or current_hash != last_hash:
                last_hash = current_hash  # Update the hash only if we are processing the chat
                
                prompt = (
                    "I am Rohan Pashikanti, a BTech student in Computer Science & Engineering at SR University, currently maintaining a CGPA of 9.62."
                    " I have a strong interest in web development, cloud technologies, data science, and AI. I love building apps that focus on productivity, emotional balance, and well-being, like a self-help app for managing emotions."
                    " I'm passionate about tech, always keeping up with the latest trends, and love exploring how AI can revolutionize industries."
                    " I also enjoy blogging about AI and full-stack projects, with a series called 'AI Chronicles.' In my free time, I enjoy listening to music, watching movies, surfing the internet, and staying updated with tech news."
                    " I’m also working on a startup called 'Airways' and exploring innovative ideas like an automated newsletter generator for SRU. I enjoy sharing my experiences and insights on LinkedIn and aspire to become a top speaker there."
                    " You are from Warangal and a student, and your goal is to engage with others through humor while analyzing chat history and responding in a funny yet informative way."
                    " Output should be the next chat response (text message only).\n"
                    f"Chat History:\n{truncated_history}"
                )

                response = query_huggingface_api(prompt)

                # Process and strip unwanted parts of the response
                processed_response = response.split(']')[-1].split(':', 1)[-1] if ':' in response else response

                # Avoid repeating the same response
                if processed_response == last_response:
                    print("Avoiding repetitive response.")
                    continue

                last_response = processed_response

                # Copy the response to the clipboard
                pyperclip.copy(processed_response)

                # Step 3: Paste the response and send it
                pyautogui.click(584, 915)
                time.sleep(1)
                pyautogui.hotkey('command', 'v')  # Use 'command' for Mac
                time.sleep(1)
                pyautogui.press('enter')
            else:
                print("No new messages. Skipping response generation.")
                
        except KeyboardInterrupt:
            print("Exiting program.")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()