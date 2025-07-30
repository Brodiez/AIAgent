import os
from google.genai import types

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):

    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not full_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    result = ""
    with open(full_path, "r") as file:
        file_content = file.read(MAX_CHARS)
    result = file_content
    if os.path.getsize(full_path) > MAX_CHARS:
        result += f'...File "{file_path}" truncated at 10000 characters'
    return result

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Prints out the content from a provided file, limited to 10000 characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to print from, relative to the working directory.",
            ),
        },
    ),
)
