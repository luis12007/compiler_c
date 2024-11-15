from prettytable import PrettyTable

""" ------------------------DICCIONARIOS------------------------------- """
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
    'switch': 'SWITCH',
    'case': 'SWITCHCASE',
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

""" ---------------------------LEXER------------------------------------ """

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

    while i < len(codigo):  # Ensure we don't go out of bounds
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
            while i < len(codigo):  # Added boundary check
                char = codigo[i]  # <--- Edited to reassign `char` within bounds
                if char.isspace() or char == '\n': 
                    break
                if char in especiales.keys():
                    if current_token != "":
                        if current_token in palabras_reservadas.keys():
                            append.append(Token(palabras_reservadas[current_token], current_token, linea))
                        elif current_token.isdigit():
                            append.append(Token("INTVAL", current_token, linea))
                        else:
                            append.append(Token("VARNAME", current_token, linea))
                    append.append(Token(especiales[char], char, linea))
                    current_token = ""
                elif char in aperturas.keys():
                    if current_token != "":
                        if current_token in palabras_reservadas.keys():
                            append.append(Token(palabras_reservadas[current_token], current_token, linea))
                        elif current_token.isdigit():
                            append.append(Token("INTVAL", current_token, linea))
                        else:
                            append.append(Token("VARNAME", current_token, linea))
                    append.append(Token(aperturas[char], char, linea))
                    current_token = ""
                elif char in operadores.keys():
                    if current_token != "":
                        if current_token in palabras_reservadas.keys():
                            append.append(Token(palabras_reservadas[current_token], current_token, linea))
                        elif current_token.isdigit():
                            append.append(Token("INTVAL", current_token, linea))
                        else:
                            append.append(Token("VARNAME", current_token, linea))
                    append.append(Token(operadores[char], char, linea))
                    current_token = ""
                elif char in cerraduras.keys():
                    if current_token != "":
                        if current_token in palabras_reservadas.keys():
                            append.append(Token(palabras_reservadas[current_token], current_token, linea))
                        elif current_token.isdigit():
                            append.append(Token("INTVAL", current_token, linea))
                        else:
                            append.append(Token("VARNAME", current_token, linea))
                    append.append(Token(cerraduras[char], char, linea))
                    current_token = ""
                else:
                    current_token += char

                i += 1  
                if i >= len(codigo): 
                    break

            if current_token != "":
                if current_token in palabras_reservadas.keys():
                    append.append(Token(palabras_reservadas[current_token], current_token, linea))
                elif current_token.isdigit():
                    append.append(Token("INTVAL", current_token, linea))
                else:
                    append.append(Token("VARNAME", current_token, linea))

            for item in append:
                tokens.append(item)

        i += 1 
        current_token = "" 

    imprimir_tabla(tokens)
    return tokens

def imprimir_tabla(tokens):
    # Crear una tabla para los símbolos
    tabla = PrettyTable()
    tabla.field_names = ["Tipo", "Valor", "Línea"]
    for token in tokens:
        tabla.add_row([token.tipo, token.valor, token.linea])
    print(tabla)

""" -------------------------VARIABLES--------------------------------- """
class Var:
    def __init__(self, name, value, tipo, source, linea):
        self.name = name
        self.value = value
        self.tipo = tipo
        self.source = source
        self.linea = linea

    def __repr__(self):
        return f'Var({self.name}, {self.value}, {self.tipo}, {self.source}, Linea: {self.linea})'


def trabajar_variables(tokens):
    variables = []
    i = 0
    length = len(tokens)

    while i < length:
        token = tokens[i]

        # Handle macros (`#define`)
        if token.valor == '#define' and i + 2 < length:
            macro_name = tokens[i + 1].valor  # Macro name
            macro_body = tokens[i + 2].valor  # Macro body
            variables.append(Var(macro_name, macro_body, "Macro", "Macro", token.linea))
            i += 3
            continue

        # Handle function declarations
        if token.valor in palabras_reservadas and tokens[i + 1].tipo == 'VARNAME' and tokens[i + 2].tipo == 'Inicio de paréntesis':
            function_name = tokens[i + 1].valor  # Function name
            return_type = palabras_reservadas[token.valor]  # Function return type
            variables.append(Var(function_name, None, return_type, "Function", token.linea))
            i += 3  # Skip function name and opening parenthesis

            # Gather function parameters
            while i < length and tokens[i].tipo != 'Fin de paréntesis':
                if tokens[i].tipo == 'VARNAME' and i - 1 >= 0 and tokens[i - 1].valor in palabras_reservadas:
                    param_type = palabras_reservadas[tokens[i - 1].valor]
                    param_name = tokens[i].valor
                    variables.append(Var(param_name, None, param_type, f"Function: {function_name}", tokens[i].linea))
                i += 1
            continue

        # Handle variable declarations
        if token.valor in palabras_reservadas and i + 1 < length and tokens[i + 1].tipo == 'VARNAME':
            tipo = palabras_reservadas[token.valor]  # Variable type
            identifier = tokens[i + 1].valor  # Variable name
            i += 2

            # Handle multi-variable declarations
            value = None
            while i < length and tokens[i].tipo != 'Punto y coma':
                if tokens[i].tipo == 'NUMERO':
                    value = tokens[i].valor  # Assign the value to the last declared variable
                elif tokens[i].tipo == 'VARNAME':
                    variables.append(Var(identifier, None, tipo, "Global Variable", token.linea))
                    identifier = tokens[i].valor  # Move to next variable in multi-declaration
                i += 1

            # Assign value to the last variable declared
            variables.append(Var(identifier, value, tipo, "Global Variable", token.linea))
            continue

        i += 1

    # Print and return final results
    imprimir_variables(variables)
    return variables

def imprimir_variables(variables):
        # Crear una tabla para los símbolos
    tabla = PrettyTable()
    tabla.field_names = [ "Tipo","Nombre", "Valor" , "Fuente" , "Línea"]
        # Printing the variables
    for var in variables:
        tabla.add_row([var.tipo,var.name, var.value, var.source, var.linea])
    print(tabla)


