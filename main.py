from goal import Goal
from action_registry import ActionRegistry
from action import Action
import action_functions as act_funcs

file_management_goal = Goal(
    priority=1,
    name="file_management",
    description="""Manage files in the current directory by:
        1. Listing files when needed
        2. Reading file contents when needed
        3. Searching within files when information is required
        4. Providing helpful explanations about file contents""",
)

# Registering all actions
registry = ActionRegistry()

registry.register(
    Action(
        name="list_files",
        function=act_funcs.list_files,
        description="List all files in the current directory",
        parameters={"type": "object", "properties": {}, "required": []},
        terminal=False,
    )
)

registry.register(
    Action(
        name="read_file",
        function=act_funcs.read_file,
        description="Read the contents of a specific file",
        parameters={
            "type": "object",
            "properties": {
                "file_name": {
                    "type": "string",
                    "description": "Name of the file to read",
                }
            },
            "required": ["file_name"],
        },
        terminal=False,
    )
)

registry.register(
    Action(
        name="search_in_file",
        function=act_funcs.search_in_file,
        description="Search for a term in a specific file",
        parameters={
            "type": "object",
            "properties": {
                "file_name": {
                    "type": "string",
                    "description": "Name of the file to search in",
                },
                "search_term": {"type": "string", "description": "Term to search for"},
            },
            "required": ["file_name", "search_term"],
        },
        terminal=False,
    )
)

print(registry)
