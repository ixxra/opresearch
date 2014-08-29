"""
   parse something like this:

   vars: x1 x2
   obj: min 3 8
   rests:
   1 1 geq 8
   2 -3 leq 0
   1 2 leq 30
   3 -1 geq 0
   1 0 leq 10
   0 1 geq 9
"""
import re
import sympy as sp


class MalformedData(Exception):
    pass


def _next_line(File):
    for line in File:
        line = line.strip()
        if len(line) > 0:
            return line

    return None


def _numberify(value):
    try:
        value = int(value)
    except ValueError:
        value = float(value)
    except ValueError:
        raise MalformedData('I was expecting a number here')
    
    return value


def _marshall(vars, obj, rests):
    nvars = len(vars)
    obj_type = obj[0]
    obj_coefs = map(_numberify, obj[1:])

    if len(obj_coefs) != nvars:
        raise MalformedData("Variables number doesn't match objective function")
    
    _rests = []

    for rest in rests:
        coefs = map(_numberify, rest[:-2])
        type = rest[-2]
        rhs = _numberify(rest[-1])

        assert(len(coefs) == nvars)

        _rests.append({
            'coefs': coefs,
            'type': type,
            'rhs': rhs
        })

    return { 
            'vars': vars, 
            'objective':  {
                'type': obj_type,
                'coefs': obj_coefs
            },
            'restrictions': _rests
        }


def parse(File):
    """
    parse(File): parses an opened file
    """
    line = _next_line(File)    
    vars = re.match(r'\s*vars:\s*(\w+\d*)\s*(\w+\d*)*\s*', line).groups()

    line = _next_line(File)
    obj = re.match(r'\s*obj:\s*(max|min)\s+(\d+\.*\d*)\s*(\d+\.*\d*)*\s*', line).groups()

    line = _next_line(File)
    
    if line != 'rests:':
        raise MalformedData('Imposible to determine the restrictions')

#    line = _next_line(File)
    
    rests = []

    for line in File:
        rest = re.match(r'\s*([+-]?\d+\.*\d*)\s*([+-]?\d+\.*\d*)*\s*(geq|leq)\s+([+-]?\d+\.*\d*)\s*', line).groups()
        rests.append(rest)

    return _marshall(vars, obj, rests)
