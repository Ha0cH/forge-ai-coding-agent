import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        #Building paths
        #Absolute path to the working directory
        working_dir_abs_path = os.path.abspath(working_directory)

        # Absolute path to the target file
        target_file_path = os.path.normpath(os.path.join(working_dir_abs_path, file_path))

        #security validation
        valid_target_file = os.path.commonpath([working_dir_abs_path, target_file_path]) == working_dir_abs_path

        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        #create parent directories if they do not exist
        parent_dir = os.path.dirname(target_file_path)
        os.makedirs(parent_dir, exist_ok=True)
        
        #check if the file path points to an existing directory
        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        #write content to the file (overwriting if it already exists)
        with open(target_file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
     
    except Exception as e:
         return f'Error: {e}'

from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the specified file",
            ),
        }, required=["file_path", "content"]
    )
)