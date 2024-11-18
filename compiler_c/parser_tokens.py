from prettytable import PrettyTable
import re

class Token:
    def __init__(self, tipo, valor, linea):
        self.tipo = tipo  # Token type
        self.valor = valor  # Token value
        self.linea = linea  # Line number

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor}, Linea: {self.linea})"

def draw_box(content):
    """Helper function to draw a box with content."""
    lines = content.split("\n")
    width = max(len(line) for line in lines)
    border = "+" + "-" * (width + 2) + "+"
    result = [border]
    for line in lines:
        result.append(f"| {line.ljust(width)} |")
    result.append(border)
    return "\n".join(result)

def is_terminal(element):
    """Determine if the given grammar element is a terminal."""
    return not element.isupper()

def display_syntax_tree(stack, token, result, transition):
    """Display the syntax tree representation with transitions and token details."""
    print("\nCurrent Syntax Tree:")
    for i, element in enumerate(reversed(stack)):
        element_type = "Terminal" if is_terminal(element) else "Non-Terminal"
        box_content = (
            f"{element_type}: {element}\nToken: {token.valor} ({token.tipo})\nResult: {result}\nTransition: {transition}"
        )
        print(draw_box(box_content))
        if i != len(stack) - 1:
            print("    |")
            print("    |")
            print("    |")

def parse(tokens, parse_table):
    stack = ['$']
    stack.append('SOURCE')  # Start with the grammar's starting symbol

    tokens.append(Token('$', '$', -1))  # End-of-input marker
    index = 0  # Track the position in the token list

    # Precompile regex patterns from the parse table for only the non-terminals that are regex-based
    regex_patterns = {
        non_terminal: {pattern: re.compile(pattern) for pattern in parse_table[non_terminal] if "[" in pattern}
        for non_terminal in parse_table
    }

    print("\nStarting Parsing Process:")
    print(f"Initial Stack: {stack}\n")
    print(f"Tokens: {tokens}\n")

    while stack:
        top = stack.pop()
        current_token = tokens[index]

        result = ""
        transition = f"{top} -> ɛ"  # Default transition for empty rules

        # Check if `top` is a regex-based non-terminal
        if top in regex_patterns and regex_patterns[top]:  # Only attempt regex if patterns exist for this non-terminal
            matched = False
            for pattern, compiled_regex in regex_patterns[top].items():
                if compiled_regex.fullmatch(current_token.valor):
                    result = f"Regex match: {current_token.valor}"
                    matched = True
                    index += 1  # Move to the next token
                    break
            if matched:
                display_syntax_tree(stack + [top], current_token, result, transition)
                continue
            else:
                if top in parse_table:
                    token_key = current_token.valor if current_token.valor in parse_table[top] else current_token.tipo
                    if token_key in parse_table[top]:
                        rule = parse_table[top][token_key]
                        result = f"Rule found: {top} -> {rule}"
                        transition = f"{top} -> {rule}"
                        if rule != ['ɛ']:
                            stack.extend(reversed(rule))
                    else:
                        result = f"Error: No rule for '{top}' with current token '{current_token.valor}'"
                        raise SyntaxError(result)
                    display_syntax_tree(stack + [top], current_token, result, transition)
                    continue
                elif top == current_token.valor:
                    result = f"Terminal match: {top} == {current_token.valor}"
                    transition = f"{top} -> terminal"
                    index += 1  # Move to the next token
                    display_syntax_tree(stack + [top], current_token, result, transition)
                    continue
                else:
                    result = f"Error: No matching regex rule for '{top}' with token '{current_token.valor}'"
                    raise SyntaxError(result)

        # Non-regex non-terminal handling
        elif top in parse_table:
            token_key = current_token.valor if current_token.valor in parse_table[top] else current_token.tipo

            if token_key in parse_table[top]:
                rule = parse_table[top][token_key]
                result = f"Rule found: {top} -> {rule}"
                transition = f"{top} -> {rule}"
                if rule != ['ɛ']:
                    stack.extend(reversed(rule))
            else:
                result = f"Error: No rule for '{top}' with current token '{current_token.valor}'"
                raise SyntaxError(result)
            display_syntax_tree(stack + [top], current_token, result, transition)

        elif top == current_token.valor:
            result = f"Terminal match: {top} == {current_token.valor}"
            transition = f"{top} -> terminal"
            index += 1  # Move to the next token
            display_syntax_tree(stack + [top], current_token, result, transition)
            continue

        else:
            result = f"Error: Expected '{top}', but got '{current_token.valor}'"
            raise SyntaxError(result)

    if index == len(tokens) and not stack:
        print("\nParsing completed successfully: Syntax correct.")
        return "yes"
    else:
        print("\nParsing ended with issues: Stack or token list not empty.")
        return "no"


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
