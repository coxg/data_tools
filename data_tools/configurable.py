import sys
from ast import literal_eval


def configurable(return_type=None, **parameters):
    """
    Looks for each parameter from command line arguments.

    For example, if you have the following code:
    max_iterations = configurable(max_iterations=10)
    Then it will search for the parameters -mi or --max_iterations in your command line arguments.
    If no pattern matches, it will use 10 as the default value.

    :param return_type:
    Default: None
    The type of the returned values.
    If None, this will return a list if multiple values should be returned.

    :param parameters:
    The parameters to configure.

    :return:
    The command line argument value or the default value.
    If multiple parameters are configured in one call, these will be returned as a tuple.

    Example usage:
    a, b, c = configurable(a=1, b=2, c=3)
    x = configurable(x="test")
    """

    # The values to return
    values = []

    # Make command line parameters more easily searchable
    command_line_parameters_dict = {value: index for index, value in enumerate(sys.argv)}

    # Loop through each key word argument, seeing if it was given as a command line parameter
    for parameter, default in parameters.items():

        # Check to see if any valid form of the parameter is given
        parameter_value = default
        parameter_index = command_line_parameters_dict.get("--" + parameter)  # Long form
        if parameter_index is None:
            parameter_index = command_line_parameters_dict.get(
                "-" + "".join([word[0] for word in parameter.split("_")]))  # Short form

        # If the parameter is present then return the value specified via command line
        if parameter_index is not None:

            # If it's the last input then no value was specified, so assume it's a flag
            if len(command_line_parameters_dict) <= parameter_index + 1:
                parameter_value = True

            # Else, get the value specified
            else:
                parameter_value = sys.argv[parameter_index + 1]

                # If this value is also a parameter then no value was specified, so assume it's a flag
                if len(parameter_value) >= 2 and parameter_value[0] == "-" and not parameter_value[1].isdigit():
                    parameter_value = True

                # Else, interpret in the value
                else:

                    # Empty sets do not have a literal, so we need to hard code this
                    if parameter_value == "set()":
                        parameter_value = set()

                    # If they pass in a literal python object then evaluate it
                    try:
                        parameter_value = literal_eval(parameter_value)

                    # If not then they were probably trying to pass in a string
                    except (ValueError, SyntaxError):
                        pass

        # Append the value to our list of values
        values.append(parameter_value)

    # After finding all values, fit them to the specified return type

    # If return type is None (the default) then return just the value if one parameter is specified
    if return_type is None:
        if not values:
            return None
        elif len(values) == 1:
            return values[0]
        else:
            return values

    # If the return type is dict then return a mapping from variable to value
    elif return_type == dict:
        return {
            parameter_name: values[parameter_index]
            for parameter_index, parameter_name in enumerate(parameters.keys())
        }

    # Else, just try to convert the values to the type
    else:
        return return_type(values)
