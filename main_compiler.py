from lexer_c import lexer, imprimir_tabla, imprimir_variables, trabajar_variables, Token
from parser import parse

# Leer el archivo example_one.c
with open('example_one.c', 'r') as file:
    codigo = file.read()

# Ejecutar el lexer
tokens = lexer(codigo)

# Obtener valores
variables = trabajar_variables(tokens)

# Imprimir la tabla de símbolos
imprimir_tabla(tokens)

imprimir_variables(variables)

print(parse(tokens, Token))