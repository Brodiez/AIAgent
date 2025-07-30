import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    full_path = os.path.abspath(os.path.join(working_directory, directory))
    named_dir = f"'{directory}'"
    if directory == ".":
        named_dir = "current"
    result = f"Result for {named_dir} directory:\n"
    if not full_path.startswith(os.path.abspath(working_directory)):
        return result + f'    Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(full_path):
        return result + f"    Error: \"{directory}\" is not a directory"
    for item in os.listdir(full_path):
        if item.startswith("__"):
            continue
        full = os.path.abspath(os.path.join(full_path, item))
        result += f" - {item}: file_size={os.path.getsize(full)} bytes, is_dir={os.path.isdir(full)}\n"
    return result

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
