import sympy as sp
from sympy import simplify
from sympy.parsing.sympy_parser import parse_expr
import numpy as np

def parseCoefficients(eqn):
    #Getting the first coeffiecient
    firstChar=eqn[0]
    secondChar=eqn[1]
    coeffiecients=[]
    coeff=''
    if firstChar=='s':
        coeff='1'
    elif firstChar=='-' and secondChar=='s':
        coeff='-1'
    elif firstChar=='-' and secondChar!='s':
        coeff='-'+secondChar
    else:
        coeff=firstChar

    coeffiecients.append(coeff)

    #Getting the rest of coefficients except the free term
    for i in range(len(eqn)):
        if(eqn[i]=='s' and eqn[i+1]=='^' and (i+3)<len(eqn)):
            if (eqn[i+3]=='+'):
                if eqn[i+4]=='s':
                    coeffiecients.append('1')
                else:
                    j=i+4
                    coeffiecient=""
                    while(j<len(eqn) and eqn[j]!='s'):
                        coeffiecient+=eqn[j]
                        j+=1
                    coeffiecients.append(coeffiecient)
            else:
                if eqn[i+4]=='s':
                    coeffiecients.append('-1')
                else:
                    j=i+4
                    coeffiecient=""
                    while(j<len(eqn) and eqn[j]!='s'):
                        coeffiecient+=eqn[j]
                        j+=1
                    coeffiecients.append('-'+coeffiecient)
    
    #Get the free term
    index=-1
    freeTerm=""
    while(eqn[index]!='s' and eqn[index]!='+'):
        freeTerm+=eqn[index]
        index-=1
    freeTerm=freeTerm[::-1]
    coeffiecients.append(freeTerm)

    return coeffiecients
        
#Returning the value of new element
def computeElement(r1c1,r2c1,r1c2,r2c2):
    return r1c2*r2c1-r2c2*r1c1


#Simplify expression
def computeExpression(original_expression):
    parsed_expr = parse_expr(str(original_expression))
    simplified_expr = simplify(parsed_expr)
    return simplified_expr

#Computing Routh Hurwitz array
def RouthHurwitz(coefficients):
    degree=len(coefficients)-1
    row1 = []
    expr = computeExpression(f's ** {degree}')
    row1.append(expr)

    for i in range(0,degree+1,2):
        expr = computeExpression(coefficients[i])
        row1.append(expr)

    row2=[]
    expr=computeExpression(f's ** {degree-1}')
    row2.append(expr)

    for i in range(1,degree+1,2):
        expr = computeExpression(coefficients[i])
        row2.append(expr)

    if len(row1) > len(row2):
        row2.append(computeExpression(0))
    
    cols=len(row1)
    RouthArray = [row1, row2]

    rowIndex=2
    for i in range(degree-2,-1,-1):
        row = [0] * (cols)
        row[0] = computeExpression(f's ** {i}')

        for colIndex in range(1, cols):
            r1c1 = RouthArray[rowIndex - 2][1] if rowIndex - 2 >= 0 and 1 < cols else 0
            r1c2 = RouthArray[rowIndex - 2][colIndex + 1] if rowIndex - 2 >= 0 and colIndex + 1 < cols else 0
            r2c1 = RouthArray[rowIndex - 1][1] if rowIndex - 1 >= 0 and 1 < cols else 0
            r2c2 = RouthArray[rowIndex - 1][colIndex + 1] if rowIndex - 1 >= 0 and colIndex + 1 < cols else 0

            b = computeElement(r1c1, r1c2, r2c1, r2c2) / (r2c1)
            b = simplify(b)
            row[colIndex] = b
        
        RouthArray.append(row)
        rowIndex += 1

    return RouthArray


#Check for stability
def checkStability(routh_array):
    # + implies True
    # - implies False
    sign = True if routh_array[0][1] > 0 else False
    for _, row in enumerate(routh_array):
        if sign ^ (row[1] > 0):
            return False
    return True

#Get the roots in the RHS
def checkRHS(roots):
    RHS_roots = []
    for root in roots:
        if (root>0):
            RHS_roots.append(root)
    return RHS_roots

def checkResult(equation):
    result = ''
    equation_coefficients=parseCoefficients(equation)
    routh_array=RouthHurwitz(equation_coefficients)
    stable=checkStability(routh_array)
    if stable:
        result += "System is stable"
    else:
        result += "System is unstable\n"

        roots=np.roots(equation_coefficients)
        RHS_roots=checkRHS(roots)  
        number_of_RHS_roots=len(RHS_roots)  
        result += str(number_of_RHS_roots)+" Roots in the RHS of plane:\n"+str(RHS_roots)

    return result

    
