import ast

user_value = input('Expression: ')
print(ast.literal_eval(user_value))
