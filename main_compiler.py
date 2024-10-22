from lexer_c import lexer, imprimir_tabla

# Leer el archivo example_one.c
with open('example_one.c', 'r') as file:
    codigo = file.read()

# Ejecutar el lexer
tokens = lexer(codigo)

# Imprimir los tokens en una tabla
imprimir_tabla(tokens)
