import os
from google.genai import types


def write_file(working_directory, file_path, content):
    # Get absolute paths for working_directory and target file
    working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Prevent access to files outside the working directory
    if not abs_file_path.startswith(working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        # Ensure the target path exists and that it's not a directory itself
        if not os.path.exists(abs_file_path):
            os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        elif os.path.isdir(abs_file_path):
            return f'Error: "{file_path}" is a directory, not a file'
        
        # Write the content to the file and return a success message
        with open(abs_file_path, 'w') as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        # Return error message if any exception occurs
        return f'Error: {e}'


schema_write_file = types.FunctionDeclaration(
    name='write_file',
    description='Rewrites a file found at the given path with included content, constrained to the working directory. If the file does not exist it creates a new one along with required subfolders',
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            'file_path': types.Schema(
                type=types.Type.STRING,
                description='The path of the file to create or rewrite, relative to the working directory.'
            ),
            'content': types.Schema(
                type=types.Type.STRING,
                description='The content to write into the file'
            )
        },
        required=['file_path', 'content'],
    )
)
