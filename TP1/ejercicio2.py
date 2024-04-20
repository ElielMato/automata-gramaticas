import re

def solve(string):
    regular_expression_num = '[0-9]+'
    regular_expression_operators = '[+*]'

    numbers = list(map(int, re.findall(regular_expression_num, string)))

    operators = re.findall(regular_expression_operators, string)
    
    i = 0
    while i < len(operators):
        if operators[i] == '*':
            numbers[i] *= numbers[i+1]
            numbers.pop(i+1)
            operators.pop(i)
        else:
            i += 1

    result = numbers[0]
    for i in range(1, len(numbers)):
        result += numbers[i]

    return result
                
print(solve("2*2*2+32*2"))   


