# -*- coding: utf-8 -*-
import sympy as sp
from opresearch import simplex


class InvalidProblemType(Exception):
    pass


class InvalidRestType(Exception):
    pass


class ProblemVarsMismatch(Exception):
    pass


obj = {'type': 'max', 'coefs': [3, 1, 0]}
rest0 = {'type': '<=', 'coefs': [1, 2, 0], 'rhs': 5}
rest1 = {'type': '<=', 'coefs': [1, 1, -1], 'rhs': 2}
rest2 = {'type': '<=', 'coefs': [7, 3, -5], 'rhs': 20}

problem = {'obj': obj, 'rests': [rest0, rest1, rest2]}

def problem_to_matrix(problem):
    matrix = sp.Matrix([problem['obj']['coefs']])
    rests = problem['rests']
    
    if problem['obj']['type'] == 'max':
        matrix = -1 * matrix
    elif problem['obj']['type'] != 'min':
        raise InvalidProblemType
        
    total_obj_vars = len(matrix)
    
    for r in rests:
        if len(r['coefs']) != total_obj_vars:
            raise ProblemVarsMismatch
        
    matrix = matrix.row_join(sp.Matrix.zeros((1, len(rests) + 1)))

    shadow = sp.Matrix.eye(len(rests))

    for k in range(shadow.rows):
        if rests[k]['type'] == '>=':
            shadow[k,k] = -1
        elif rests[k]['type'] != '<=':
            raise InvalidRestType

    coefs = sp.Matrix([r['coefs'] for r in rests]).row_join(shadow)            
    coefs = coefs.row_join(sp.Matrix([[r['rhs']] for r in rests]))
    
    basics = range(total_obj_vars, total_obj_vars + len(rests))
    return matrix.col_join(coefs), basics
    
    #return matrix


simplex_matrix, basic_vars = problem_to_matrix(problem)

simplex.print_tableu(simplex_matrix, basic_vars)

while True:
    try:
        leaving_col = simplex.find_leaving_col(simplex_matrix)

    except simplex.NoLeavingVarException:
        print '\n\nOptimum found'
        break        
        
    entering_row = simplex.find_entering_row(simplex_matrix, leaving_col)
    simplex.move_pivot(simplex_matrix, entering_row, leaving_col)
    basic_vars[entering_row - 1] = leaving_col
    
    print '\n\n'
    
    simplex.print_tableu(simplex_matrix, basic_vars)









                
    
