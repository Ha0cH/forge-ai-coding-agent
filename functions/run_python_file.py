import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
     try: 
        #Building paths
        #Absolute path to the working directory
        working_dir_abs_path = os.path.abspath(working_directory)

        # Absolute path to the target file
        target_file_path = os.path.normpath(os.path.join(working_dir_abs_path, file_path))

        #security validation
        valid_target_file = os.path.commonpath([working_dir_abs_path, target_file_path]) == working_dir_abs_path

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        #check if the file path exists and points to a regular file
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        #check if the target file is a python file
        if not target_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file_path]
        #if any additonal arguments are provided, append them to the command
        if args:
            command.extend(args)

        #record the CompletedProcess object returned by subprocess.run()
        result = subprocess.run(command, cwd=working_dir_abs_path, capture_output=True, text=True, timeout=30)

        output_string = ""
        if result.returncode != 0:
            output_string += f"Process exited with code {result.returncode}\n"
        if result.stdout:
            output_string += f"STDOUT:\n{result.stdout}\n"
        if result.stderr:
            output_string += f"STDERR:\n{result.stderr}\n"
        if (not result.stdout) and (not result.stderr):
            output_string += "No output produced\n"
        
        
        return output_string
     except Exception as e:
         return f"Error: executing Python file: {e}"

        
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Arguments to pass to the Python file",
                items=types.Schema(
                    type=types.Type.STRING
                )
            )
        }, required=["file_path"]
    )
)
