
import typing

class Task(typing.TypedDict):
    name : str
    at : str
    maxruntime : typing.Union[str, int]
    start : typing.List[dict]
    stop : typing.List[dict]
    expire : typing.Optional[str] 
    skip : typing.Optional[bool]
