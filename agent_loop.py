import json
import traceback

from litellm import _turn_on_debug, completion  # noqa: F401
from pydantic import validate_call
from pydantic_core import to_jsonable_python

import env_config  # noqa: F401
from game_initializer import (
    actions_environment,
    actions_registry,
    file_reading_goal,
    memories,
)
from game_types import (
    ErrorResultType,
    Memory,
)

# _turn_on_debug()  # Uncomment for verbose litellm


@validate_call
def agent_loop(iteration: int, max_iterations: int, model=str):
    while iteration < max_iterations:
        messages = [to_jsonable_python(file_reading_goal)] + [
            to_jsonable_python(msg) for msg in memories.get_memories()
        ]
        tools = actions_registry.get_actions_llm_schema()

        response = completion(
            model=model,
            messages=messages,
            tools=tools,
            max_tokens=1024,
            tool_choice="required",
        )
        print(
            f"\n\nThis is the content of the llm response: ''{response.choices[0].message.content}''\n\n"
        )
        if response.choices[0].message.tool_calls:
            for tool in response.choices[0].message.tool_calls:
                actions = []
                results = []
                tool_name = tool.function.name
                tool_args = json.loads(tool.function.arguments)

                action = actions_registry.get_action(tool_name)
                actions.append(action.to_litellm_schema())

                if tool_name == "terminate":
                    print(f"Termination message: {tool_args['message']}")
                    break
                elif tool_name in actions_registry.get_actions_names():
                    result = actions_environment.execute_actions(action, tool_args)
                else:
                    result = ErrorResultType(
                        tool_executed=False,
                        error=f"Unknown tool: {tool_name}",
                        traceback=traceback.format_exc(),
                    )
                results.append(result.model_dump())
                print(f"Executing: {tool_name} with args {tool_args}")
                print(f"Result: {result}")

            memories.add_memory(
                Memory(
                    role="assistant",
                    content=json.dumps(actions),
                )
            )

            memories.add_memory(
                Memory(
                    role="user",
                    content=json.dumps(results),
                )
            )

        else:
            result = response.choices[0].message.content
            print(f"Response: {result}")
            break

        iteration += 1
        print(f"Iteration number {iteration}...")
