from agent_loop import agent_loop

iteration = 0
max_iterations = 10
model = "gemini/gemini-1.5-flash"

# Text to fill in the initial input:
# Please list all the files in the folder and provide a summary of what they contain
agent_loop(iteration, max_iterations, model)
