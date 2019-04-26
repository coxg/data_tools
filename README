## Where to get it
The source code is currently hosted on GitHub at:
github.com/coxg/data_tools

Binary installers for the latest released version are available at the [Python
package index](https://pypi.org/project/data_tools/).

```sh
pip install pandas
```

## What is it?

The main utility comes from the `configurable` function. This can be called directly or as a function decorator.

### As a function

Looks for each keyword argument in the command line arguments and returns them. If the keyword arguments are not present, the value of the keyword argument will be returned as a default.

For example, given the following `dt_test.py`:
```python
import data_tools as dt  
  
print_variable = dt.configurable(print_variable=1)  
print(print_variable)
```

Running `python dt_test.py` prints `1`, as it uses the default value. 

Running `python dt_test.py -pv 12` prints `12`, as it will search for the abbreviated versions of any variables passed in. 

Running `python dt_test.py --print_variable 123` prints `123`, as it will search for all full matches passed in. 

Running `python dt_test.py --do_not_print 1234` prints `1`, as any non-matching patterns will be ignored.

### As a decorator

Looks for each of the decorated function's arguments in the command line arguments and passes to the function as appropriate.

For example, given the following `dt_test.py`:
```python
import data_tools as dt  
  
  
@dt.configurable  
def print_func(var_1, var_2=2):  
    return var_1, var_2  
  
  
print(print_func(1))
```
Running `python dt_test.py` prints `(1, 2)`, as that is what would happen without the `configurable` decorator.

Running `python dt_test.py -v1 "heck"` prints `('heck', 2)`, as `-v1` is matched to the `var_1` parameter and `"heck"` is read as its value.

Running `python dt_test.py --var_2 "me"` prints `(1, 'me')`, as `--var_2` is matched to the `var_2` parameter and `"me"` is read as its value.

Running `python dt_test.py -v1 'set()' --var_2 '{1:2,3:4}'` prints `(set(), {1: 2, 3: 4})`, as strings are evaluated safely wherever possible. For information on our safe evaluation strategy, see [here](https://github.com/coxg/data_tools/blob/master/data_tools/safe_eval.py).
