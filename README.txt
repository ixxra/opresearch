#Operation Research Toolbox

This is a collection of tools for learning the simplex method. The way I use them is from the terminal with ipython. 

The *simplex method* uses a lot of matrix manipulations, which make it tedious to do on hand. 

**This project is not ready for end users. It is very likely that it will change. Forks welcome**

##Requirements

To use this package you will need sympy, which makes the row operations.

##Installation

Simply run 

```sh
python2 setup.py install
```

It will install a package, opresearh globally. If you want to install somewhere else, for instance, in your `$HOME`:

```sh
python2 setup.py install --prefix=$HOME
```

##Usage

Read the source code ;-) (documentation coming), but as a shorthand, you should do something like this:

```python
from opresearch import simplex
import sympy as sp

matrix = sp.Matrix([
    [-3, -4, -2, 0,  1, 0, -8],
    [ 2,  1,  1, 1,  0, 0,  2],
    [ 3,  4,  2, 0, -1, 1,  8]
    ])

simplex.print_tableu(matrix)
print '\n\n'

while True:
    try:
        row, col = simplex.do_step(matrix)
        print 'entering col:', col
        print 'leaving row:', row
        print '\n'
        simplex.print_tableu(matrix)
        print '\n'

    except simplex.NoLeavingVarException:
        print 'End of simplex'
        break
```
