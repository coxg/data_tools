import sys
from .safe_eval import safe_eval


class NotConfigured:
    pass


def configurable(configurable_function=None, return_type=None, **parameters):
    """
    Looks for each parameter in the command line arguments and return them as appropriate.

    For example, if you have the following code:

        max_iterations = configurable(max_iterations=10)

    Then it will search for the parameters -mi or --max_iterations in your command line arguments.
    If no pattern matches, it will use 10 as the default value.

    This can also work as a function decorator. In this case, it will look for each parameter in the command line
    arguments and pass them to the function as appropriate.

    For example, if you have the following code:

        @configurable
        def test_func(var_1, var_2=10):
            return var_1, var_2

    Then it will first search for the parameters -v1, --var_1, -v2, or --var_2 in your command line arguments.
    Any variables provided via command line will be fed to the function each time it is called.
    Any variables without command line arguments will work normally, meaning values provided to the function will
    be passed to it and any defaults will be preserved.

    :param configurable_function:
    If provided, make all parameters to the function configurable. This can be used as a decorator.

    :param return_type:
    Default: None
    The type of the returned values.
    If None, this will return a list if multiple values should be returned.

    :param parameters:
    The parameters to configure.

    :return:
    The command line argument value or the default value.
    If multiple parameters are configured in one call, these will be returned as a tuple by default, but this can
    be specified via the return_type.

    Example usage:
    a, b, c = configurable(a=1, b=2, c=3)
    x = configurable(x="test")
    """

    # If it's handed a function, configure all parameters of the function.
    if configurable_function:
        def _wrapper(*args, **kwargs):

            # Get variables to configure
            function_parameters = configurable_function.__code__.co_varnames
            function_parameters_dict = {
                function_parameter: NotConfigured()
                for function_parameter in function_parameters}

            # Get configuration results from command line
            function_parameters_dict = configurable(return_type=dict, **function_parameters_dict)

            # Loop through each variable, assigning the value if not configured
            min_arg_index_used = len(args)
            for index, function_parameter in enumerate(function_parameters):
                if isinstance(function_parameters_dict[function_parameter], NotConfigured):

                    # If the value is provided in the function call then use that
                    if function_parameter in kwargs:
                        function_parameters_dict[function_parameter] = kwargs[function_parameter]

                    # Else, if it was provided as a positional argument then use that
                    elif index < len(args):
                        function_parameters_dict[function_parameter] = args[index]

                # Make sure the variable is only supplied once
                if isinstance(function_parameters_dict[function_parameter], NotConfigured):
                    del function_parameters_dict[function_parameter]
                elif function_parameter in kwargs:
                    del kwargs[function_parameter]
                if function_parameter in function_parameters_dict:
                    if index < len(args):
                        if index < min_arg_index_used:
                            min_arg_index_used = index

            # Return the result of the function with the configured parameters
            result = configurable_function(*args[:min_arg_index_used], **function_parameters_dict, **kwargs)
            return result
        return _wrapper

    # If there's no function then we're configuring a variable or set of variables manually
    else:

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
                        parameter_value = safe_eval(parameter_value)

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
