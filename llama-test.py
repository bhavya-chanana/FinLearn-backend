from huggingface_hub import InferenceClient

# Initialize the client with the model and API token
client = InferenceClient(
    "mistralai/Mistral-7B-Instruct-v0.3",
    token="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",
    )

def chat():
    print("Chatbot: Hello! I'm a chatbot. Type 'exit' to end the conversation.")
    
    while True:
        user_input = input("You: ")
        
        # Exit the loop if the user types 'exit'
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break
        
        # Generate a response from the model
        responses = client.chat_completion(
            messages=[{"role": "user", "content": user_input}],
            max_tokens=1024,
            stream=True,
        )
        
        response_text = ""
        for message in responses:
            response_text += message.choices[0].delta.content
        
        # Print the model's response
        print(f"Chatbot: {response_text}")

if __name__ == "__main__":
    chat()
