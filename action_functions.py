import os

from pydantic import validate_call

from game_types import list_of_tuples_adapter, string_adapter

files_folder = "files_to_analyze/"


def list_files() -> list:
    """List all files in the current directory."""
    return os.listdir(files_folder)


@validate_call
def read_file(file_name: str) -> str:
    """Reads the content of a specific file in the current directory"""
    with open(os.path.join(files_folder, file_name), "r") as f:
        return string_adapter.validate_python(f.read())


@validate_call
def search_in_file(file_name: str, search_term: str) -> list[str]:
    """Search for a term in a file and return matching lines."""
    results = []
    with open(os.path.join(files_folder, file_name), "r") as f:
        for i, line in enumerate(f.readlines()):
            if search_term in line:
                results.append((i + 1, line.strip()))

    return list_of_tuples_adapter.validate_python(results)


@validate_call
def terminate(message: str) -> None:
    """Terminate the agent loop and provide a summary message."""
    print(f"Termination message: {message}")
