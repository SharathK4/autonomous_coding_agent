from langchain.tools import tool
import os
from typing import List, Dict

@tool
def write_files(files_to_write: List[Dict[str, str]]) -> str:
    """
    Writes a list of files to the filesystem. This is the primary tool for 
    creating or updating multiple files in a project at once.
    The input should be a list of dictionaries, where each dictionary has a 
    'path' and 'content' key.
    """
    if not isinstance(files_to_write, list):
        return "Error: Input must be a list of file dictionaries."
    
    for file_info in files_to_write:
        try:
            file_path = file_info['path']
            content = file_info['content']

            directory = os.path.dirname(file_path)
            if directory:
                os.makedirs(directory, exist_ok=True)

            with open(file_path, 'w') as f:
                f.write(content)
        except Exception as e:
            # Return an error for the specific file, but continue with others
            return f"Error writing file {file_info.get('path', 'N/A')}: {e}"
            
    return f"Successfully wrote {len(files_to_write)} files."


@tool
def read_file(file_path: str) -> str:
    """Reads the content of a single file at the given file path."""
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"