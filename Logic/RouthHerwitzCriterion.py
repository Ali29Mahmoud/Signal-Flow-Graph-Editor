import sympy as sp
import numpy as np


def parseCoefficients(eqn):
    coefficients = []
    coeff = ''


    firstChar = eqn[0]
    secondChar = eqn[1]

    if firstChar == 's':
        coeff = '1'
    elif firstChar == '-' and secondChar == 's':
        coeff = '-1'
    elif firstChar == '-' and secondChar != 's':
        coeff = '-' + secondChar
    else:
        coeff = firstChar

    coefficients.append(coeff)


    for i in range(len(eqn)):
        if eqn[i] == 's' and eqn[i + 1] == '^' and (i + 3) < len(eqn):
            if eqn[i + 3] == '+':
                if eqn[i + 4] == 's':
                    coefficients.append('1')
                else:
                    j = i + 4
                    coefficient = ""
                    while j < len(eqn) and eqn[j] != 's':
                        coefficient += eqn[j]
                        j += 1
                    coefficients.append(coefficient)
            else:
                if eqn[i + 4] == 's':
                    coefficients.append('-1')
                else:
                    j = i + 4
                    coefficient = ""
                    while j < len(eqn) and eqn[j] != 's':
                        coefficient += eqn[j]
                        j += 1
                    coefficients.append('-' + coefficient)

    # Get the free term
    index = -1
    freeTerm = ""
    while eqn[index] != 's' and eqn[index] != '+':
        freeTerm += eqn[index]
        index -= 1
    freeTerm = freeTerm[::-1]
    coefficients.append(freeTerm)

    return coefficients


def computeElement(r1c1, r2c1, r1c2, r2c2):
    return r1c2 * r2c1 - r2c2 * r1c1


def computeExpression(original_expression):
    parsed_expr = sp.sympify(str(original_expression))
    simplified_expr = sp.simplify(parsed_expr)
    return simplified_expr


def RouthHurwitz(coefficients):
    degree = len(coefficients) - 1
    row1 = [computeExpression(f's**{degree}')] + [computeExpression(coefficients[i]) for i in range(0, degree + 1, 2)]
    row2 = [computeExpression(f's**{degree - 1}')] + [computeExpression(coefficients[i]) for i in
                                                      range(1, degree + 1, 2)]


    if len(row1) > len(row2):
        row2.append(computeExpression(0))

    cols = len(row1)
    RouthArray = [row1, row2]

    for i in range(degree - 2, -1, -1):
        row = [computeExpression(f's**{i}')]

        for colIndex in range(1, cols):
            r1c1 = RouthArray[-2][1] if len(RouthArray) >= 2 and 1 < cols else 0
            r1c2 = RouthArray[-2][colIndex + 1] if len(RouthArray) >= 2 and colIndex + 1 < cols else 0
            r2c1 = RouthArray[-1][1] if len(RouthArray) >= 1 and 1 < cols else 0
            r2c2 = RouthArray[-1][colIndex + 1] if len(RouthArray) >= 1 and colIndex + 1 < cols else 0

            if r2c1 == 0:
                b = 0
            else:
                b = computeElement(r1c1, r1c2, r2c1, r2c2) / (r2c1)
                b = sp.simplify(b)
            row.append(b)

        RouthArray.append(row)

    return RouthArray


def checkStability(routh_array):
    sign = routh_array[0][1] > 0
    for row in routh_array:
        if sign ^ (row[1] > 0):
            return False
    return True


def checkRHS(roots):
    RHS_roots = [root for root in roots if root > 0]
    return RHS_roots


def checkResult(equation):
    result = ''
    equation_coefficients = parseCoefficients(equation)
    routh_array = RouthHurwitz(equation_coefficients)
    stable = checkStability(routh_array)

    if stable:
        result += "System is stable"
    else:
        result += "System is unstable\n"
        roots = np.roots(equation_coefficients)
        RHS_roots = checkRHS(roots)

        RHS_roots_formatted = [f"{root:.5f}" for root in RHS_roots]
        result += f"{len(RHS_roots)} Roots in the RHS of plane:\n{RHS_roots_formatted}"

    return result
