import os
from google.genai import types


def get_files_info(working_directory, directory=None):
    # Get absolute paths for working_directory and target directory
    working_directory = os.path.abspath(working_directory)
    if directory:
        directory = os.path.abspath(os.path.join(working_directory, directory))
    else: 
        directory = working_directory

    # Prevent directory traversal outside the working directory
    if not directory.startswith(working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'
    
    try:
        contents = []
        # Iterate through each item in the directory
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            size = os.path.getsize(file_path)  # Get file size in bytes
            is_dir = os.path.isdir(file_path)  # Check if item is a directory
            contents.append(f'- {file}: file_size={size} bytes, is_dir={is_dir}')
        return '\n'.join(contents)
    except Exception as e:
        # Return error message if any exception occurs
        return f'Error: {e}'
    

schema_get_files_info = types.FunctionDeclaration(
    name='get_files_info',
    description='Lists files in the specified directory along with their sizes, constrained to the working directory.',
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            'directory': types.Schema(
                type=types.Type.STRING,
                description='The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.',
            ),
        },
    ),
)
