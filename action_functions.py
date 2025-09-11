import os
from pydantic import validate_call, TypeAdapter

string_adapter = TypeAdapter(str)
list_of_tuples_adapter = TypeAdapter(list[tuple[int, str]])


def list_files() -> list:
    """List all files in the current directory."""
    return os.listdir(".")


@validate_call
def read_file(file_name: str) -> str:
    """Reads the content of a specific file in the current directory"""
    with open(file_name, "r") as f:
        return string_adapter.validate_python(f.read())


@validate_call
def search_in_file(file_name: str, search_term: str) -> list[str]:
    """Search for a term in a file and return matching lines."""
    results = []
    with open(file_name, "r") as f:
        for i, line in enumerate(f.readlines()):
            if search_term in line:
                results.append((i + 1, line.strip()))

    return list_of_tuples_adapter.validate_python(results)
