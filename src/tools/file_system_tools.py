from langchain.tools import tool

@tool
def write_file(file_path: str, content: str) -> str:
    """Writes content to a file at the given file path."""
    with open(file_path, 'w') as f:
        f.write(content)
    return f"Successfully wrote to {file_path}"

@tool
def read_file(file_path: str) -> str:
    """Reads the content of a file at the given file path."""
    with open(file_path, 'r') as f:
        return f.read()