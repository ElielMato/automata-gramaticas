import re
def validate_string(string):
    regular_expression_one = '([a-zA-Z0-9])'
    regular_expression_two = '([a-zA-Z])'
    regular_expression_three = '([a-z])'
    regular_expression_four = '([A-Z])'
    regular_expression_five = '([0-9])'

    if re.search(regular_expression_one, string) is None:
        print(False)
    else:
        print(True)
    
    if re.search(regular_expression_two, string) is None:
        print(False)
    else:
        print(True)
    
    if re.search(regular_expression_three, string) is None:
        print(False)
    else:
        print(True)
    
    if re.search(regular_expression_four, string) is None:
        print(False)
    else:
        print(True)
    
    if re.search(regular_expression_five, string) is None:
        print(False)
    else:
        print(True)
    
    if len(string) < 8:
        print(False)
    else:
        print(True)


