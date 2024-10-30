# LL(1) Parse Table (Sample)
parse_table = {
    'Program': {'int': ['FunctionDecl', 'Program'], 'float': ['FunctionDecl', 'Program'], 
                'void': ['FunctionDecl', 'Program'], 'double': ['FunctionDecl', 'Program'], '$': ['ε']},
    'FunctionDecl': {'int': ['Type', 'ID', '(', 'Params', ')', 'Block'],
                     'float': ['Type', 'ID', '(', 'Params', ')', 'Block'],
                     'void': ['Type', 'ID', '(', 'Params', ')', 'Block'],
                     'double': ['Type', 'ID', '(', 'Params', ')', 'Block']},
    'Type': {'int': ['int'], 'float': ['float'], 'void': ['void'], 'double': ['double']},
    'Params': {'int': ['ParamList'], 'float': ['ParamList'], 'double': ['ParamList'], 'char': ['ParamList'], ')': ['ε']},
    'ParamList': {'int': ['Type', 'ID', 'MoreParams'], 'float': ['Type', 'ID', 'MoreParams'], 
                  'double': ['Type', 'ID', 'MoreParams'], 'char': ['Type', 'ID', 'MoreParams']},
    'MoreParams': {',': [',', 'Type', 'ID', 'MoreParams'], ')': ['ε']},
    'Block': {'{': ['{', 'StatementList', '}']},
    'StatementList': {'int': ['Statement', 'StatementList'], 'if': ['Statement', 'StatementList'],
                      'for': ['Statement', 'StatementList'], 'return': ['Statement', 'StatementList'],
                      'ID': ['Statement', 'StatementList'], '{': ['Statement', 'StatementList'], '}': ['ε']},
    'Statement': {'int': ['VarDecl'], 'if': ['IfStatement'], 'for': ['ForStatement'],
                  'return': ['ReturnStatement'], '{': ['Block'], 'ID': ['Assignment', ';']},
    'VarDecl': {'int': ['Type', 'ID', 'VarInit', ';'], 'float': ['Type', 'ID', 'VarInit', ';'],
                'double': ['Type', 'ID', 'VarInit', ';'], 'char': ['Type', 'ID', 'VarInit', ';']},
    'VarInit': {'=': ['=', 'Expression'], ';': ['ε']},
    'Assignment': {'ID': ['ID', '=', 'Expression']},
    'IfStatement': {'if': ['if', '(', 'Condition', ')', 'Statement', 'ElsePart']},
    'ElsePart': {'else': ['else', 'Statement'], 'int': ['ε'], 'if': ['ε'], 'for': ['ε'], 'return': ['ε'], '}': ['ε']},
    'ForStatement': {'for': ['for', '(', 'ForInit', ';', 'Condition', ';', 'Assignment', ')', 'Statement']},
    'ForInit': {'int': ['Type', 'ID', '=', 'Expression'], 'ID': ['Assignment']},
    'ReturnStatement': {'return': ['return', 'Expression', ';']},
    
    # Condition with Relational Operators
    'Condition': {'(': ['Expression', 'RelationalOp', 'Expression'], 'ID': ['Expression', 'RelationalOp', 'Expression'], 'NUM': ['Expression', 'RelationalOp', 'Expression']},
    'RelationalOp': {'<': ['<'], '>': ['>'], '<=': ['<='], '>=': ['>='], '==': ['=='], '!=': ['!=']},

    # Expression for Arithmetic Handling
    'Expression': {'(': ['Term', "Expression'"], 'ID': ['Term', "Expression'"], 'NUM': ['Term', "Expression'"]},
    'Expression\'': {'+': ['+', 'Term', "Expression'"], '-': ['-', 'Term', "Expression'"], ';': ['ε'], ')': ['ε']},
    'Term': {'(': ['Factor', "Term'"], 'ID': ['Factor', "Term'"], 'NUM': ['Factor', "Term'"]},
    'Term\'': {'*': ['*', 'Factor', "Term'"], '/': ['/', 'Factor', "Term'"], '+': ['ε'], '-': ['ε'], ';': ['ε'], ')': ['ε']},
    'Factor': {'(': ['(', 'Expression', ')'], 'ID': ['ID'], 'NUM': ['NUM']}
}


parse_table_second = {
    'Program': {'int': ['Declaration', 'Program'], 'float': ['Declaration', 'Program'],
                'void': ['Declaration', 'Program'], 'char': ['Declaration', 'Program'],
                '$': ['ε']},
    'Declaration': {'int': ['Type', 'ID', 'DeclarationRest', ';'], 'float': ['Type', 'ID', 'DeclarationRest', ';'],
                    'void': ['Type', 'ID', 'DeclarationRest', ';'], 'char': ['Type', 'ID', 'DeclarationRest', ';']},
    'DeclarationRest': {'=': ['=', 'Expression'], ';': ['ε']},
    'Type': {'int': ['int'], 'float': ['float'], 'void': ['void'], 'char': ['char']},
    'Statement': {'if': ['if', '(', 'Expression', ')', 'Statement', 'else', 'Statement'],
                  'for': ['for', '(', 'Expression', ';', 'Expression', ';', 'Expression', ')', 'Statement'],
                  'while': ['while', '(', 'Expression', ')', 'Statement'], '{': ['Block']},
    'Block': {'{': ['{', 'Program', '}']},
    'Expression': {'(': ['Term', 'Expression\''], 'ID': ['Term', 'Expression\''], 'NUM': ['Term', 'Expression\'']},
    'Expression\'': {'+': ['+', 'Term', 'Expression\''], '-': ['-', 'Term', 'Expression\''], ';': ['ε'], ')': ['ε']},
    'Term': {'(': ['Factor', 'Term\''], 'ID': ['Factor', 'Term\''], 'NUM': ['Factor', 'Term\'']},
    'Term\'': {'*': ['*', 'Factor', 'Term\''], '/': ['/', 'Factor', 'Term\''], '+': ['ε'], '-': ['ε'], ';': ['ε'], ')': ['ε']},
    'Factor': {'(': ['(', 'Expression', ')'], 'ID': ['ID'], 'NUM': ['NUM']},
    'Assignment': {'ID': ['ID', '=', 'Expression']},
    'ValidOpSeq': {'-': ['-', '-'], '+': ['+', '+'], '*': ['*'], '/': ['/'], '=': ['='], ';': ['ε']}
}



def parse(tokens,Token):
    stack = ['$', 'Program']
    index = 0
    tokens.append(Token('$', '$', -1))  # End-of-input marker

    while stack:
        top = stack.pop()
        current_token = tokens[index]
        
        # Debug output for tracing
        print(f"Stack: {stack}, Current Token: {current_token.valor} (Type: {current_token.tipo})")


        # Access token attributes directly
        if current_token.tipo == 'ID':
            current_token_type = current_token.valor
            current_token_value = current_token.tipo
        else:
            current_token_type = current_token.tipo
            current_token_value = current_token.valor



        if top == current_token_value:  # Terminal match based on token value
            index += 1
        elif top in parse_table and current_token_value in parse_table[top]:  # Non-terminal with a rule
            rule = parse_table[top][current_token_value]
            if rule != ['ε']:  # Ignore epsilon productions
                stack.extend(reversed(rule))
        else:
            # Use specific attributes for error message details
            raise SyntaxError(
                f"Unexpected token '{current_token_value}' (type '{current_token_type}') at line {current_token.linea} (position {index})"
            )

    if index == len(tokens) - 1:  # Successfully parsed all tokens
        return "Parsing completed successfully"
    else:
        raise SyntaxError("Parsing failed due to incomplete parse")
