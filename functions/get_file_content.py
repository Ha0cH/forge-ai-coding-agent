import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        #Building paths
        #Absolute path to the working directory
        working_dir_abs_path = os.path.abspath(working_directory)

        # Absolute path to the target file
        target_file_path = os.path.normpath(os.path.join(working_dir_abs_path, file_path))

        #security validation
        valid_target_file = os.path.commonpath([working_dir_abs_path, target_file_path]) == working_dir_abs_path

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        #check if the file exists
        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(target_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):  # Check if there's more content beyond the max character limit
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return file_content_string
        
    except Exception as e:
        return f"Error: {e}"
    

from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the content of a specified file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to retrieve content from, relative to the working directory",
            ),
        },  required=["file_path"]
    )
)