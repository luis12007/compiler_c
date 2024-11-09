# LL(1) Parse Table (Sample)
parse_table = {
    'Program': {
        'var': ['var', 'Variables', 'begin', 'Operators', 'end'],
        '$': None  # End of input
    },
    'Variables': {
        'identifier': ['Variable', ';', 'Variables'],
        ';': ['ε'],  # Epsilon production
        'begin': ['ε']
    },
    'Variable': {
        'identifier': ['identifier']
    },
    'Operators': {
        'read': ['Operator', ';', 'Operators'],
        'write': ['Operator', ';', 'Operators'],
        'end': ['ε']  # Epsilon production
    },
    'Operator': {
        'read': ['read', '(', 'Variable', ')'],
        'write': ['write', '(', 'Variable', ')']
    },
    'INCLUDEBLOCK': {
        '->': ['->', 'INCLUDESTATEMENT', 'INCLUDEBLOCK'],
        '$': ['ε']
    },
    'DEFINEBLOCK': {
        '->': ['->', 'DEFINESTATEMENT', 'DEFINEBLOCK'],
        '$': ['ε']
    },
    'FUNCTIONBLOCK': {
        '->': ['->', 'FUNCDEC', 'FUNCTIONBLOCK'],
        '$': ['ε']
    },
    'STATEMENT': {
        'INITLINE': ['INITLINE', 'STATEMENT'],
        'SWITCHSTATEMENT': ['SWITCHSTATEMENT', 'STATEMENT'],
        'CONDITIONAL': ['CONDITIONAL', 'STATEMENT'],
        'LOOPSTATEMENT': ['LOOPSTATEMENT', 'STATEMENT'],
        'VARCHANGELINE': ['VARCHANGELINE', 'STATEMENT'],
        'RETURNSTATEMENT': ['RETURNSTATEMENT', 'STATEMENT'],
        '}': ['ε']
    },
    'CONDITION': {
        'VARNAME': ['VARNAME', 'CONDOPERATOR', 'VARNAME'],
        'VARVAL': ['VARVAL', 'CONDOPERATOR', 'VARVAL'],
        '(0 + 1)': ['(0 + 1)'],
        '(true + false)': ['(true + false)']
    },
    'CONDOPERATOR': {
        '==': ['=='],
        '<': ['<'],
        '<=': ['<='],
        '>': ['>'],
        '>=': ['>=']
    },
    'CONDITIONAL': {
        'if': ['if', '(', 'CONDITION', ')', '{', 'STATEMENT', '}', 'ELSE']
    },
    'ELSE': {
        'else': ['else', 'CONDITIONAL'],
        '$': ['ε']
    },
    'SWITCHSTATEMENT': {
        'switch': ['switch', '(', 'VARNAME', ')', '{', 'SWITCHCASELIST', '}']
    },
    'SWITCHCASELIST': {
        'case': ['SWITCHCASE', 'SWITCHCASELIST'],
        'default': ['default', ':', 'STATEMENT', 'break;'],
        '}': ['ε']
    },
    'SWITCHCASE': {
        'case': ['case', 'VARVAL', ':', 'STATEMENT', 'break;']
    },
    'LOOPSTATEMENT': {
        'for': ['FORLOOP'],
        'while': ['WHILELOOP'],
        'do': ['DOWHILELOOP']
    },
    'FORLOOP': {
        'for': ['for', '(', 'FORVAR', ';', 'CONDITION', ';', 'VARCHANGESTATEMENT', ')', '{', 'STATEMENT', '}']
    },
    'WHILELOOP': {
        'while': ['while', '(', 'CONDITION', ')', '{', 'STATEMENT', '}']
    },
    'DOWHILELOOP': {
        'do': ['do', '{', 'STATEMENT', '}', 'while', '(', 'CONDITION', ')']
    },
    'VARNAME': {
        '[a-zA-Z_]': ['[a-zA-Z_]', '[a-zA-Z0-9_]*']  # Regular expression match for variable names
    },
    'INCLUDESTATEMENT': {
        '#include': ['#include', '<', 'VARNAME', '>'],
        'STRINGVAL': ['#include', 'STRINGVAL']
    },
    'DEFINESTATEMENT': {
        '#define': ['#define', 'VARNAME', 'VARNAME'],
        '{': ['#define', 'VARNAME', '{', 'STATEMENT', '}'],
        'FUNCTION': ['#define', 'FUNCTION']
    },
    'RETURNSTATEMENT': {
        'return': ['return', 'VARVAL', ';'],
        ';': ['return', ';']
    },
    # Additional non-terminals and terminals go here
}

# This table is partial and serves as a structure. You’ll need to expand it fully based on all productions in your grammar.



# Parsing function
def parse(tokens, Token):
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

# Define Token class if not defined
class Token:
    def __init__(self, tipo, valor, linea):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea

# Example usage
# Assume tokens is a list of Token objects generated from lexical analysis
tokens = [Token('var', 'var', 1), Token('identifier', 'x', 1), Token(';', ';', 1), Token('begin', 'begin', 2), Token('end', 'end', 3)]
try:
    result = parse(tokens, Token)
    print(result)
except SyntaxError as e:
    print(e)