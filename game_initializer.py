from goal import Goal
from action_registry import ActionRegistry
from action import Action
import action_functions as act_funcs
from memory import Memories
from game_types import Memory

# Initializing goals

file_management_goal = Goal(
    priority=1,
    name="file_management",
    content="""Manage files in the current directory by:
        1. Listing files when needed
        2. Reading file contents when needed
        3. Searching within files when information is required
        4. Providing helpful explanations about file contents""",
    role="system",
)

file_reading_goal = Goal(
    priority=1,
    name="file_reading",
    content="""
    You are an AI agent that can perform tasks by using available tools.
    If a user asks about files, documents, or content, first list the files before reading them.
    When you are done, terminate the conversation by using the "terminate" tool and I will provide
    the results to the user.""",
    role="system",
)

user_task = input("What would you like me to do? ")

# Initializing memory
memories = Memories(
    [
        file_reading_goal,
        Memory(role="user", content=user_task),
    ]
)

# Registering all actions
actions_registry = ActionRegistry()

actions_registry.register(
    Action(
        name="list_files",
        function=act_funcs.list_files,
        description="List all files in the current directory",
        parameters={"type": "object", "properties": {}, "required": []},
        terminal=False,
    )
)

actions_registry.register(
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

actions_registry.register(
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

actions_registry.register(
    Action(
        name="terminate",
        function=act_funcs.terminate,
        description="Terminate the agent loop and provide a summary message",
        parameters={
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "Message to display when the agent finishes",
                },
            },
            "required": ["message"],
        },
        terminal=False,
    )
)
