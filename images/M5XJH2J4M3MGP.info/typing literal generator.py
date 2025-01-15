
def typing_literal_generator(*args: typing.Tuple[str]):
    """
    Generate a typing.Literal type from the provided arguments.

    This function takes a variable number of string arguments and generates a
    typing.Literal type that represents the union of those string literals.
    It is a convenient way to create a Literal type without having to manually
    enumerate all the possible values.

    Args:
        *args: A variable number of string arguments to include in the Literal type.

    Returns:
        A typing.Literal type that represents the union of the provided string arguments.
    """
    oneliner = ",".join(f'"{arg}"' for arg in args)

    local = {"typing": typing}
    exec(f"x = typing.Literal[{oneliner}]", local, local)

    return local["x"]

