from prettytable import PrettyTable
import re

class Token:
    def __init__(self, tipo, valor, linea):
        self.tipo = tipo  # Token type
        self.valor = valor  # Token value
        self.linea = linea  # Line number

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor}, Linea: {self.linea})"

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

def define_parse(value, line):
    define_name = ""
    define_body = ""
    define_params = ""
    inparentheses = False
    for index in range(0, len(value)):
        if(value[index] == "("):
            inparentheses = True
        elif(value[index] == ")"):
            inparentheses = False
        if(value[index] == " " and not inparentheses):
            if("<" in define_name):
                define_body = define_name
                define_name = value[index:]
                break
            else:
                define_body = value[index:]
                break
        else:
            define_name += value[index]
    define_name = define_name.strip()
    define_body = define_body.strip()
    #print(define_name)
    #print(define_body)
    if("(" in define_name):
        define_params = "(" + define_name.split("(", 1)[1]
        define_name = define_name.split("(", 1)[0]
    return Var(define_name, define_body, "", "Define Statement", line, define_params)

def variable_parse(tokens, parse_table):
    #Variable Things
    current_scope = ["Invalid", "Invalid", "Global"]
    variable_declaration = False
    variable_name = ""
    variable_type = ""
    value_flag = False
    variable_value = ""
    variable_line = ""
    variable_param = ""
    variables = []
    define_line = -1
    in_define = False
    definevalue = ""
    #Everything else
    stack = ['$']
    stack.append('SOURCE')
    tokens.append(Token('$', '$', -1))
    index = 0
    regex_patterns = {
        non_terminal: {pattern: re.compile(pattern) for pattern in parse_table[non_terminal] if "[" in pattern}
        for non_terminal in parse_table
    }
    while stack:
        #print(current_scope)
        top = stack.pop()
        current_token = tokens[index]
        #print(current_scope)
        #print(current_token)
        if(in_define and (define_line != current_token.linea)):
            #print(current_scope)
            in_define = False
            temp = define_parse(definevalue, define_line)
            variables.append(temp)
            definevalue = ""
            while(current_scope[-1] != 'Define Statement'):
                current_scope.pop()
            current_scope.pop()
            #print(current_scope)
        if top in regex_patterns and regex_patterns[top]:
            matched = False
            for pattern, compiled_regex in regex_patterns[top].items():
                if compiled_regex.fullmatch(current_token.valor):
                    matched = True
                    index += 1
                    break
            if matched:
                if(in_define):
                    definevalue += current_token.valor
                elif(variable_declaration and not value_flag):
                    variable_name = current_token.valor
                    variable_line = current_token.linea
                elif(value_flag):
                    variable_value += current_token.valor
                continue
            else:
                if top in parse_table:
                    token_key = current_token.valor if current_token.valor in parse_table[top] else current_token.tipo
                    if token_key in parse_table[top]:
                        rule = parse_table[top][token_key]
                        
                        #Declaration setting
                        if(top == "INITSTATEMENT" or top == "FUNCINIT"):
                            variable_declaration = True
                        #Scope checking
                        if(top == "FUNCINIT"):
                            current_scope.append("Function Initialization")
                        elif(top == "FUNCDEC"):
                            current_scope.append("Function Declaration")
                        elif(top == "FUNCTION" or top == "VOID_FUNCTION" or top == "MAINFUNCTION"):
                            current_scope.append("Function Body")
                        elif(top == "FORVAR"):
                            current_scope.append("For Loop")
                        elif(top == "IF" or top == "ELSEIF"):
                            current_scope.append("If Statement")
                        elif(top == "SWITCHSTATEMENT"):
                            current_scope.append("Switch Statement")
                        elif(top == "DEFINESTATEMENT"):
                            current_scope.append("Define Statement")
                            in_define = True
                            define_line = current_token.linea
                        if rule != ['ɛ']:
                            stack.extend(reversed(rule))
                    continue
                elif top == current_token.valor:
                    if(in_define and top != "#define"):
                        if(definevalue[-1] != "<" and (top == "int" or top == "float" or top == "char")):
                            definevalue += " " + current_token.valor + " "
                        else:
                            definevalue += current_token.valor
                        if(current_token.valor == ")" or current_token.valor == ">" or current_token.valor == ","):
                            definevalue += " "
                        continue
                    if(top == "=" and variable_declaration):
                        value_flag = True
                    elif(top == "," and variable_declaration):
                        value_flag = False
                        variable_param += ', '
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
                        variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line, variable_param))
                        variable_declaration = False
                        variable_name = ""
                        variable_type = ""
                        value_flag = False
                        variable_value = ""
                        variable_line = ""
                    elif(current_scope[-1] == "Function Initialization" and variable_declaration and current_token.valor == ")"):
                        variable_param += ')'
                        variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line, variable_param))
                        variable_declaration = False
                        variable_name = ""
                        variable_type = ""
                        value_flag = False
                        variable_value = ""
                        variable_line = ""
                        variable_param = ""
                        current_scope.pop()
                    elif(current_scope[-1] == "Function Body" and variable_declaration and current_token.valor == ";"):
                        variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line, variable_param))
                        variable_declaration = False
                        variable_name = ""
                        variable_type = ""
                        value_flag = False
                        variable_value = ""
                        variable_line = ""
                    elif(current_scope[-1] == "For Loop" and variable_declaration and current_token.valor == ";"):
                        variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line, variable_param))
                        variable_declaration = False
                        variable_name = ""
                        variable_type = ""
                        value_flag = False
                        variable_value = ""
                        variable_line = ""
                    elif(current_scope[-1] == "If Statement" and variable_declaration and current_token.valor == ";"):
                        variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line, variable_param))
                        variable_declaration = False
                        variable_name = ""
                        variable_type = ""
                        value_flag = False
                        variable_value = ""
                        variable_line = ""
                    elif(current_scope[-1] == "Switch Statement" and variable_declaration and current_token.valor == ";"):
                        variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line, variable_param))
                        variable_declaration = False
                        variable_name = ""
                        variable_type = ""
                        value_flag = False
                        variable_value = ""
                        variable_line = ""
                    elif(variable_declaration and in_define and current_token.valor == ")"):
                        variable_param += ')'
                        variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line, variable_param))
                        variable_declaration = False
                        variable_name = ""
                        variable_type = ""
                        value_flag = False
                        variable_value = ""
                        variable_line = ""
                        variable_param = ""
                    #Saving without end of init statements
                    elif(variable_declaration and current_token.valor == "," and (current_scope[-1] != "")):
                        variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line))
                        variable_name = ""
                        value_flag = False
                        variable_value = ""
                        variable_line = ""
                    
                    if(current_token.valor == "}"):
                        current_scope.pop()
                    index += 1
                    continue
        elif top in parse_table:
            token_key = current_token.valor if current_token.valor in parse_table[top] else current_token.tipo
            if token_key in parse_table[top]:
                rule = parse_table[top][token_key]
                #Declaration setting
                if(top == "INITSTATEMENT" or top == "FUNCINIT"):
                    variable_declaration = True
                #Scope checking
                if(top == "FUNCINIT"):
                    current_scope.append("Function Initialization")
                elif(top == "FUNCDEC"):
                    current_scope.append("Function Declaration")
                elif(top == "FUNCTION" or top == "VOID_FUNCTION" or top == "MAINFUNCTION"):
                    current_scope.append("Function Body")
                elif(top == "FORVAR"):
                    current_scope.append("For Loop")
                elif(top == "IF" or top == "ELSEIF"):
                    current_scope.append("If Statement")
                elif(top == "SWITCHSTATEMENT"):
                    current_scope.append("Switch Statement")
                elif(top == "DEFINESTATEMENT"):
                    current_scope.append("Define Statement")
                    in_define = True
                    define_line = current_token.linea
                if rule != ['ɛ']:
                    stack.extend(reversed(rule))
            continue
        elif top == current_token.valor:
            if(in_define and top != "#define"):
                if(definevalue[-1] != "<" and (top == "int" or top == "float" or top == "char")):
                    if(definevalue[-1] == "("):
                        definevalue += current_token.valor + " "
                    else:
                        definevalue += " " + current_token.valor + " "
                        
                elif(top == "="):
                    definevalue += " " + current_token.valor + " "
                else:
                    definevalue += current_token.valor
                if(top == ")" or top == ">" or top == "," or top == ";"):
                    definevalue += " "
                index += 1
                continue
            if(top == "=" and variable_declaration):
                value_flag = True
            elif(top == "," and variable_declaration):
                value_flag = False
                variable_param += ', '
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
                variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line, variable_param))
                variable_declaration = False
                variable_name = ""
                variable_type = ""
                value_flag = False
                variable_value = ""
                variable_line = ""
            elif(current_scope[-1] == "Function Initialization" and variable_declaration and current_token.valor == ")"):
                variable_param += ')'
                variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line, variable_param))
                variable_declaration = False
                variable_name = ""
                variable_type = ""
                value_flag = False
                variable_value = ""
                variable_line = ""
                variable_param = ""
                current_scope.pop()
            elif(current_scope[-1] == "Function Body" and variable_declaration and current_token.valor == ";"):
                variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line, variable_param))
                variable_declaration = False
                variable_name = ""
                variable_type = ""
                value_flag = False
                variable_value = ""
                variable_line = ""
            elif(current_scope[-1] == "For Loop" and variable_declaration and current_token.valor == ";"):
                variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line, variable_param))
                variable_declaration = False
                variable_name = ""
                variable_type = ""
                value_flag = False
                variable_value = ""
                variable_line = ""
            elif(current_scope[-1] == "If Statement" and variable_declaration and current_token.valor == ";"):
                variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line, variable_param))
                variable_declaration = False
                variable_name = ""
                variable_type = ""
                value_flag = False
                variable_value = ""
                variable_line = ""
            elif(current_scope[-1] == "Switch Statement" and variable_declaration and current_token.valor == ";"):
                variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line, variable_param))
                variable_declaration = False
                variable_name = ""
                variable_type = ""
                value_flag = False
                variable_value = ""
                variable_line = ""
            elif(variable_declaration and in_define and current_token.valor == ")"):
                variable_param += ')'
                variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line, variable_param))
                variable_declaration = False
                variable_name = ""
                variable_type = ""
                value_flag = False
                variable_value = ""
                variable_line = ""
                variable_param = ""
            #Saving without end of init statements
            elif(variable_declaration and current_token.valor == "," and (current_scope[-1] != "")):
                variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line))
                variable_name = ""
                value_flag = False
                variable_value = ""
                variable_line = ""
            
            if(current_token.valor == "}"):
                current_scope.pop()
            index += 1  # Move to the next token
            continue
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
