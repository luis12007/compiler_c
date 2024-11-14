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
                        if(current_token in palabras_reservadas.keys()):
                            append.append(Token(palabras_reservadas[current_token], current_token, linea))
                        elif(current_token.isdigit()):
                            append.append(Token("INTVAL", current_token, linea))
                        else:
                            append.append(Token("VARNAME", current_token, linea))
                    append.append(Token(especiales[char], char, linea))
                    current_token = ""
                elif(char in aperturas.keys()):
                    if current_token != "":
                        if(current_token in palabras_reservadas.keys()):
                            append.append(Token(palabras_reservadas[current_token], current_token, linea))
                        elif(current_token.isdigit()):
                            append.append(Token("INTVAL", current_token, linea))
                        else:
                            append.append(Token("VARNAME", current_token, linea))
                    append.append(Token(aperturas[char], char, linea))
                    current_token = ""
                elif(char in operadores.keys()):
                    if current_token != "":
                        if(current_token in palabras_reservadas.keys()):
                            append.append(Token(palabras_reservadas[current_token], current_token, linea))
                        elif(current_token.isdigit()):
                            append.append(Token("INTVAL", current_token, linea))
                        else:
                            append.append(Token("VARNAME", current_token, linea))
                    append.append(Token(operadores[char], char, linea))
                    current_token = ""
                elif(char in cerraduras.keys()):
                    if current_token != "":
                        if(current_token in palabras_reservadas.keys()):
                            append.append(Token(palabras_reservadas[current_token], current_token, linea))
                        elif(current_token.isdigit()):
                            append.append(Token("INTVAL", current_token, linea))
                        else:
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
                if(current_token in palabras_reservadas.keys()):
                    append.append(Token(palabras_reservadas[current_token], current_token, linea))
                elif(current_token.isdigit()):
                    append.append(Token("INTVAL", current_token, linea))
                else:
                    append.append(Token("VARNAME", current_token, linea))
            #print (append)
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
    def __init__(self, name, value, tipo):
        self.name = name
        self.value = value
        self.tipo = tipo

    def __repr__(self):
        return f'Var({self.name}, {self.value}, {self.tipo})'

def trabajar_variables(tokens):
    variables = {}
    i = 0
    length = len(tokens)

    while i < length:
        # Check if the token is a variable declaration by its value in `palabras_reservadas`
        if tokens[i].valor in palabras_reservadas and i + 1 < length and tokens[i + 1].tipo == 'VARNAME':
            identifier = tokens[i + 1].valor  # Variable name
            tipo = palabras_reservadas[tokens[i].valor]  # Look up type from reserved words

            # Check if this identifier is part of a function declaration
            if i + 2 < length and tokens[i + 2].tipo == 'Inicio de paréntesis':
                i += 3  # Skip the function name and opening parenthesis
                continue

            i += 2  # Move to the token after the variable name

            # Check for assignment after declaration
            if i < length and tokens[i].tipo == 'Igual':
                i += 1  # Move to the token after '='

                values = []
                operators = []

                # Gather tokens until we reach a semicolon
                while i < length and tokens[i].tipo != 'Punto y coma':
                    if tokens[i].tipo == 'VARNAME':
                        # Use the variable's value if assigned before, or assume it as 0 if not yet assigned
                        value = variables.get(tokens[i].valor, {}).get("value", 0)
                        values.append(value)
                    elif tokens[i].tipo == 'NUMERO':
                        values.append(int(tokens[i].valor))  # Numeric literals as integers
                    elif tokens[i].valor in ['+', '-', '*', '/']:
                        operators.append(tokens[i].valor)  # Add operators
                    i += 1

                # Calculate the expression result
                if values:
                    result = values.pop(0)
                    while values and operators:
                        op = operators.pop(0)
                        val = values.pop(0)
                        if op == '+':
                            result += val
                        elif op == '-':
                            result -= val
                        elif op == '*':
                            result *= val
                        elif op == '/':
                            result = int(result / val)  # Integer division for simplicity

                    # Assign the calculated result to the variable with its type
                    variables[identifier] = {"value": result, "tipo": tipo}
            else:
                # If there’s no assignment, initialize with default value (e.g., 0)
                variables[identifier] = {"value": 0, "tipo": tipo}

        i += 1  # Move to the next token

    # Convert dictionary to list of Var objects and print final variable values
    final_variables = [Var(name, details["value"], details["tipo"]) for name, details in variables.items()]
    imprimir_variables(final_variables)
    return final_variables

def imprimir_variables(variables):
        # Crear una tabla para los símbolos
    tabla = PrettyTable()
    tabla.field_names = [ "Tipo","Nombre", "Valor"]
        # Printing the variables
    for var in variables:
        tabla.add_row([var.tipo,var.name, var.value])
    print(tabla)


