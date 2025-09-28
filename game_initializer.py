from datetime import datetime

import action_functions as act_funcs
from action import Action
from action_registry import ActionRegistry
from environment import Environment
from game_types import (
    ActionParametersModel,
    Memory,
    Properties,
    PropertiesArgument,
    SuccessResultType,
)
from goal import Goal
from memory import Memories

# Initializing goals

# file_management_goal = Goal(
#     priority=1,
#     name="file_management",
#     content="""Manage files in the current directory by:
#         1. Listing files when needed
#         2. Reading file contents when needed
#         3. Searching within files when information is required
#         4. Providing helpful explanations about file contents""",
#     role="system",
# )

file_reading_goal = Goal(
    priority=1,
    content="""
            You are an autonomous AI agent.
                - You MUST always use the available tools to take action.
                - Never ask the user for permission.
                - If files are listed, immediately proceed to read them without confirmation.
                - Continue executing tool calls until the task is completed.
                - Only stop once you call the "terminate" tool with your final summary.
                - Do not output normal text responses unless you are calling a tool.""",
    role="system",
)

# user_task = input("What would you like me to do? ")
user_task = (
    "Please list all the files in the folder and provide a summary of what they contain"
)

# Initializing memory
memories = Memories(
    [
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
        parameters=ActionParametersModel(
            type="object",
            properties=Properties(),
            required=[],
        ),
        terminal=False,
    )
)

actions_registry.register(
    Action(
        name="read_file",
        function=act_funcs.read_file,
        description="Read the contents of a specific file",
        parameters=ActionParametersModel(
            type="object",
            properties=Properties(
                file_name=PropertiesArgument(
                    type="string",
                    description="Name of the file to read",
                )
            ),
            required=["file_name"],
        ),
        terminal=False,
    )
)

actions_registry.register(
    Action(
        name="search_in_file",
        function=act_funcs.search_in_file,
        description="Search for a term in a specific file",
        parameters=ActionParametersModel(
            type="object",
            properties=Properties(
                file_name=PropertiesArgument(
                    type="string",
                    description="Name of the file to search in",
                ),
                search_term=PropertiesArgument(
                    type="string",
                    description="Term to search for",
                ),
            ),
            required=["file_name", "search_term"],
        ),
        terminal=False,
    )
)

actions_registry.register(
    Action(
        name="terminate",
        function=act_funcs.terminate,
        description="Terminate the agent loop and provide a summary message",
        parameters=ActionParametersModel(
            type="object",
            properties=Properties(
                message=PropertiesArgument(
                    type="string",
                    description="Message to display when the agent finishes",
                ),
            ),
            required=["message"],
        ),
        terminal=False,
    )
)

# Initializing environment
actions_environment = Environment()
