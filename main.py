from goal import Goal

file_management_goal = Goal(
    priority = 1,
    name = "file_management",
    description = """Manage files in the current directory by:
        1. Listing files when needed
        2. Reading file contents when needed
        3. Searching within files when information is required
        4. Providing helpful explanations about file contents"""
    )

print("file_management_goal: ", file_management_goal)