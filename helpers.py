import requests

def chat_with_api(message, api_key):
    url = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
    headers = {"Authorization": f"Bearer {api_key}"}

    # Prepare the payload
    payload = {
        "inputs": message,
        "options": {
            "use_cache": False
        },
        "parameters": {
            "max_new_tokens": 50,  
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    
    # Check for errors
    if response.status_code != 200:
        print("Error:", data)
        return "I am currently having issues retrieving a response. Please try again later."
    
    # Extract the generated text
    generated_text = data[0]['generated_text']
    return generated_text

# Main interaction loop
if __name__ == "__main__":
    api_key = "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"  # Replace with your actual API key
    print("AI: Hello! How can I help you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("AI: Goodbye!")
            break
        response = chat_with_api(user_input, api_key)
        print(f"AI: {response}")