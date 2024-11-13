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
    '=': 'Igual',
    '+': 'suma',
    '-': 'resta',
    '*': 'Multiplicacion',
    '/': 'Division',
    '%': 'Modulo',
    '>': 'Mayor que',
    '<': 'Menor que',
    '&': 'Ampersand',
    '|': 'Pipe',
    '!': 'Negacion',
    '^': 'Potencia',
    '~': 'Complemento'
}

# Dictionary for delimiters
especiales = {
    '.': 'Punto',
    ';': 'Punto y coma',
    ',': 'Coma',
    ':': 'Dos puntos',
    '<': 'Menor que',
    '>': 'Mayor que'
}

aperturas = {
    '(': 'Inicio de paréntesis',
    '{': 'Inicio de llave',
    '[': 'Inicio de corchete',
}

cerraduras = {
    ')': 'Fin de paréntesis',
    '}': 'Fin de llave',
    ']': 'Fin de corchete',
}

class Token:
    def __init__(self, tipo, valor, linea):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor}, Linea: {self.linea})"

def lexer(codigo):
    tokens = []
    current_token = ""
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
        elif char == '/' and i + 1 < len(codigo) and codigo[i + 1] == '/':
            while i < len(codigo) and codigo[i] != '\n':
                i += 1
            continue

        # Handle multi-line comments
        elif char == '/' and i + 1 < len(codigo) and codigo[i + 1] == '*':
            i += 2
            while i < len(codigo) - 1 and not (codigo[i] == '*' and codigo[i + 1] == '/'):
                if codigo[i] == '\n':
                    linea += 1
                i += 1
            i += 2
            continue

        # Ignore whitespace
        elif char.isspace():
            i += 1
            continue

        else:
            append = []
            while(not char.isspace()):
                if(char in especiales.keys()):
                    if current_token != "":
                        append.append(Token("VARNAME", current_token, linea))
                    append.append(Token(especiales[char], char, linea))
                    current_token = ""
                elif(char in aperturas.keys()):
                    if current_token != "":
                        append.append(Token("VARNAME", current_token, linea))
                    append.append(Token(aperturas[char], char, linea))
                    current_token = ""
                elif(char in operadores.keys()):
                    if current_token != "":
                        append.append(Token("VARNAME", current_token, linea))
                    append.append(Token(operadores[char], char, linea))
                    current_token = ""
                elif(char in cerraduras.keys()):
                    if current_token != "":
                        append.append(Token("VARNAME", current_token, linea))
                    append.append(Token(cerraduras[char], char, linea))
                    current_token = ""
                else:
                    current_token += char  
                i += 1
                char = codigo[i]
                if(char == '\n'):
                    linea += 1
            if current_token != "":
                append.append(Token("VARNAME", current_token, linea))
            #print (append)
            for item in append:
                tokens.append(item)        
            i += 1
            current_token = ""

    return tokens


def imprimir_tabla(tokens):
    # Crear una tabla para los símbolos
    tabla = PrettyTable()
    tabla.field_names = ["Tipo", "Valor", "Línea"]
    for token in tokens:
        tabla.add_row([token.tipo, token.valor, token.linea])
    print(tabla)



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


# Leer el archivo example_one.cpp
with open('example_one.c', 'r') as content:
    codigo = content.read()
# Ejecutar el lexer
tokens = lexer(codigo)
# Imprimir la tabla de símbolos
imprimir_tabla(tokens)