from prettytable import PrettyTable

# Define dictionaries for reserved words, operators, and delimiters
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
    'string': 'Tipo de dato string',
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
    'inline': 'Modificador Inline',
    'scanf': 'Funcion de Lectura',
    'printf': 'Funcion de Escritura',
    'strlen': 'Funcion de Longitud de Cadena',
    'strcpy': 'Funcion de Copia de Cadena',
    '#include': 'Directiva de Inclusion',
    '#define': 'Definición de Macro'
}

# Dictionary for operators
operadores = {
    '=': 'Asignacion',
    '==': 'Igualdad',
    '!=': 'Diferente de',
    '+': 'Operador suma',
    '-': 'Operador resta',
    '*': 'Multiplicacion',
    '/': 'Division',
    '++': 'Operador incremento',
    '--': 'Operador decremento',
    '%': 'Modulo',
    '>': 'Mayor que',
    '<': 'Menor que',
    '>=': 'Mayor o igual que',
    '<=': 'Menor o igual que',
    '&&': 'AND logico',
    '||': 'OR logico',
    '!': 'Negacion logica',
    '&': 'AND bit a bit',
    '|': 'OR bit a bit',
    '^': 'XOR bit a bit',
    '~': 'Complemento',
    '<<': 'Desplazamiento a la izquierda',
    '>>': 'Desplazamiento a la derecha',
    '+=': 'Asignacion suma',
    '-=': 'Asignacion resta',
    '*=': 'Asignacion multiplicacion',
    '/=': 'Asignacion division'
}

# Dictionary for delimiters
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
    '#': 'Inicio de directiva',
    '<': 'Menor que',
    '>': 'Mayor que'
}

import re
class Token:
    def __init__(self, tipo, valor, linea):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor}, Linea: {self.linea})"

def lexer(codigo):
    tokens = []
    current_token = ''
    i = 0
    linea = 1

    while i < len(codigo):
        char = codigo[i]

        # Handle new lines
        if char == '\n':
            linea += 1
            i += 1
            continue

        # Handle single-line comments
        if char == '/' and i + 1 < len(codigo) and codigo[i + 1] == '/':
            while i < len(codigo) and codigo[i] != '\n':
                i += 1
            continue

        # Handle multi-line comments
        if char == '/' and i + 1 < len(codigo) and codigo[i + 1] == '*':
            i += 2
            while i < len(codigo) - 1 and not (codigo[i] == '*' and codigo[i + 1] == '/'):
                if codigo[i] == '\n':
                    linea += 1
                i += 1
            i += 2
            continue

        # Ignore whitespace
        if char.isspace():
            i += 1
            continue

        
        # Handle #include directive with <...> pattern for libraries
        if codigo[i:i + 8] == '#include':
            tokens.append(Token('Directiva de Inclusion', '#include', linea))
            i += 9  # Move past '#include'

            # Capture the content within <...> as a single ID token
            if i < len(codigo) and codigo[i] == '<':
                tokens.append(Token('Menor que', '<', linea))
                i += 1  # Move past '<'
                header_name = ''

                while i < len(codigo) and codigo[i] != '>':
                    
                    header_name += codigo[i]
                    i += 1

                if i < len(codigo) and codigo[i] == '>':
                    # Include '<' and '>' around the ID for full pattern representation
                    tokens.append(Token( f'{header_name}' , 'VARNAME',linea))
                    i += 1  # Move past '>'
                tokens.append(Token('Mayor que', '>', linea))
            continue


        # Handle keywords, VARNAME, and general ID
        if char.isalpha() or char == '_':
            while i < len(codigo) and (codigo[i].isalnum() or codigo[i] == '_'):
                current_token += codigo[i]
                i += 1

            if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*\.[a-zA-Z0-9]+$", current_token):
                tokens.append(Token('ID' ,current_token, linea))  # Specific library names, etc.
            else:
                if current_token in palabras_reservadas:
                    tokens.append(Token("VARNAME", current_token, linea))
                else:
                    tokens.append(Token(current_token, 'VARNAME', linea))  # General variable names
            current_token = ''
            continue

        # Handle multi-character operators (==, !=, etc.)
        if char in operadores.keys():
            next_char = codigo[i + 1] if i + 1 < len(codigo) else ''
            if char + next_char in operadores:
                tokens.append(Token(operadores[char + next_char], char + next_char, linea))
                i += 2
            else:
                tokens.append(Token(operadores[char], char, linea))
                i += 1
            continue

        # Handle delimiters
        if char in delimitadores:
            tokens.append(Token(delimitadores[char], char, linea))
            i += 1
            continue

        # Handle numbers
        if char.isdigit():
            while i < len(codigo) and codigo[i].isdigit():
                current_token += codigo[i]
                i += 1
            tokens.append(Token('NUMERO', current_token, linea))
            current_token = ''
            continue

        # Handle unrecognized characters as errors
        tokens.append(Token('ERROR', char, linea))
        i += 1

    return tokens


def imprimir_tabla(tokens):
    # Crear una tabla para los símbolos
    tabla = PrettyTable()
    tabla.field_names = ["Tipo", "Valor", "Línea"]
    for token in tokens:
        tabla.add_row([token.tipo, token.valor, token.linea])
    print(tabla)



""" Working var table """
class Var:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f'Var({self.name}, {self.value})'
    


 #TODO: change it
def trabajar_variables(tokens):
    length = len(tokens)
    variables = {}
    for i in range(length - 1):
        if(tokens[i].tipo == 'ID' and tokens[i+1].tipo == 'Asignacion'):
            counter = 2
            identifier = tokens[i].valor
            operators = []
            values = []
            while(tokens[i+counter].tipo != 'Punto y coma'):
                if(tokens[i+counter].tipo == 'ID'):
                    values.append(tokens[i+counter].valor)
                if(tokens[i+counter].tipo == 'NUMERO'):
                    values.append(int(tokens[i+counter].valor))
                if(tokens[i+counter].tipo == 'Multiplicacion' or tokens[i+counter].tipo == 'Operador suma' or tokens[i+counter].tipo == 'Operador resta'
                    or tokens[i+counter].tipo == 'Division'):
                    operators.append(tokens[i+counter].valor)
                counter += 1
            val = 0
            t2 = values.pop()
            if(isinstance(t2, str)):
                if(t2 in variables):
                    val = int(variables[t2])
            else:
                val = t2
            while(len(values) > 0):
                op = operators.pop()
                val2 = 1
                t2 = values.pop()
                if(isinstance(t2, str)):
                    if(t2 in variables):
                            val2 = int(variables[t2])
                else:
                    val2 = t2
                if(op == '-'):
                    val -= val2
                if(op == '+'):
                    val += val2
                if(op == '*'):
                    val *= val2
                if(op == '/'):
                    val /= val2
            variables[identifier] = val
    li = []
    for i, j in variables.items():
        li.append(Var(i, j))
    return li

def imprimir_variables(variables):
        # Crear una tabla para los símbolos
    tabla = PrettyTable()
    tabla.field_names = ["Nombre", "Valor"]

    for var in variables:
        tabla.add_row([var.name, var.value])
    print(tabla)


