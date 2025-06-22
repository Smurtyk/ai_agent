import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    # Get absolute paths for working_directory and target file
    working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Prevent access to files outside the working directory
    if not abs_file_path.startswith(working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    # Return error strings if file at given path doesn't exist or if it's not a Pyhton file
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not abs_file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        # Build the command to run the Python file
        commands = ["python", abs_file_path]
        if args:
            commands.extend(args)  # Add any additional arguments

        # Run the command in a subprocess, capturing output and errors
        result = subprocess.run(
            commands,
            cwd=working_directory,      # Set the working directory
            capture_output=True,        # Capture stdout and stderr
            text=True,                  # Return output as string, not bytes
            timeout=30                  # Set a timeout for execution
        )

        output = ''
        if result.stdout:
            output += f'STDOUT: {result.stdout}'  # Append standard output
        if result.stderr:
            output += f'STDERR: {result.stderr}'  # Append standard error
        if result.returncode != 0:
            output += f'Process exited with code {result.returncode}'

        # Return the collected output, or a default message if empty
        return output if output else 'No output produced'
    
    except Exception as e:
        # Catch and return any exceptions that occur during execution
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name='run_python_file',
    description='Runs a Python file, with optional arguments, in a controled enviroment constrained to the working directory, capturing its output and errors.',
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            'file_path': types.Schema(
                type=types.Type.STRING,
                description='The path of the file to execute, relative to the working directory.'
            ),
            'args': types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description='Optional list of arguments to pass to the Python file.'
            )
        },
        required=["file_path"],
    )
)
