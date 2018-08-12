import sys
from .safe_eval import safe_eval
import inspect
import collections


class NotConfigured:
    """
    Used as a dummy value for parameters which have not been configured yet. This should never be exposed to users of
    the library.
    """
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

    #######################################################################
    # If it's handed a function, configure all parameters of the function #
    #######################################################################

    if configurable_function:
        def _wrapper(*args, **kwargs):

            # Get the function spec
            function_spec = inspect.getfullargspec(configurable_function)

            # Create dictionaries for positional and keyword arguments
            function_parameters = {
                "args": collections.OrderedDict((arg, NotConfigured) for arg in function_spec.args),
                "*args": [],
                "kwargs": collections.OrderedDict((kwarg, NotConfigured) for kwarg in function_spec.kwonlyargs)
            }

            # Update positional arguments with default values of the parameters
            if function_spec.defaults:
                values_to_assign = function_spec.defaults[:len(function_parameters["args"])]
                for index, positional_argument in enumerate(reversed(values_to_assign)):
                    variable_to_assign = list(function_parameters["args"].keys())[-index - 1]
                    function_parameters["args"][variable_to_assign] = positional_argument

            # Update positional arguments with passed in values of the parameters
            values_to_assign = args[:len(function_parameters["args"])]
            for index, positional_argument in enumerate(values_to_assign):
                variable_to_assign = list(function_parameters["args"].keys())[index]
                function_parameters["args"][variable_to_assign] = positional_argument

            # Grab arbitrary positional arguments
            function_parameters["*args"] = args[len(function_parameters["args"]):]

            # Update keyword arguments with default values of the parameters
            if function_spec.kwonlydefaults:
                function_parameters["kwargs"].update(function_spec.kwonlydefaults)

            # Update keyword arguments with passed in values of the parameters
            for keyword_parameter, keyword_value in kwargs.items():
                if keyword_parameter in function_parameters["args"]:
                    function_parameters["args"][keyword_parameter] = keyword_value
                else:
                    function_parameters["kwargs"][keyword_parameter] = keyword_value

            # Update with command line values of the parameters
            all_parameters = list(function_parameters["args"].keys()) + list(function_parameters["kwargs"].keys())
            all_parameters = {any_parameter: NotConfigured() for any_parameter in all_parameters}
            all_parameters = configurable(return_type=dict, **all_parameters)
            configured_parameters = {
                configured_parameter: configured_value
                for configured_parameter, configured_value in all_parameters.items()
                if not isinstance(configured_value, NotConfigured)}
            for keyword_parameter, keyword_value in configured_parameters.items():
                if keyword_parameter in function_parameters["args"]:
                    function_parameters["args"][keyword_parameter] = keyword_value
                else:
                    function_parameters["kwargs"][keyword_parameter] = keyword_value

            # Return the result of the function with all parameters
            result = configurable_function(
                *function_parameters["args"].values(),
                *function_parameters["*args"],
                **function_parameters["kwargs"])
            return result
        return _wrapper

    #########################################################################################
    # If there's no function then we're configuring a variable or set of variables manually #
    #########################################################################################

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
