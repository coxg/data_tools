from ast import literal_eval


def safe_eval(code_string):
    """
    Safely creates a python object from a string representing it.

    For example, the code_string "{1: 2, 3: 4}" should return the dictionary {1: 2, 3: 4}.

    To preserve safety, this will not evaluate code snippets, just return single objects expressed as strings.

    :param code_string:
    The string
    :return:
    """

    # Allow people to use the functions to create empty objects
    type_function_from_code_str = {
        "int()": int(),
        "float()": float(),
        "str()": str(),
        "bool()": bool(),
        "tuple()": tuple(),
        "list()": list(),
        "set()": set(),
        "dict()": dict()
    }
    if code_string in type_function_from_code_str:
        return type_function_from_code_str[code_string]

    # If they pass in a literal python object then evaluate it
    try:
        return literal_eval(code_string)

    # If not then they were probably trying to pass in a string
    except (ValueError, SyntaxError):
        return code_string
