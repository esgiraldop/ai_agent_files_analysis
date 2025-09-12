import typing

from pydantic import BaseModel, TypeAdapter

from action import Action

# Adapters
string_adapter = TypeAdapter(str)
list_of_tuples_adapter = TypeAdapter(list[tuple[int, str]])
action_adapter = TypeAdapter(Action | None)
action_list_adapter = TypeAdapter(list[Action])


# BaseModels
class Memory(BaseModel):
    role: str
    content: str


class SuccessResultType(BaseModel):
    tool_executed: bool
    result: typing.Any
    timestamp: str


class ErrorResultType(BaseModel):
    tool_executed: bool
    error: str
    traceback: str


class FileName(BaseModel):
    type: typing.Literal["object"]
    description: str


class Properties(BaseModel):
    file_name: FileName


class Parameters(BaseModel):
    type: typing.Literal["string"]
    properties: Properties
    required: list[str]
