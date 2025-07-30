import os, subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not full_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    if file_path.split(".")[-1] != "py":
        return f'Error: "{file_path}" is not a Python file.'
    try:
        completed = subprocess.run(['python3',full_path, *args], timeout=30, stdout=True, stderr=True)
        print(completed)
        result = f"STDOUT: {completed.stdout}\nSTDERR: {completed.stderr}"
        if completed.returncode != 0:
            result += f"Process exited with code {completed.returncode}"
        return result
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the provided python file, relative to the working path",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python script to run, relative to the working directory.",
            ),
        },
    ),
)
