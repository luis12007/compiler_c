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
    '#define': 'Definición de Macro',
    'main': 'Identificador de Funcion Main'
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
        #print(linea)
        # Handle new lines
        if char == '\n':
            linea += 1
            #print(linea)
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
                    #print(linea)
                i += 1
            i += 2
            continue

        # Ignore whitespace
        elif char == ' ':
            i += 1
            continue

        else:
            append = []
            while i < len(codigo):  # Added boundary check
                char = codigo[i]  # <--- Edited to reassign `char` within bounds
                if char == ' ' or char == '\n': 
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
            if(char == '\n'):
                linea += 1

        i += 1 
        current_token = "" 

    imprimir_tabla(tokens)
    return tokens

def imprimir_tabla(tokens):
    # Crear una tabla para los símbolos
    tabla = PrettyTable()
    tabla.field_names = ["Tipo", "Valor", "Línea"]
    #print("Tokens encontrados:")
    #print(tokens)
    for token in tokens:
        tabla.add_row([token.tipo, token.valor, token.linea])
    print(tabla)

""" -------------------------VARIABLES--------------------------------- """

"""#TODO: MULTIPLE DECLARATIONS IN A LINE, DECLARATIONS, SEPARATE THE INCREMET WITH THE COMPARASON IN FOR LOOPS AND FOR MISSING
def trabajar_variables(tokens):
    variables = []
    i = 0

    while i < len(tokens):
        token = tokens[i]
        print(f"Processing token: {token}")

        # Process variable declarations (e.g., int x = 1;, float x = 1.2, y = 3.3f;)
        if token.tipo.startswith("Tipo de dato"):
            tipo = token.valor
            print(f"Found type: {tipo}")
            i += 1
            while i < len(tokens) and tokens[i].tipo == "VARNAME":
                name = tokens[i].valor
                i += 1
                value = None
                if i < len(tokens) and tokens[i].tipo == "Igual":
                    i += 1
                    if i < len(tokens):
                        value = tokens[i].valor
                        i += 1
                variables.append(Var(name=name, value=value, tipo=tipo, source="declaration", linea=token.linea))
                print(f"Declared variable: {name} with value {value} and type {tipo}")
                # Handle multiple declarations separated by commas
                while i < len(tokens) and tokens[i].tipo == "Coma":
                    print(f"Handling multiple declarations, current token: {tokens[i]}")
                    i += 1  # Skip the comma
                    if i < len(tokens) and tokens[i].tipo == "VARNAME":
                        name = tokens[i].valor
                        i += 1
                        value = None
                        if i < len(tokens) and tokens[i].tipo == "Igual":
                            i += 1
                            if i < len(tokens):
                                value = tokens[i].valor
                                i += 1
                        variables.append(Var(name=name, value=value, tipo=tipo, source="declaration", linea=token.linea))
                        print(f"Declared variable (comma): {name} with value {value} and type {tipo}")
                # Stop parsing on semicolon
                if i < len(tokens) and tokens[i].tipo == "Punto y coma":
                    print("End of declaration with semicolon")
                    i += 1
                    break

        # Process for loops (e.g., for (int i = 1; i <= n; i++))
        elif token.tipo == "Bucle For":
            print(f"Found for loop at line {token.linea}")
            i += 1
            if i < len(tokens) and tokens[i].tipo == "Inicio de paréntesis":
                i += 1
                # Initialization
                if i < len(tokens) and tokens[i].tipo.startswith("Tipo de dato"):
                    tipo = tokens[i].valor
                    i += 1
                    if i < len(tokens) and tokens[i].tipo == "VARNAME":
                        name = tokens[i].valor
                        i += 1
                        if i < len(tokens) and tokens[i].tipo == "Igual":
                            i += 1
                            if i < len(tokens):
                                init_value = tokens[i].valor
                                i += 1
                                variables.append(Var(name=name, value=init_value, tipo=tipo, source="forloop-init", linea=token.linea))
                                print(f"For loop initialization: {name} = {init_value} ({tipo})")

                # Separate condition and increment
                condition = []
                increment = []
                while i < len(tokens) and tokens[i].tipo != "Fin de paréntesis":
                    print(f"Parsing for loop, current token: {tokens[i]}")
                    if tokens[i].tipo == "Punto y coma":
                        # Add the condition to variables
                        if condition:
                            condition_value = " ".join(condition).strip()
                            variables.append(Var(name="for_condition", value=condition_value, tipo="comparison", source="forloop", linea=token.linea))
                            print(f"For loop condition: {condition_value}")
                        condition = []  # Clear condition for next parse
                        i += 1  # Move to increment part
                        while i < len(tokens) and tokens[i].tipo != "Fin de paréntesis":
                            increment.append(tokens[i].valor)
                            i += 1
                        break
                    condition.append(tokens[i].valor)
                    i += 1
                    
                # Add condition and increment
                if condition:
                    condition_value = " ".join(condition).strip()
                    variables.append(Var(name="for_condition", value=condition_value, tipo="comparison", source="forloop", linea=token.linea))
                    print(f"For loop condition (final): {condition_value}")
                if increment:
                    increment_value = " ".join(increment).strip()
                    variables.append(Var(name="for_increment", value=increment_value, tipo="increment", source="forloop", linea=token.linea))
                    print(f"For loop increment: {increment_value}")

        # Process if statements (e.g., if (x > 10))
        elif token.tipo == "Condicional If":
            print(f"Found if statement at line {token.linea}")
            i += 1
            condition = []
            if i < len(tokens) and tokens[i].tipo == "Inicio de paréntesis":
                i += 1
                while i < len(tokens) and tokens[i].tipo != "Fin de paréntesis":
                    condition.append(tokens[i].valor)
                    i += 1
                condition_value = " ".join(condition).strip()
                variables.append(Var(name="if_condition", value=condition_value, tipo="comparison", source="if_statement", linea=token.linea))
                print(f"If condition: {condition_value}")

        # Process return statements
        elif token.tipo == "Declaracion Return":
            print(f"Found return statement at line {token.linea}")
            i += 1
            if i < len(tokens) and tokens[i].tipo == "VARNAME":
                name = tokens[i].valor
                variables.append(Var(name=name, value=None, tipo="return", source="return", linea=token.linea))
                print(f"Return variable: {name}")

        # Move to next token
        i += 1
        print(f"Next token index: {i}")

    imprimir_variables(variables)
    return variables"""