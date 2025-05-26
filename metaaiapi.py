from meta_ai_api import MetaAI

ai = MetaAI()

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Goodbye!")
        break
    response = ai.prompt(message=user_input)
    
    if isinstance(response, dict):
        # Assuming the response is a dictionary with a 'message' key
        cleaned_response = str(response.get('message', ''))
    else:
        cleaned_response = str(response).replace("\n"," ")
    
    cleaned_response = cleaned_response.replace("source:", "").replace("media:", "").strip()
    print("AI:", cleaned_response)
