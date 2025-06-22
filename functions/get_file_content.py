import os
from google.genai import types

from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    # Get absolute paths for working_directory and target file
    working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Prevent access to files outside the working directory
    if not abs_file_path.startswith(working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        # Open the file in read mode and read up to MAX_CHARS characters
        with open(abs_file_path, "r") as file:
            file_content_string = file.read(MAX_CHARS)
        # If the file content reaches the MAX_CHARS limit, indicate truncation
        if len(file_content_string) == MAX_CHARS:
            file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'  
        return file_content_string
    except Exception as e:
        # Return error message if any exception occurs
        return f'Error: {e}'


schema_get_file_content = types.FunctionDeclaration(
    name='get_file_content',
    description='Reads a limited amount of text from a file at the specified path, constrained to the working directory.',
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            'file_path': types.Schema(
                type=types.Type.STRING,
                description='The path of the file to read from, relative to the working directory.'
            )
        },
        required=['file_path'],
    )
)
