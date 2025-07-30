import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

def main():
    if len(sys.argv) <= 1:
        sys.exit(1)
    verbose = False
    if "--verbose" in sys.argv:
        verbose = True
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file, 
            schema_write_file 
        ]
    )


    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """   
    user_prompt = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    for run in range(0,20):
        try:
            response = client.models.generate_content(model="gemini-2.0-flash-001",
                                                    contents=messages, 
                                                    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
            print(response.text)
            for candidate in response.candidates:
                messages.append(candidate.content)

            if response.function_calls is not None :
                print(f"Calling function: {response.function_calls[0].name}({response.function_calls[0].args})")
                content = call_function(response.function_calls)
                messages.append(types.Content(role="tool",
                                                parts=[types.Part.from_function_response(name=response.function_calls[0].name,
                                                                                        response={"result": content.parts[0].function_response})]))
            if verbose:
                print(f"-> {content.parts[0].function_response.response}")
        except Exception as e:
            print(e)
    if verbose:
        print(f"User prompt: {user_prompt}\n")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")


def call_function(function_call_part, verbose=False):
    valid_funcs = {"get_files_info": get_files_info,
                    "get_file_content": get_file_content,
                    "run_python_file": run_python_file,
                   "write_file": write_file}
    if verbose:
        print(f"Calling function: {function_call_part[0].name}({function_call_part[0].args})")
    else:
        print(f" - Calling function: {function_call_part[0].name}")
    if function_call_part[0].name in valid_funcs:
        function_result = valid_funcs[function_call_part[0].name]("./calculator", **function_call_part[0].args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part[0].name,
                    response={"result": function_result},
                )
            ],
        )

    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part[0].name ,
                    response={"error": f"Unknown function: {function_call_part[0].name}"},
                )
            ],
        )


if __name__ == "__main__":
    main()
