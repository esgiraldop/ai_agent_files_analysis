import os

def list_files() -> list:
    """List all files in the current directory."""
    return os.listdir('.')

def read_file(file_name: str) -> str:
    """Reads the content of a specific file in the current directory"""
    with open(file_name, 'r') as f:
        return f.read()

def search_in_file(file_name: str, search_term: str) -> list:
    """Search for a term in a file and return matching lines."""
    results = []
    with open(file_name, 'r') as f:
        for i, line in enumerate(f.readlines()):
            if search_term in line:
                results.append((i+1, line.strip()))

    return results