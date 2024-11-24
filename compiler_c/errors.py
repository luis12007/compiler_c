from prettytable import PrettyTable
import re
import time

class Token:
    def __init__(self, tipo, valor, linea):
        self.tipo = tipo  # Token type
        self.valor = valor  # Token value
        self.linea = linea  # Line number

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor}, Linea: {self.linea})"


def parse(tokens, parse_table):
    errr_stack = []
    stack = ['$']
    stack.append('SOURCE')  # Start with the grammar's starting symbol

    tokens.append(Token('$', '$', -1))  # End-of-input marker
    index = 0  # Track the position in the token list

    # Syntax tree data structure
    syntax_tree = []  # List to store the syntax tree nodes

    # Precompile regex patterns from the parse table for only the non-terminals that are regex-based
    regex_patterns = {
        non_terminal: {pattern: re.compile(pattern) for pattern in parse_table[non_terminal] if "[" in pattern}
        for non_terminal in parse_table
    }

    print("\nStarting Parsing Process:")
    print(f"Initial Stack: {stack}\n")
    print(f"Tokens: {tokens}\n")

    while stack:
        print(f"Index: {index}\n")
        top = stack.pop()
        print(f"tOP: {top}\n")

        current_token = tokens[index]
        print(f"current_token: {current_token}\n")
        print(f"Index: {index}\n")
        result = ""
        transition = f"{top} -> ɛ"  # Default transition for empty rules

        # Check if `top` is a regex-based non-terminal
        if top in regex_patterns and regex_patterns[top]:  # Only attempt regex if patterns exist for this non-terminal
            matched = False
            for pattern, compiled_regex in regex_patterns[top].items():
                if compiled_regex.fullmatch(current_token.valor):
                    result = f"Regex match: {current_token.valor}"
                    matched = True
                    print(f"Caso 1\n")
                    index += 1  # Move to the next token
                    syntax_tree.append((top, current_token.valor, "Regex Match"))  # Save to syntax tree
                    break
            if matched:
                continue
            else:
                if top in parse_table:
                    token_key = current_token.valor if current_token.valor in parse_table[top] else current_token.tipo
                    if token_key in parse_table[top]:
                        print(f"Caso 2\n")
                        rule = parse_table[top][token_key]
                        result = f"Rule found: {top} -> {rule}"
                        transition = f"{top} -> {rule}"
                        if rule != ['ɛ']:
                            stack.extend(reversed(rule))
                        syntax_tree.append((top, rule, "Rule Applied"))  # Save rule to syntax tree
                    else:
                        print("error 1")
                        time.sleep(15)
                        tokens, errr_iteration, index = handle_error_non_terminal(top, current_token, index, tokens, parse_table)
                        errr_stack.append(errr_iteration)
                        continue
                    continue
                elif top == current_token.valor:
                    print(f"Caso 3\n")
                    result = f"Terminal match: {top} == {current_token.valor}"
                    transition = f"{top} -> terminal"
                    index += 1  # Move to the next token
                    syntax_tree.append((top, current_token.valor, "Terminal Match"))  # Save to syntax tree
                    continue
                else:
                    tokens, errr_iteration = handle_error_terminal(top, current_token,  index, tokens)
                    errr_stack.append(errr_iteration)
                    stack.append(top)
                    continue

        # Non-regex non-terminal handling
        elif top in parse_table:
            token_key = current_token.valor if current_token.valor in parse_table[top] else current_token.tipo
            print(f"token_key: {token_key}\n")

            if token_key in parse_table[top]:
                print(f"Caso 4\n")
                rule = parse_table[top][token_key]
                result = f"Rule found: {top} -> {rule}"
                transition = f"{top} -> {rule}"
                if rule != ['ɛ']:
                    stack.extend(reversed(rule))
                syntax_tree.append((top, rule, "Rule Applied"))  # Save rule to syntax tree
            else:
                print("error 2")
                time.sleep(15)
                tokens, errr_iteration, index = handle_error_non_terminal(top, current_token, index, tokens, parse_table)
                errr_stack.append(errr_iteration)
                continue
        #Terminal handling
        elif top == current_token.valor:
            result = f"Terminal match: {top} == {current_token.valor}"
            print(f"Caso 5\n")
            transition = f"{top} -> terminal"
            index += 1  # Move to the next token
            syntax_tree.append((top, current_token.valor, "Terminal Match"))  # Save to syntax tree
            continue

        else:
            tokens, errr_iteration = handle_error_terminal(top, current_token,  index, tokens)
            errr_stack.append(errr_iteration)
            stack.append(top)
            continue
        


    if index == len(tokens) and not stack:
        print(len(tokens), index, stack)
        print(errr_stack)
        print("\nParsing completed successfully: Syntax correct.")
        print("Yes")
        return syntax_tree
    else:
        print(len(tokens), index, stack)
        print("\nParsing ended with issues: Stack or token list not empty.")
        print("No")
        print(errr_stack)
        return syntax_tree

"""-----------------------ERROR HANDLER--------------------"""

# New function: Error handler
def handle_error_non_terminal(stack_top, current_tkn, index, tokens, parse_table):
    global errr_stack

    print(f"Error detected with non-terminal: {stack_top} and token: {current_tkn.valor}")
    error_fixed = False

    # Estrategia 1: Omitir tokens no válidos(Contemplado a lo mucho avanzar 1 token adelante(Cumpliendo gramática LL1))
    if current_tkn.valor not in parse_table[stack_top] or current_tkn.tipo not in parse_table[stack_top]:
        if tokens[index + 1].valor in parse_table[stack_top] or tokens[index + 1].tipo in parse_table[stack_top]:
            print(f"Missing token found")
            del tokens[index]
            index += 1
            error_msg = f"There is a token not expected in the line {current_tkn.linea}"
            print(error_msg)
            time.sleep(15)
            return tokens, error_msg, index
        

    # Estrategia 2: Insertar tokens faltantes(Contemplar tokens faltantes(Los cuales podrían ser mucho, reducir número))
    token_key = current_tkn.valor if current_tkn.valor in parse_table[stack_top] else current_tkn.tipo 
    if token_key not in parse_table[stack_top]:
        print(f"Inserting missing token for non-terminal: {stack_top}")
        missing_token = find_missing_token(stack_top, parse_table, current_tkn.linea)  # Función para determinar el token esperado
        error_msg = f"There is a missing token in the line {current_tkn.linea}, please insert the correct element following the sintax"
        print(error_msg)
        time.sleep(15)
        tokens.insert(index, missing_token)
        index += 1
        error_fixed = True
        #Salta a la siguiente iteración sin aumentar el número del elemento
        return tokens, error_msg, index

    # Estrategia 3: Eliminar no terminal mal posicionado
    if not error_fixed:
        print(f"Removing invalid non-terminal: {stack_top} from stack") 
        # Omite el no terminal actual
        
        error_msg = f"Sintax error in the line {current_tkn.linea}, please verify the sintax"
        print(error_msg)
        time.sleep(15)

        
        return tokens, error_msg, index
    #Asegurarse que avance a la siguiente iteración


        
def find_missing_token(non_terminal, parse_table, current_line):
    # Encuentra el primer token válido basado en First(non_terminal)
    if non_terminal in parse_table:
        for key in parse_table[non_terminal]:
            # Retorna el primer token válido en la tabla
            if key != "ɛ":  # Ignoramos las producciones vacías
                return Token(key, key, current_line)  # Simula un token con valor y tipo igual
    return Token("$", "EOF", current_line)  # Token de fin como fallback


def handle_error_terminal(stack_top, current_tkn, index, tokens):
    tokens_esperados = {    
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
        'main': 'Identificador de Funcion Main',
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
        '~': 'Complemento',
        '.': 'Punto',
        ';': 'Punto y coma',
        ',': 'Coma',
        ':': 'Dos puntos',
        '<': 'Menor que',
        '>': 'Mayor que',
        '(': 'Inicio de paréntesis',
        '{': 'Inicio de llave',
        '[': 'Inicio de corchete',
        ')': 'Fin de paréntesis',
        '}': 'Fin de llave',
        ']': 'Fin de corchete',
    }
    #asegurarse que hay next token
    next_token = tokens[index + 1]
    if(next_token.valor == stack_top):
        error_msg = f"There is a token not expected in the line {current_tkn.linea}"
        print(error_msg)

        del tokens[index]
        return tokens, error_msg

        

    
    else: 
        if stack_top in tokens_esperados:
            token_recovery = (Token(stack_top, stack_top, current_tkn.linea))
            tokens.insert(index, token_recovery)
            error_msg = f"Expected token of type {stack_top} in the line {current_tkn.linea}, {current_tkn.valor}, case 1"
            print(error_msg)
            return tokens, error_msg
        elif stack_top == 'VARNAME':
            token_recovery = (Token(stack_top, 'tknvrnm' + stack_top + str(index) +str(current_tkn.linea), current_tkn.linea))
            tokens.insert(index, token_recovery)
            error_msg = f"Expected token of type {stack_top} in the line {current_tkn.linea}, {current_tkn.valor}"
            print(error_msg)
            return tokens, error_msg
        elif stack_top == 'INTVAL':
            token_recovery = (Token(stack_top, 0, current_tkn.linea))
            tokens.insert(index, token_recovery)
            print( error_msg )
            return tokens, error_msg
        else : 
            error_msg = f"Unexpected error in the line {current_tkn.linea}"
            return tokens, error_msg
        
        

            # Este apartado es para variables, por ende necesito verificar como maneja las variables el código.




    
    





"""---------------------------VARIABLES--------------------"""
class Var:
    def __init__(self, name, value, var_type, scope, line, parameters=None):
        self.name = name
        self.value = value
        self.var_type = var_type  
        self.scope = scope
        self.line = line
        self.parameters = parameters

    def __repr__(self):
        return f"Var({self.name}, {self.value}, {self.var_type}, {self.scope}, Line: {self.line}, Parameters: {self.parameters})"

def variable_parse(tokens, parse_table):
    #Variable Things
    current_scope = ["Invalid", "Invalid"]
    variable_declaration = False
    variable_name = ""
    variable_type = ""
    value_flag = False
    variable_value = ""
    variable_line = ""
    variables = []
    define_line = -1
    in_define = False
    #Everything else
    stack = ['$']
    stack.append('SOURCE')  # Start with the grammar's starting symbol
    tokens.append(Token('$', '$', -1))  # End-of-input marker
    index = 0  # Track the position in the token list
    # Precompile regex patterns from the parse table for only the non-terminals that are regex-based
    regex_patterns = {
        non_terminal: {pattern: re.compile(pattern) for pattern in parse_table[non_terminal] if "[" in pattern}
        for non_terminal in parse_table
    }
    while stack:
        top = stack.pop()
        current_token = tokens[index]
        #print(current_scope)
        # Check if `top` is a regex-based non-terminal
        if top in regex_patterns and regex_patterns[top]:  # Only attempt regex if patterns exist for this non-terminal
            matched = False
            for pattern, compiled_regex in regex_patterns[top].items():
                if compiled_regex.fullmatch(current_token.valor):
                    matched = True
                    index += 1  # Move to the next token
                    break
            if matched:
                #print("1")
                if(variable_declaration and not value_flag):
                    variable_name = current_token.valor
                    variable_line = current_token.linea
                elif(value_flag):
                    variable_value += current_token.valor
                continue
            else:
                #print("2")
                if top in parse_table:
                    #print("A")
                    token_key = current_token.valor if current_token.valor in parse_table[top] else current_token.tipo
                    if token_key in parse_table[top]:
                        rule = parse_table[top][token_key]
                        #Declaration setting
                        if(top == "INITSTATEMENT" or top == "FUNCINIT"):
                            variable_declaration = True
                        #Scope checking
                        if(top == "FUNCTION" or top == "VOID_FUNC"):
                            current_scope.append("Function")
                        elif(top == "FORVAR"):
                            current_scope.append("For Loop")
                        elif(top == "IF" or top == "ELSEIF"):
                            current_scope.append("If Statement")
                        elif(top == "SWITCHSTATEMENT"):
                            current_scope.append("Switch Statement")
                        elif(top == "DEFINEBLOCK"):
                            in_define = True
                            define_line = current_token.linea
                        if rule != ['ɛ']:
                            stack.extend(reversed(rule))
                    continue
                elif top == current_token.valor:
                    #print("B")
                    if(top == "=" and variable_declaration):
                        value_flag = True
                    elif(top == "," and variable_declaration):
                        value_flag = False
                    elif(value_flag and top != ";" and top != ")"):
                        variable_value += current_token.valor
                    #Type checking
                    match top :
                        case "int":
                            variable_type = "int"
                            
                        case "float":
                            variable_type = "float"
                            
                        case "char":
                            variable_type = "char"
                            
                        case "string":
                            variable_type = "string"
                            
                        case "double":
                            variable_type = "double"
                            
                        case "long":
                            variable_type = "long"
                            
                        case "short":
                            variable_type = "short"
                            
                    # Variable saving
                    if(current_scope[-1] == "Global" and variable_declaration and current_token.valor == ";"):
                        variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line))
                        variable_declaration = False
                        variable_name = ""
                        variable_type = ""
                        value_flag = False
                        variable_value = ""
                        variable_line = ""
                    elif(current_scope[-1] == "Function" and variable_declaration and current_token.valor == ")"):
                        variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line))
                        variable_declaration = False
                        variable_name = ""
                        variable_type = ""
                        value_flag = False
                        variable_value = ""
                        variable_line = ""
                    elif(current_scope[-1] == "Function" and variable_declaration and current_token.valor == ";"):
                        variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line))
                        variable_declaration = False
                        variable_name = ""
                        variable_type = ""
                        value_flag = False
                        variable_value = ""
                        variable_line = ""
                    elif(current_scope[-1] == "For Loop" and variable_declaration and current_token.valor == ";"):
                        variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line))
                        variable_declaration = False
                        variable_name = ""
                        variable_type = ""
                        value_flag = False
                        variable_value = ""
                        variable_line = ""
                    elif(current_scope[-1] == "If Statement" and variable_declaration and current_token.valor == ";"):
                        variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line))
                        variable_declaration = False
                        variable_name = ""
                        variable_type = ""
                        value_flag = False
                        variable_value = ""
                        variable_line = ""
                    elif(current_scope[-1] == "Switch Statement" and variable_declaration and current_token.valor == ";"):
                        variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line))
                        variable_declaration = False
                        variable_name = ""
                        variable_type = ""
                        value_flag = False
                        variable_value = ""
                        variable_line = ""
                    #Saving without end of init statements
                    elif(variable_declaration and current_token.valor == ","):
                        variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line))
                        variable_name = ""
                        value_flag = False
                        variable_value = ""
                        variable_line = ""
                    
                    if(current_token.valor == "}"):
                        current_scope.pop()
                    elif((in_define and define_line != current_token.linea)):
                        in_define = False
                        current_scope.pop()
                    index += 1  # Move to the next token
                    continue
                else:
                    print(f"Error: No matching regex rule for '{top}' with token '{current_token.valor}'")
                    raise SyntaxError(
                        f"Unexpected token '{current_token.valor}' (type '{current_token.tipo}') at line {current_token.linea}"
                    )
        # Non-regex non-terminal handling
        elif top in parse_table:
            token_key = current_token.valor if current_token.valor in parse_table[top] else current_token.tipo
            if token_key in parse_table[top]:
                #print("A2")
                rule = parse_table[top][token_key]
                #Declaration setting
                if(top == "INITSTATEMENT" or top == "FUNCINIT"):
                    variable_declaration = True
                #Scope checking
                if(top == "FUNCTION" or top == "VOID_FUNC"):
                    current_scope.append("Function")
                elif(top == "FORVAR"):
                    current_scope.append("For Loop")
                elif(top == "IF" or top == "ELSEIF"):
                    current_scope.append("If Statement")
                elif(top == "SWITCHSTATEMENT"):
                    current_scope.append("Switch Statement")
                elif(top == "DEFINEBLOCK"):
                    define_line = current_token.linea
                    in_define = True
                if rule != ['ɛ']:
                    stack.extend(reversed(rule))
            else:
                print(f"Error: No rule for '{top}' with current token '{current_token.valor}' (Type: '{current_token.tipo}')")
                raise SyntaxError(
                    f"Unexpected token '{current_token.valor}' (type '{current_token.tipo}') at line {current_token.linea}"
                )
        elif top == current_token.valor:
            #print("B2")
            if(top == "=" and variable_declaration):
                value_flag = True
            elif(top == "," and variable_declaration):
                value_flag = False
            elif(value_flag and top != ";" and top != ")"):
                variable_value += current_token.valor
            #Type checking
            match top:
                case "int":
                    variable_type = "int"
                    
                case "float":
                    variable_type = "float"
                    
                case "char":
                    variable_type = "char"
                    
                case "string":
                    variable_type = "string"
                    
                case "double":
                    variable_type = "double"
                    
                case "long":
                    variable_type = "long"
                    
                case "short":
                    variable_type = "short"
                    
            # Variable saving
            if(current_scope[-1] == "Global" and variable_declaration and current_token.valor == ";"):
                variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line))
                variable_declaration = False
                variable_name = ""
                variable_type = ""
                value_flag = False
                variable_value = ""
                variable_line = ""
            elif(current_scope[-1] == "Function" and variable_declaration and current_token.valor == ")"):
                variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line))
                variable_declaration = False
                variable_name = ""
                variable_type = ""
                value_flag = False
                variable_value = ""
                variable_line = ""
            elif(current_scope[-1] == "Function" and variable_declaration and current_token.valor == ";"):
                variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line))
                variable_declaration = False
                variable_name = ""
                variable_type = ""
                value_flag = False
                variable_value = ""
                variable_line = ""
            elif(current_scope[-1] == "For Loop" and variable_declaration and current_token.valor == ";"):
                variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line))
                variable_declaration = False
                variable_name = ""
                variable_type = ""
                value_flag = False
                variable_value = ""
                variable_line = ""
            elif(current_scope[-1] == "If Statement" and variable_declaration and current_token.valor == ";"):
                variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line))
                variable_declaration = False
                variable_name = ""
                variable_type = ""
                value_flag = False
                variable_value = ""
                variable_line = ""
            elif(current_scope[-1] == "Switch Statement" and variable_declaration and current_token.valor == ";"):
                variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line))
                variable_declaration = False
                variable_name = ""
                variable_type = ""
                value_flag = False
                variable_value = ""
                variable_line = ""
            #Saving without end of init statements
            elif(variable_declaration and current_token.valor == ","):
                variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line))
                variable_name = ""
                value_flag = False
                variable_value = ""
                variable_line = ""
            if(current_token.valor == "}"):
                current_scope.pop()
            elif((in_define and define_line != current_token.linea)):
                in_define = False
                current_scope.pop()
            index += 1  # Move to the next token
            continue

        else:
            print(f"Error: Expected '{top}', but got '{current_token.valor}' (Type: {current_token.tipo})")
            raise SyntaxError(
                f"Unexpected token '{current_token.valor}' (type '{current_token.tipo}') at line {current_token.linea}"
            )
    return variables

def variable_print(variables):
    # Crear una tabla para los símbolos
    print(variables)
    table = PrettyTable()
    table.field_names = ["Name", "Value", "Type", "Scope", "Line" , "params"]

    # Printing the variables
    for var in variables:
        table.add_row([var.name, var.value, var.var_type, var.scope, var.line, var.parameters])
    print(table)