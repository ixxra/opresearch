# -*- coding: utf-8 -*-
class NoLeavingVarException(Exception):
    pass


class NoMatrixPackage(Exception):
    pass


def projection_y(x, y):
    return y

    
def find_leaving_row(matrix):
    first_row = enumerate (matrix[0,:-1])
    idx, val = min(first_row, key=lambda (x, y) : y)
    
    if val >= 0:
        raise NoLeavingVarException
    
    return idx

    
def find_entering_col(matrix, leaving_row):
    m = enumerate(matrix[1:,[leaving_row, -1]].tolist())
    thetas = [(idx, y / x) for idx, (x, y) in m if y / x >= 0]
    idx, val = min(thetas, key=lambda (idx, ratio) : ratio)
    return idx + 1

    
def move_pivot(matrix, i, j):
    pivot = matrix[i, j]
    for r in range(matrix.rows):
        if r == i: 
            continue
            
        mul = -matrix[r, j] / pivot
        
        matrix.zip_row_op(r, i, lambda v, u: v + mul * u)
        
    matrix[i, :] = matrix[i, :] / pivot


def do_step(matrix):
    row = find_leaving_row(matrix)
    col = find_entering_col(matrix, row)
    move_pivot(matrix, row, col)
    return row, col


def print_tableu(matrix, basic_vars=None):
    cols = matrix.cols
    table_fmt = '%s\t' * cols

    if basic_vars is not None:
        total_basics = len(basic_vars)
        total_shadow = cols - total_basics - 1
        
        head_fmt = '\t' + 'x%d \t' * total_basics + 's%d \t' * total_shadow + 'rhs'
        print head_fmt % tuple(range(1, total_basics + 1) + range(1, total_shadow + 1))

        col0 = ['z']
        
        for v in basic_vars:
            if v < total_basics:
                col0.append('x%d' % (v + 1))
            else:
                col0.append('s%d' % (v + 1 - total_basics))
                
        for c, r in zip(col0, matrix.tolist()):
            print c + '\t' + table_fmt % tuple(r)
    
    else:    
        
        for r in matrix.tolist():
            print table_fmt % tuple(r)



class Problem:
    '''
    class Problem: Abstracts a linear programming problem.

    To initialize: 

    Problem(problem)

    where problem is a dictionary like those returned by the parser.parse function.
    '''
    class Objective:
        def __init__(self, objective):
            self.type = objective['type']
            self.coefs = objective['coefs']

        def __repr__(self):
            assert self.type == 'min' or self.type == 'max'

            if self.type == 'min':
                return 'minimize'
            else:
                return 'maximize'

    
    class Restriction:
        def __init__(self, restriction):
            self.coefs = restriction['coefs']
            self.type = restriction['type']
            self.rhs = restriction['rhs']

        def __repr__(self):
            assert self.type in ('leq', 'geq', 'eq')
            
            if self.type == 'leq':
                rel = '<='
            elif self.type == 'geq':
                rel = '>='
            else:
                rel = '='

            return '{c} {r} {v}'.format(
                    c=self.coefs,
                    r=rel,
                    v=self.rhs
                )

    def __init__(self, problem):
        self.vars = problem['vars']
        self.obj = self.Objective(problem['objective'])
        self.restrictions = [self.Restriction(rest) for rest in problem['restrictions']]

    def asmatrix(self):
        '''
        Method asmatrix():

        Returns the matrix representation of the linear problem.

        If sympy is present, the matrix will be a sympy.Matrix.

        In case you don't have sympy installed, it will use a numpy.ndarray.

        If you don't have neither, it will raise a NoMatrixPackage exception.
        '''
        try:
            import sympy as matrix_package
        except ImportError:
            import numpy as matrix_package
        except:
            raise NoMatrixPackage('Either numpy or sympy is required to generate the matrix')
        ncols = len(self.vars) + len(self.restrictions) + 1
        nrows = len(self.restrictions) + 1

        m = matrix_package.zeros(nrows, ncols)

        m[0, :len(self.vars)] = [self.obj.coefs]
        
        if self.obj.type == 'max':
            m[0, :len(self.vars)] *= -1

        m[1:, :len(self.vars)] = [r.coefs for r in self.restrictions]
        m[1:, len(self.vars):-1] = matrix_package.eye(len(self.restrictions))
        
        for idx, r in enumerate(self.restrictions):
            if r.type == 'geq':
                m[idx + 1, len(self.vars) + idx] = -1

            m[idx + 1, -1] = r.rhs
        
        return m


    def from_file(cls, fname):
        from parser import parse
        return cls(parse(open(fname)))

    from_file = classmethod(from_file)

    def __repr__(self):
        _obj = []
        
        for c, v in zip(self.obj.coefs, self.vars):
            _obj.append(' '.join([str(c), v]))
        
        lines = [
            '{t} {obj}'.format(t=self.obj.type, obj=' + '.join(_obj)),
            '',
            'subject to'
            ''
        ]

        for r in self.restrictions:
            _rest = [
                ' + '.join(
                    [str(c) + v for c, v in zip(r.coefs, self.vars)]
                )
            ]

            if r.type == 'leq':
                _rest.append('<=')

            elif r.type == 'geq':
                _rest.append('>=')

            else:
                _rest.append('=')

            _rest.append(str(r.rhs))

            lines.append(' '.join(_rest))

        return '\n'.join(lines)


