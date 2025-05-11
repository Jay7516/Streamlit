from google import genai
from google.genai import types
from utils.load_env import gemini_key
import json
client = genai.Client(api_key=gemini_key)
def generate_text(message,prompt = "",temperature = 0.1):
    response = client.models.generate_content(
        model="gemini-2.0-flash",  
        config=types.GenerateContentConfig(
            system_instruction = prompt,
            #max_output_tokens=1000,
            temperature = temperature),
            #contents=['Why is the sky blue?', 'Why is the cloud white?']
            contents = message,
        
    )
    return response.text
def generate_text_file(message):
    file = client.files.upload(file='mcchicken_data.txt')
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",  
        config=types.GenerateContentConfig(
            #system_instruction="Act like a HYPER person who randomly inserts backshots in their sentences. DON'T MENTION ANY WORDS IN THE QUESTION. Like you can't use any words from the response",
            #max_output_tokens=1000,
            temperature=1.0),
            contents=[message, file]
        
    )
    return response
def process_json_with_gemini(json_data_string, message):
    """
    Sends JSON data along with a custom instruction to Gemini and returns the response.
    """

    prompt = f"""
    Here is some data in JSON format:
    ```json
    {json_data_string}
    ```

    Based only on this data, please:
    {message}
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",  
        config=types.GenerateContentConfig(
            #system_instruction= 
            #max_output_tokens=1000,
            temperature=1.0),
            contents=[prompt]
        
    )
    try:
        print("\n--- Sending Prompt to Gemini ---")
        # print(prompt) # Uncomment to see the full prompt being sent
        print("------------------------------\n")

        return response.text
    except Exception as e:
        print(f"An error occurred while calling the Gemini API: {e}")
        if hasattr(response, 'prompt_feedback'):
            print(f"Prompt Feedback: {response.prompt_feedback}")
        return None

def create_response(message):
    response = generate_text(message)
    #print(response.text)
    #create_sound(response.text)
    #get_voice(response.text)



if __name__ == "__main__":
    with open(r"json\all_data.json", 'r') as f:
        # Load JSON data into a Python dictionary/list
        data_dict = json.load(f)
        # Convert the Python dictionary/list back to a formatted JSON string
        # This is good for including in the prompt so Gemini sees it as JSON
        json_string_for_prompt = json.dumps(data_dict, indent=2)
    while True:
        message = input("Enter your message (or type 'exit' to quit): ").strip()
        if message.lower() == "exit":
            print("Goodbye!")
            #create_sound("Goodbye!")
            exit() 
        gemini_response = process_json_with_gemini(json_string_for_prompt, message)
        print(gemini_response)
