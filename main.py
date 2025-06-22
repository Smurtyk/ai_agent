import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import call_function, available_functions
from config import MAX_ITERATIONS


def main(user_prompt, verbose):
    load_dotenv() # Load the environment variables from .env
    # Read the API key and use it to create a new instance of a Gemini client
    api_key = os.environ.get('GEMINI_API_KEY')
    client = genai.Client(api_key=api_key)

    if verbose:
        print(f'User prompt: {user_prompt}\n')

    # Prepare the message payload for the model, with the user's prompt
    messages = [
        types.Content(role='user', parts=[types.Part(text=user_prompt)]),
    ]

    for i in range(MAX_ITERATIONS):
        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print(f'Final response:\n{final_response}')
                sys.exit(0)
        except Exception as e:
            print(f'Error while generating content: {e}')

    print(f'{MAX_ITERATIONS} (MAX) iterations reached')
    sys.exit(2)
        

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if response.function_calls:    
        function_responses = []
        for fun_call in response.function_calls:
            result = call_function(fun_call, verbose)
            if not result.parts or not result.parts[0].function_response:
                raise Exception('Empty function call result')
            if verbose:
                print(f'-> {result.parts[0].function_response.response['result']}')
            function_responses.append(result.parts[0])

        messages.append(types.Content(role="tool", parts=function_responses))
        return None
    
    if response.text: 
        return response.text

    raise Exception("No function calls or text in response, something went wrong!")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Error: No prompt provided')
        sys.exit(1)
    
    prompt = sys.argv[1]
    verbose = len(sys.argv) > 2 and sys.argv[2] == '--verbose'
    
    main(prompt, verbose)
