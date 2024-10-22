from prettytable import PrettyTable

# Definición de los diccionarios
palabras_reservadas = {
    'if': 'Condicional If',
    'else': 'Condicional Else',
    'for': 'Bucle For',
    'while': 'Bucle While',
    'do': 'Bucle Do-While',
    'return': 'Declaracion Return',
    'int': 'Tipo de dato int',
    'float': 'Tipo de dato float',
    'double': 'Tipo de dato double',
    'long': 'Tipo de dato long',
    'short': 'Tipo de dato short',
    'void': 'Tipo de retorno void',
    'char': 'Tipo de dato char',
    'struct': 'Declaracion de Estructura',
    'union': 'Declaracion de Union',
    'enum': 'Declaracion de Enum',
    'typedef': 'Definicion de tipo',
    'switch': 'Condicional Switch',
    'case': 'Condicional Case',
    'break': 'Salida de bucle',
    'continue': 'Continuacion de bucle',
    'default': 'Caso por defecto en Switch',
    'goto': 'Salto de linea Goto',
    'static': 'Modificador Static',
    'extern': 'Modificador Extern',
    'auto': 'Modificador Auto',
    'register': 'Modificador Register',
    'sizeof': 'Operador Sizeof',
    'malloc': 'Funcion de Asignacion de Memoria',
    'free': 'Liberacion de Memoria',
    'const': 'Declaracion Constante',
    'volatile': 'Modificador Volatile',
    'inline': 'Modificador Inline'
}

# Diccionario de los operadores
operadores = {
    '=': 'Asignacion',
    '+': 'Operador suma',
    '-': 'Operador resta',
    '*': 'Multiplicacion',
    '/': 'Division',
    '++': 'Operador incremento',
    '--': 'Operador decremento',
    '%': 'Modulo',
    '==': 'Igualdad',
    '!=': 'Diferente de',
    '>': 'Mayor que',
    '<': 'Menor que',
    '>=': 'Mayor o igual que',
    '<=': 'Menor o igual que',
    '&&': 'AND logico',
    '||': 'OR logico',
    '!': 'Negacion logica',
    '&': 'AND',
    '|': 'OR',
    '^': 'XOR',
    '~': 'Complemento'
}

# Diccionario de delimitadores
delimitadores = {
    '.': 'Punto',
    ';': 'Punto y coma',
    ',': 'Coma',
    ':': 'Dos puntos',
    '(': 'Inicio de paréntesis',
    ')': 'Fin de paréntesis',
    '{': 'Inicio de llave',
    '}': 'Fin de llave',
    '[': 'Inicio de corchete',
    ']': 'Fin de corchete',
    '#': 'Inicio de include'
}

class Token:
    def __init__(self, tipo, valor, linea):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea  # Añadir la línea donde se encontró el token

    def __repr__(self):
        return f'Token({self.tipo}, {self.valor}, {self.linea})'

def lexer(codigo):
    tokens = []
    current_token = ''
    i = 0
    linea = 1
    variables = {}  # Diccionario para almacenar valores de variables

    while i < len(codigo):
        char = codigo[i]

        # Nueva línea
        if char == '\n':
            linea += 1
        # Ignorar comentario de linea 
        if char == '/' and (codigo[i+1] == '/'):
            while i < len(codigo) and codigo[i] != '\n':
                i += 1
            i += 1
            linea +=1
            continue
        # Ignorar comentario multilinea 
        if char == '/' and (codigo[i+1] == '*'): 
            checker = True;  
            i += 2  # Moverse al inicio del comentario
            while i < len(codigo) and (checker == True):
                if codigo[i]=='*' and codigo[i+1] =='/':
                    checker = False
                    i += 2
                    continue
                if codigo[i] == '\n':
                    linea += 1
                i += 1
            continue
            
        # Ignorar espacios en blanco
        if char.isspace():
            i += 1
            continue

        # Identificadores y literales de cadena
        if char.isalpha() or char == '_':
            while i < len(codigo) and (codigo[i].isalnum() or codigo[i] == '_'):
                current_token += codigo[i]
                i += 1
            tipo = palabras_reservadas.get(current_token, 'ID') 
            tokens.append(Token(tipo, current_token, linea))
            current_token = ''
            continue

        if char == '"':  # Literal de cadena
            i += 1  # Moverse más allá de la comilla inicial
            while i < len(codigo) and codigo[i] != '"':
                current_token += codigo[i]
                i += 1
            tokens.append(Token('CADENA', current_token, linea))
            current_token = ''
            i += 1  # Moverse más allá de la comilla final
            continue

        # Números
        if char.isdigit():
            while i < len(codigo) and codigo[i].isdigit():
                current_token += codigo[i]
                i += 1
            tokens.append(Token('NUMERO', current_token, linea))
            current_token = ''
            continue

        # Operadores
        if char in operadores.keys():
            if char == '<' and codigo[i+1] == '<':
                tokens.append(Token('Tuberia de Datos', '<<', linea))
                i += 2
            else:
                tokens.append(Token(operadores[char], char, linea))
                i += 1
            continue
        
        # Delimitadores
        if char in delimitadores.keys():
            tokens.append(Token(delimitadores[char], char, linea))
            i += 1
            continue

        # Manejo de asignaciones
        if char == '=' and i + 1 < len(codigo) and codigo[i + 1] != '=':
            i += 1  # Moverse más allá del '='
            while i < len(codigo) and codigo[i] not in operadores.keys() and codigo[i] not in delimitadores.keys():
                current_token += codigo[i]
                i += 1
            # Asignar el valor a la variable
            variable = tokens[-1].valor  # La última variable registrada
            value = eval(current_token.strip()) if current_token.strip() else '0'  # Evaluar el valor asignado
            variables[variable] = value  # Guardar el valor en el diccionario
            tokens.append(Token('ASIGNACION', f'{variable} = {value}', linea))
            current_token = ''
            continue

        # Manejo de caracteres no reconocidos
        tokens.append(Token('ERROR', char, linea))
        i += 1

    # Agregar valores de variables a la tabla de tokens
    for token in tokens:
        if token.tipo == 'ID' and token.valor in variables:
            token.valor += f' (Valor: {variables[token.valor]})'

    return tokens

def imprimir_tabla(tokens):
    # Crear una tabla para los símbolos
    tabla = PrettyTable()
    tabla.field_names = ["Tipo", "Valor", "Línea"]

    for token in tokens:
        tabla.add_row([token.tipo, token.valor, token.linea])
    print(tabla)


# Leer el archivo example_one.cpp
with open('example_one.c', 'r') as content:
    codigo = content.read()

# Ejecutar el lexer
tokens = lexer(codigo)


# Imprimir la tabla de símbolos
imprimir_tabla(tokens)
