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
    if(define_params == ""):
        return Var(define_name, define_body, "", "Define Statement", line)
    else:
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
    function = False
    functionid = ""
    functionline = -1
    functiontype = ""
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
                elif(function):
                    functionid = current_token.valor
                    functionline = current_token.linea
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
                            variable_param = "("
                        elif(top == "FUNCDEC"):
                            current_scope.append("Function Declaration")
                        elif(top == "FUNCTION" or top == "VOID_FUNCTION"):
                            current_scope.append("Function Body")
                            function = True
                        elif(top == "MAINFUNCTION"):
                            current_scope.append("Function Body")
                            functionid = "main"
                            functionline = current_token.linea
                            function = True
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
                        elif(top == "="):
                            if(definevalue[-1] == "<"):
                                definevalue += current_token.valor + " "
                            elif(definevalue[-1] == " " and definevalue[-2] == ">"):
                                definevalue[-1] = current_token.valor
                                definevalue += " "
                            else:
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
                            if(function):
                                functiontype = "int"
                                function = False
                            elif(variable_declaration):
                                variable_type = "int"
                        case "float":
                            if(function):
                                functiontype = "float"
                                function = False
                            elif(variable_declaration):
                                variable_type = "float"
                        case "char":
                            if(function):
                                functiontype = "char"
                                function = False
                            elif(variable_declaration):
                                variable_type = "char"
                        case "string":
                            if(function):
                                functiontype = "string"
                                function = False
                            elif(variable_declaration):
                                variable_type = "string"
                        case "double":
                            if(function):
                                functiontype = "double"
                                function = False
                            elif(variable_declaration):
                                variable_type = "double"
                        case "long":
                            if(function):
                                functiontype = "long"
                                function = False
                            elif(variable_declaration):
                                variable_type = "long"
                        case "short":
                            if(function):
                                functiontype = "short"
                                function = False
                            elif(variable_declaration):
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
                    elif(current_scope[-1] == "Function Initialization" and variable_declaration and current_token.valor == ")"):
                        variable_param += variable_name + ")"
                        if(variable_name != ""):
                            variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line))
                            variable_name = ""
                            variable_type = ""
                            variable_value = ""
                            variable_line = ""
                        variable_declaration = False
                        value_flag = False
                        variables.append(Var(functionid, "None", functiontype, "Function", functionline, variable_param))
                        variable_param = ""
                        current_scope.pop()
                    elif(current_scope[-1] == "Function Body" and variable_declaration and current_token.valor == ";"):
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
                    elif(variable_declaration and current_token.valor == "," and (current_scope[-1] != "")):
                        if(current_scope[-1] == "Function Initialization"):
                            variable_param += variable_name + ", "
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
                    variable_param = "("
                elif(top == "FUNCDEC"):
                    current_scope.append("Function Declaration")
                elif(top == "FUNCTION" or top == "VOID_FUNCTION"):
                    function = True
                    current_scope.append("Function Body")
                elif(top == "MAINFUNCTION"):
                    current_scope.append("Function Body")
                    functionid = "main"
                    functionline = current_token.linea
                    function = True
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
                    if(definevalue[-1] == "<"):
                        definevalue += current_token.valor + " "
                    elif(definevalue[-1] == " " and definevalue[-2] == ">"):
                        definevalue[-1] = current_token.valor
                        definevalue += " "
                    else:
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
                    if(function):
                        functiontype = "int"
                        function = False
                    elif(variable_declaration):
                        variable_type = "int"
                case "float":
                    if(function):
                        functiontype = "float"
                        function = False
                    elif(variable_declaration):
                        variable_type = "float"
                case "char":
                    if(function):
                        functiontype = "char"
                        function = False
                    elif(variable_declaration):
                        variable_type = "char"
                case "string":
                    if(function):
                        functiontype = "string"
                        function = False
                    elif(variable_declaration):
                        variable_type = "string"
                case "double":
                    if(function):
                        functiontype = "double"
                        function = False
                    elif(variable_declaration):
                        variable_type = "double"
                case "long":
                    if(function):
                        functiontype = "long"
                        function = False
                    elif(variable_declaration):
                        variable_type = "long"
                case "short":
                    if(function):
                        functiontype = "short"
                        function = False
                    elif(variable_declaration):
                        variable_type = "short"
                case "void":
                    functiontype = "void"
                    function = False
                            
            # Variable saving
            if(current_scope[-1] == "Global" and variable_declaration and current_token.valor == ";"):
                variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line))
                variable_declaration = False
                variable_name = ""
                variable_type = ""
                value_flag = False
                variable_value = ""
                variable_line = ""
            elif(current_scope[-1] == "Function Initialization" and variable_declaration and current_token.valor == ")"):
                variable_param += variable_name + ")"
                if(variable_name != ""):
                    variables.append(Var(variable_name, variable_value, variable_type, current_scope[-1], variable_line))
                    variable_name = ""
                    variable_type = ""
                    variable_value = ""
                    variable_line = ""
                variable_declaration = False
                value_flag = False
                variables.append(Var(functionid, "None", functiontype, "Function", functionline, variable_param))
                variable_param = ""
                current_scope.pop()
            elif(current_scope[-1] == "Function Body" and variable_declaration and current_token.valor == ";"):
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
            elif(variable_declaration and current_token.valor == "," and (current_scope[-1] != "")):
                if(current_scope[-1] == "Function Initialization"):
                    variable_param += variable_name + ", "
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
