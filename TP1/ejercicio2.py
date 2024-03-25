import re

def solve(string):
    regular_expression_num = '[0-9]+'
    regular_expression_operators = '[+*]'

    numbers = list(map(int, re.findall(regular_expression_num, string)))
    operators = re.findall(regular_expression_operators, string)

    result = numbers[0]
    for i in range(1, len(numbers)):
        if operators[i-1] == "+":
            result += numbers[i]
        else:
            result *= numbers[i]
    return result
                

print(solve("1+1+1*1*1+1"))   