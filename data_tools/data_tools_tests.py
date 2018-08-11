import unittest
from .configurable import configurable
from .safe_eval import safe_eval
import sys


class ConfigurableVariableTests(unittest.TestCase):

    def test_int(self):

        # Test positive values
        sys.argv = ["python_script.py", "--test_int", "123"]
        test_int = configurable(test_int=None)
        self.assertEqual(test_int, 123)

        # Test negative values
        sys.argv = ["python_script.py", "--test_int", "-123"]
        test_int = configurable(test_int=None)
        self.assertEqual(test_int, -123)

    def test_float(self):

        # Test positive values
        sys.argv = ["python_script.py", "--test_float", "123.456"]
        test_float = configurable(test_float=None)
        self.assertEqual(test_float, 123.456)

        # Test negative values
        sys.argv = ["python_script.py", "--test_float", "-123.456"]
        test_float = configurable(test_float=None)
        self.assertEqual(test_float, -123.456)

    def test_str(self):

        # Read in strings with quotes provided
        sys.argv = ["python_script.py", "--test_str", '"123"']
        test_str = configurable(test_str=None)
        self.assertEqual(test_str, "123")
        sys.argv = ["python_script.py", "--test_str", "'123'"]
        test_str = configurable(test_str=None)
        self.assertEqual(test_str, "123")

        # Assume string when no quotes provided
        sys.argv = ["python_script.py", "--test_str", "heck"]
        test_str = configurable(test_str=None)
        self.assertEqual(test_str, "heck")

    def test_none(self):

        # Test None
        sys.argv = ["python_script.py", "--test_none", "None"]
        test_none = configurable(test_none="test")
        self.assertEqual(test_none, None)

    def test_bool(self):

        # Read in False
        sys.argv = ["python_script.py", "--test_bool", "False"]
        test_bool = configurable(test_bool=None)
        self.assertEqual(test_bool, False)

        # Read in True
        sys.argv = ["python_script.py", "--test_bool", "True"]
        test_bool = configurable(test_bool=None)
        self.assertEqual(test_bool, True)

        # If no value provided, assume true
        sys.argv = ["python_script.py", "--test_bool"]
        test_bool = configurable(test_bool=None)
        self.assertEqual(test_bool, True)

    def test_tuple(self):

        # Empty list
        sys.argv = ["python_script.py", "--test_tuple", "()"]
        test_tuple = configurable(test_tuple=None)
        self.assertEqual(test_tuple, ())

        # Non-empty list
        sys.argv = ["python_script.py", "--test_tuple", "(4,5,6)"]
        test_tuple = configurable(test_tuple=None)
        self.assertEqual(test_tuple, (4, 5, 6))

    def test_list(self):

        # Empty list
        sys.argv = ["python_script.py", "--test_list", "[]"]
        test_list = configurable(test_list=None)
        self.assertEqual(test_list, [])

        # Non-empty list
        sys.argv = ["python_script.py", "--test_list", "[4,5,6]"]
        test_list = configurable(test_list=None)
        self.assertEqual(test_list, [4, 5, 6])

    def test_set(self):

        # Empty set
        sys.argv = ["python_script.py", "--test_set", "set()"]
        test_set = configurable(test_set=None)
        self.assertEqual(test_set, set())

        # Non-empty set
        sys.argv = ["python_script.py", "--test_set", "{1,2,3}"]
        test_set = configurable(test_set=None)
        self.assertEqual(test_set, {1, 2, 3})

    def test_dict(self):

        # Empty dict
        sys.argv = ["python_script.py", "--test_dict", "{}"]
        test_dict = configurable(test_dict=None)
        self.assertEqual(test_dict, {})

        # Non-empty dict
        sys.argv = ["python_script.py", "--test_dict", "{1:2}"]
        test_dict = configurable(test_dict=None)
        self.assertEqual(test_dict, {1: 2})

    def test_no_inputs(self):

        # Test one of each of the fundamental data types
        sys.argv = ["python_script.py"]
        test_int, test_float, test_str, test_none, test_bool, test_tuple, test_list, test_set, test_dict = configurable(
            test_int=12,
            test_float=123.456,
            test_str="test",
            test_none=None,
            test_bool=False,
            test_tuple=(1, 2, 3),
            test_list=[1, "two", None],
            test_set={1, 2, 3},
            test_dict={1: "one", "two": 2}
        )
        self.assertEqual(test_int, 12)
        self.assertEqual(test_float, 123.456)
        self.assertEqual(test_str, "test")
        self.assertEqual(test_none, None)
        self.assertEqual(test_bool, False)
        self.assertEqual(test_tuple, (1, 2, 3))
        self.assertEqual(test_list, [1, "two", None])
        self.assertEqual(test_set, {1, 2, 3})
        self.assertEqual(test_dict, {1: "one", "two": 2})

    def test_multiple_inputs(self):

        # Test one of each of the fundamental data types
        sys.argv = [
            "python_script.py",
            "--test_int", "12",
            "--test_float", "123.456",
            "--test_str", "test",
            "--test_none", "None",
            "--test_bool", "False",
            "--test_tuple", "(1, 2, 3)",
            "--test_list", "[1, 'two', None]",
            "--test_set", "{1, 2, 3}",
            "--test_dict", '{1: "one", "two": 2}',
        ]
        test_int, test_float, test_str, test_none, test_bool, test_tuple, test_list, test_set, test_dict = configurable(
            test_int=None,
            test_float=None,
            test_str=None,
            test_none="test",
            test_bool=None,
            test_tuple=None,
            test_list=None,
            test_set=None,
            test_dict=None
        )
        self.assertEqual(test_int, 12)
        self.assertEqual(test_float, 123.456)
        self.assertEqual(test_str, "test")
        self.assertEqual(test_none, None)
        self.assertEqual(test_bool, False)
        self.assertEqual(test_tuple, (1, 2, 3))
        self.assertEqual(test_list, [1, "two", None])
        self.assertEqual(test_set, {1, 2, 3})
        self.assertEqual(test_dict, {1: "one", "two": 2})

    def test_return_type_default(self):

        # No input, no output
        sys.argv = ["python_script.py"]
        test_output = configurable()
        self.assertEqual(test_output, None)

        # One input, one output
        sys.argv = ["python_script.py", "--test_output", "123"]
        test_output = configurable(test_output=None)
        self.assertEqual(type(test_output), int)

        # No input, one output
        sys.argv = ["python_script.py"]
        test_output = configurable(test_output=123)
        self.assertEqual(type(test_output), int)

        # One input, multiple outputs
        sys.argv = ["python_script.py", "--test_output", "123"]
        test_output = configurable(test_output=None, not_given=None)
        self.assertEqual(type(test_output), list)

        # No input, multiple outputs
        sys.argv = ["python_script.py"]
        test_output = configurable(test_output=None, not_given=None)
        self.assertEqual(type(test_output), list)

    def test_return_type_dict(self):

        # No input, no output
        sys.argv = ["python_script.py"]
        test_output = configurable(return_type=dict)
        self.assertEqual(test_output, dict())

        # One input, one output
        sys.argv = ["python_script.py", "--test_output", "123"]
        test_output = configurable(return_type=dict, test_output=None)
        self.assertEqual(test_output, {"test_output": 123})

        # No input, one output
        sys.argv = ["python_script.py"]
        test_output = configurable(return_type=dict, test_output=123)
        self.assertEqual(test_output, {"test_output": 123})

        # One input, multiple outputs
        sys.argv = ["python_script.py", "--test_output", "123"]
        test_output = configurable(return_type=dict, test_output=1, not_given=2)
        self.assertEqual(test_output, {"test_output": 123, "not_given": 2})

        # No input, multiple outputs
        sys.argv = ["python_script.py"]
        test_output = configurable(return_type=dict, test_output=1, not_given=2)
        self.assertEqual(test_output, {"test_output": 1, "not_given": 2})

    def test_return_type_tuple(self):

        # No input, no output
        sys.argv = ["python_script.py"]
        test_output = configurable(return_type=tuple)
        self.assertEqual(test_output, ())

        # One input, one output
        sys.argv = ["python_script.py", "--test_output", "123"]
        test_output = configurable(return_type=tuple, test_output=None)
        self.assertEqual(test_output, (123, ))

        # No input, one output
        sys.argv = ["python_script.py"]
        test_output = configurable(return_type=tuple, test_output=123)
        self.assertEqual(test_output, (123, ))

        # One input, multiple outputs
        sys.argv = ["python_script.py", "--test_output", "123"]
        test_output = configurable(return_type=tuple, test_output=1, not_given=2)
        self.assertEqual(test_output, (123, 2))

        # No input, multiple outputs
        sys.argv = ["python_script.py"]
        test_output = configurable(return_type=tuple, test_output=1, not_given=2)
        self.assertEqual(test_output, (1, 2))

    def test_return_type_list(self):

        # No input, no output
        sys.argv = ["python_script.py"]
        test_output = configurable(return_type=list)
        self.assertEqual(test_output, [])

        # One input, one output
        sys.argv = ["python_script.py", "--test_output", "123"]
        test_output = configurable(return_type=list, test_output=None)
        self.assertEqual(test_output, [123])

        # No input, one output
        sys.argv = ["python_script.py"]
        test_output = configurable(return_type=list, test_output=123)
        self.assertEqual(test_output, [123])

        # One input, multiple outputs
        sys.argv = ["python_script.py", "--test_output", "123"]
        test_output = configurable(return_type=list, test_output=1, not_given=2)
        self.assertEqual(test_output, [123, 2])

        # No input, multiple outputs
        sys.argv = ["python_script.py"]
        test_output = configurable(return_type=list, test_output=1, not_given=2)
        self.assertEqual(test_output, [1, 2])


class ConfigurableFunctionTests(unittest.TestCase):

    def test_no_variables(self):

        # Define function
        @configurable
        def test_func():
            return 10

        # Make sure nothing changed
        sys.argv = ["python_script.py"]
        self.assertEqual(test_func(), 10)

    def test_no_inputs(self):

        # Define function
        @configurable
        def test_func(x, y=10):
            return x, y

        # Make sure nothing changed
        sys.argv = ["python_script.py"]
        self.assertEqual(test_func(1), (1, 10))
        self.assertEqual(test_func(x=1), (1, 10))
        self.assertEqual(test_func(1, 2), (1, 2))
        self.assertEqual(test_func(x=1, y=2), (1, 2))

        # Make sure arbitrary positional args still work
        @configurable
        def test_func(*args, x, y=10):
            return args, x, y

        # Make sure nothing changed
        self.assertEqual(test_func(x=1), ((), 1, 10))
        self.assertEqual(test_func(1, x=1), ((1,), 1, 10))
        self.assertEqual(test_func(1, 2, 3, x=1), ((1, 2, 3), 1, 10))
        self.assertEqual(test_func(x=1, y=2), ((), 1, 2))
        self.assertEqual(test_func(1, x=1, y=2), ((1,), 1, 2))
        self.assertEqual(test_func(1, 2, 3, x=1, y=2), ((1, 2, 3), 1, 2))

    def test_with_inputs_positional(self):

        # Define function
        @configurable
        def test_func(x, y=10):
            return x, y

        # Make sure the variable changed
        sys.argv = ["python_script.py", "--x", "12"]
        self.assertEqual(test_func(1), (12, 10))
        self.assertEqual(test_func(x=1), (12, 10))
        self.assertEqual(test_func(1, 2), (12, 2))
        self.assertEqual(test_func(x=1, y=2), (12, 2))
        self.assertEqual(test_func(y=2), (12, 2))

        # Define function
        @configurable
        def test_func(*args, x, y=10):
            return args, x, y

    def test_with_inputs_keyword(self):

        # Define function
        @configurable
        def test_func(x, y=10):
            return x, y

        # Make sure the variable changed
        sys.argv = ["python_script.py", "--y", "12"]
        self.assertEqual(test_func(1), (1, 12))
        self.assertEqual(test_func(x=1), (1, 12))
        self.assertEqual(test_func(1, 2), (1, 12))
        self.assertEqual(test_func(x=1, y=2), (1, 12))

    def test_with_inputs_mixed(self):

        # Define function
        @configurable
        def test_func(x, y=10):
            return x, y

        # Make sure the variable changed
        sys.argv = ["python_script.py", "--x", "7", "--y", "12"]
        self.assertEqual(test_func(1), (7, 12))
        self.assertEqual(test_func(x=1), (7, 12))
        self.assertEqual(test_func(1, 2), (7, 12))
        self.assertEqual(test_func(x=1, y=2), (7, 12))
        self.assertEqual(test_func(y=2), (7, 12))
        self.assertEqual(test_func(), (7, 12))


class SafeEvalTests(unittest.TestCase):

    def test_int(self):

        # Test literal
        test_value = safe_eval("1")
        self.assertEqual(test_value, 1)

        # Test function
        test_value = safe_eval("int()")
        self.assertEqual(test_value, 0)

    def test_float(self):

        # Test literal
        test_value = safe_eval("1.0")
        self.assertEqual(test_value, 1.0)

        # Test function
        test_value = safe_eval("float()")
        self.assertEqual(test_value, 0.0)

    def test_str(self):

        # Test literal
        test_value = safe_eval("'Heck'")
        self.assertEqual(test_value, "Heck")

        # Test strings without quotes
        test_value = safe_eval("Heck")
        self.assertEqual(test_value, "Heck")

        # Test function
        test_value = safe_eval("str()")
        self.assertEqual(test_value, "")

    def test_none(self):

        # Test literal
        test_value = safe_eval("None")
        self.assertEqual(test_value, None)

    def test_bool(self):

        # Test literal
        test_value = safe_eval("True")
        self.assertEqual(test_value, True)
        test_value = safe_eval("False")
        self.assertEqual(test_value, False)

        # Test function
        test_value = safe_eval("bool()")
        self.assertEqual(test_value, False)

    def test_tuple(self):

        # Test literal
        test_value = safe_eval("(1, 2, 3)")
        self.assertEqual(test_value, (1, 2, 3))

        # Test function
        test_value = safe_eval("tuple()")
        self.assertEqual(test_value, ())

    def test_list(self):

        # Test literal
        test_value = safe_eval("[1, 2, 3]")
        self.assertEqual(test_value, [1, 2, 3])

        # Test function
        test_value = safe_eval("list()")
        self.assertEqual(test_value, [])

    def test_set(self):

        # Test literal
        test_value = safe_eval("{1, 2, 3}")
        self.assertEqual(test_value, {1, 2, 3})

        # Test function
        test_value = safe_eval("set()")
        self.assertEqual(test_value, set())

    def test_dict(self):

        # Test literal
        test_value = safe_eval("{1: 2, 'one': 'two'}")
        self.assertEqual(test_value, {1: 2, 'one': 'two'})

        # Test function
        test_value = safe_eval("dict()")
        self.assertEqual(test_value, {})


if __name__ == '__main__':
    unittest.main()
