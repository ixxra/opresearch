# -*- coding: utf-8 -*-

class NoLeavingVarException(Exception):
    pass


def projection_y(x, y):
    return y

    
def find_leaving_col(matrix):
    first_row = enumerate (matrix[0,:-1])
    idx, val = min(first_row, key=lambda (x, y) : y)
    
    if val >= 0:
        raise NoLeavingVarException
    
    return idx

    
def find_entering_row(matrix, leaving_col):
    thetas = [y / x for x, y in matrix[1:,[leaving_col, -1]].tolist() if y / x >= 0]
    idx, val = min(enumerate(thetas), key=lambda (x, y) : y)
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
    col = find_leaving_col(matrix)
    row = find_entering_row(matrix, col)
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
        
























