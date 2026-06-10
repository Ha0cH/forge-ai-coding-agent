import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try: 
        working_dir_abs_path = os.path.abspath(working_directory)

        # Absolute path to the target directory
        target_dir = os.path.normpath(os.path.join(working_dir_abs_path, directory))

        valid_target_dir = os.path.commonpath([working_dir_abs_path, target_dir]) == working_dir_abs_path

        header = (
            "Result for current directory:"
            if directory == "."
            else f"Result for {directory} directory:"
        )

        if not valid_target_dir:
            return header + "\n" + f'Error: Cannot list "{directory}" as it is outside the permitted working directory.'
        
        if not os.path.isdir(target_dir):
            return header + "\n" + f'Error: "{directory}" is not a directory.'
        
        files = []
        
        for item in os.listdir(target_dir):
            file_path = os.path.join(target_dir, item)
            files.append(f"- {item}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}")
        return header + "\n" +"\n".join(files)
        
    except Exception as e:
        return f"Error: {e}"
    

from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

