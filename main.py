import os
import sys
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from functions.call_functions import available_functions, call_function
from config import MAX_ITERATIONS

def main():
    print("Hello from Forge!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY environment variable is not set")

    parser = argparse.ArgumentParser(description="Forge: An AI coding assistant.")
    parser.add_argument("user_prompt", type=str, help="The prompt to send to the Gemini API")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")


    args = parser.parse_args()

    client = genai.Client(api_key=api_key)
    prompt = args.user_prompt
    
    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]
    for _ in range(MAX_ITERATIONS): #feedback loop with a max of 20 iterations to prevent infinite loops
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt, temperature=0)
        )

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if response.usage_metadata is not None:
            prompt_tokens = response.usage_metadata.prompt_token_count
            response_tokens = response.usage_metadata.candidates_token_count
        else:
            raise RuntimeError("Response does not contain usage metadata. Likely an API request error occurred.")

        if args.verbose:
            print(f"User prompt: {prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
        
        function_results = []
        if response.function_calls:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, args.verbose)
                if not function_call_result.parts:
                    raise Exception("No parts returned")
                if function_call_result.parts[0].function_response is None:
                    raise Exception("No function response returned")
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception("No response returned")
                function_results.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                
            messages.append(
                types.Content(
                    role="user",
                    parts=function_results
                )
            )
                
        else:
            print(f"Response:\n{response.text}")
            break
    
    else:
        print(
            f"Error: Agent exceeded maximum iterations {MAX_ITERATIONS} without reaching a final response."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
