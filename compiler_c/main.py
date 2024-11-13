from lexer import lexer, trabajar_variables, Token
from parser_tokens import parse
from SemanticAnalyzer import analyze_structure
from code_generator import generate_code , reset_intermediate_code
from object_code_generator import generate_object_code, print_object_code, reset_object_code

# Leer el archivo source_code.c
with open('source_code.c', 'r') as file:
    codigo = file.read()


""" -----------------------------LEXER-------------------------------------- """
# Ejecutar el lexer con variables
tokens = lexer(codigo)
variables = trabajar_variables(tokens)
""" -----------------------------PARSER------------------------------------- """
# Parsear el código fuente
parse_table = {
    "SOURCE": {
        "#include": ["INCLUDEBLOCK", "DEFINEBLOCK", "FUNCTIONBLOCK", "MAINFUNCTION"],
        "#define": ["INCLUDEBLOCK", "DEFINEBLOCK", "FUNCTIONBLOCK", "MAINFUNCTION"],
        "int": ["INCLUDEBLOCK", "DEFINEBLOCK", "FUNCTIONBLOCK", "MAINFUNCTION"],
        "float": ["INCLUDEBLOCK", "DEFINEBLOCK", "FUNCTIONBLOCK", "MAINFUNCTION"],
        "char": ["INCLUDEBLOCK", "DEFINEBLOCK", "FUNCTIONBLOCK", "MAINFUNCTION"],
        "string": ["INCLUDEBLOCK", "DEFINEBLOCK", "FUNCTIONBLOCK", "MAINFUNCTION"],
        "double": ["INCLUDEBLOCK", "DEFINEBLOCK", "FUNCTIONBLOCK", "MAINFUNCTION"],
        "long": ["INCLUDEBLOCK", "DEFINEBLOCK", "FUNCTIONBLOCK", "MAINFUNCTION"],
        "short": ["INCLUDEBLOCK", "DEFINEBLOCK", "FUNCTIONBLOCK", "MAINFUNCTION"],
        "void": ["INCLUDEBLOCK", "DEFINEBLOCK", "FUNCTIONBLOCK", "MAINFUNCTION"]
    },
    
    "INCLUDEBLOCK": {
        "#include": ["INCLUDESTATEMENT", "INCLUDEBLOCK"],
        "ɛ": []
    },
    
    "DEFINEBLOCK": {
        "#define": ["DEFINESTATEMENT", "DEFINEBLOCK"],
        "ɛ": []
    },
    
    "FUNCTIONBLOCK": {
        "int": ["FUNCDEC", "FUNCTIONBLOCK"],
        "float": ["FUNCDEC", "FUNCTIONBLOCK"],
        "char": ["FUNCDEC", "FUNCTIONBLOCK"],
        "string": ["FUNCDEC", "FUNCTIONBLOCK"],
        "double": ["FUNCDEC", "FUNCTIONBLOCK"],
        "long": ["FUNCDEC", "FUNCTIONBLOCK"],
        "short": ["FUNCDEC", "FUNCTIONBLOCK"],
        "void": ["FUNCDEC", "FUNCTIONBLOCK"],
        "ɛ": []
    },
    
    "MAINFUNCTION": {
        "int": ["FUNCTYPE", "main", "(", "INITLIST", ")", "{", "STATEMENT", "RETURNSTATEMENT", "}"],
        "float": ["FUNCTYPE", "main", "(", "INITLIST", ")", "{", "STATEMENT", "RETURNSTATEMENT", "}"],
        "char": ["FUNCTYPE", "main", "(", "INITLIST", ")", "{", "STATEMENT", "RETURNSTATEMENT", "}"],
        "string": ["FUNCTYPE", "main", "(", "INITLIST", ")", "{", "STATEMENT", "RETURNSTATEMENT", "}"],
        "double": ["FUNCTYPE", "main", "(", "INITLIST", ")", "{", "STATEMENT", "RETURNSTATEMENT", "}"],
        "long": ["FUNCTYPE", "main", "(", "INITLIST", ")", "{", "STATEMENT", "RETURNSTATEMENT", "}"],
        "short": ["FUNCTYPE", "main", "(", "INITLIST", ")", "{", "STATEMENT", "RETURNSTATEMENT", "}"],
        "void": ["void", "main", "(", "INITLIST", ")", "{", "STATEMENT", "RETURNSTATEMENT", "}"]
    },
    
    "STATEMENT": {
        "static": ["INITLINE", "STATEMENT"],
        "const": ["INITLINE", "STATEMENT"],
        "volatile": ["INITLINE", "STATEMENT"],
        "inline": ["INITLINE", "STATEMENT"],
        "if": ["CONDITIONAL", "STATEMENT"],
        "switch": ["SWITCHSTATEMENT", "STATEMENT"],
        "for": ["FORLOOP"],
        "while": ["WHILELOOP"],
        "do": ["DOWHILELOOP"],
        "VARNAME": ["VARCHANGELINE", "STATEMENT"],
        "return": ["RETURNSTATEMENT", "STATEMENT"],
        "ɛ": []
    },
    
    "CONDITIONAL": {
        "if": ["if", "(", "CONDITION", ")", "{", "STATEMENT", "}", "CONDITIONAL_ELSE"]
    },
    
    "CONDITIONAL_ELSE": {
        "else": ["else", "{", "STATEMENT", "}"],
        "ɛ": []
    },
    
    "SWITCHSTATEMENT": {
        "switch": ["switch", "(", "VARNAME", ")", "{", "SWITCHCASELIST", "}"]
    },
    
    "SWITCHCASELIST": {
        "case": ["SWITCHCASE", "SWITCHCASELIST'", "DEFAULTCASE"],
        "default": ["SWITCHCASE", "SWITCHCASELIST'", "DEFAULTCASE"]
    },
    
    "SWITCHCASELIST'": {
        "case": ["SWITCHCASE", "SWITCHCASELIST'"],
        "ɛ": []
    },
    
    "DEFAULTCASE": {
        "default": ["default:", "STATEMENT", "break;"]
    },
    
    "LOOPSTATEMENT": {
        "for": ["FORLOOP"],
        "while": ["WHILELOOP"],
        "do": ["DOWHILELOOP"]
    },
    
    "FORLOOP": {
        "for": ["for", "(", "FORVAR", ";", "CONDITION", ";", "VARCHANGESTATEMENT", ")", "{", "STATEMENT", "}"]
    },
    
    "FORVAR": {
        "int": ["INITSTATEMENT"],
        "float": ["INITSTATEMENT"],
        "char": ["INITSTATEMENT"],
        "string": ["INITSTATEMENT"],
        "double": ["INITSTATEMENT"],
        "long": ["INITSTATEMENT"],
        "short": ["INITSTATEMENT"],
        "VARNAME": ["VARNAME"]
    },
    
    "WHILELOOP": {
        "while": ["while", "(", "CONDITION", ")", "{", "STATEMENT", "}"]
    },
    
    "DOWHILELOOP": {
        "do": ["do", "{", "STATEMENT", "}", "while", "(", "CONDITION", ")"]
    },
    
    "VARNAME": {
        "[a-zA-Z_][a-zA-Z0-9_]*": ["[a-zA-Z_][a-zA-Z0-9_]*"]
    },
    
    "KEYWORD": {
        "static": ["static"],
        "const": ["const"],
        "volatile": ["volatile"],
        "inline": ["inline"],
        "ɛ": []
    },
    
    "INCLUDESTATEMENT": {
        "#include": ["#include", "<", "VARNAME", ".", "VARNAME", ">"],
        "#include (quote)": ["#include", "\"", "VARNAME", ".", "VARNAME", "\""]
    },
    
    "DEFINESTATEMENT": {
        "#define": ["#define", "VARNAME", "VARNAME"],
        "#define": ["#define", "VARNAME", "{", "STATEMENT", "}"],
        "#define": ["#define", "FUNCTION"]
    },
    
    "RETURNSTATEMENT": {
        "return": ["return", "VARVAL", ";"],
        "return": ["return", ";"]
    },
    
    "INITLINE": {
        "static": ["KEYWORD", "INITSTATEMENT"],
        "const": ["KEYWORD", "INITSTATEMENT"],
        "volatile": ["KEYWORD", "INITSTATEMENT"],
        "inline": ["KEYWORD", "INITSTATEMENT"]
    },
    
    "INITLIST": {
        "int": ["INITSTATEMENT", "INITLIST'"],
        "float": ["INITSTATEMENT", "INITLIST'"],
        "char": ["INITSTATEMENT", "INITLIST'"],
        "string": ["INITSTATEMENT", "INITLIST'"],
        "double": ["INITSTATEMENT", "INITLIST'"],
        "long": ["INITSTATEMENT", "INITLIST'"],
        "short": ["INITSTATEMENT", "INITLIST'"],
        "VARNAME": ["INITSTATEMENT", "INITLIST'"]
    },
    
    "INITLIST'": {
        "int": ["INITSTATEMENT", "INITLIST'"],
        "float": ["INITSTATEMENT", "INITLIST'"],
        "char": ["INITSTATEMENT", "INITLIST'"],
        "string": ["INITSTATEMENT", "INITLIST'"],
        "double": ["INITSTATEMENT", "INITLIST'"],
        "long": ["INITSTATEMENT", "INITLIST'"],
        "short": ["INITSTATEMENT", "INITLIST'"],
        "VARNAME": ["INITSTATEMENT", "INITLIST'"],
        "ɛ": []
    },
    
    "INITSTATEMENT": {
        "int": ["INTINIT"],
        "float": ["FLOATINIT"],
        "char": ["CHARINIT"],
        "string": ["STRINGINIT"],
        "double": ["DOUBLEINIT"],
        "long": ["LONGINIT"],
        "short": ["SHORTINIT"]
    },
    
    "INTINIT": {
        "int": ["int", "VARNAME", "INTLIST"],
        "int": ["int", "VARNAME", "=", "INTVAL", "INTLIST"]
    },
    
    "FLOATINIT": {
        "float": ["float", "VARNAME", "FLOATLIST"],
        "float": ["float", "VARNAME", "=", "FLOATVAL", "FLOATLIST"]
    },
    
    "CHARINIT": {
        "char": ["char", "VARNAME", "CHARLIST"],
        "char": ["char", "VARNAME", "=", "CHARVAL", "CHARLIST"]
    },
    
    "STRINGINIT": {
        "string": ["string", "VARNAME", "STRINGLIST"],
        "string": ["string", "VARNAME", "=", "STRINGVAL", "STRINGLIST"]
    },
    
    "DOUBLEINIT": {
        "double": ["double", "VARNAME", "DOUBLELIST"],
        "double": ["double", "VARNAME", "=", "DOUBLEVAL", "DOUBLELIST"]
    },
    
    "LONGINIT": {
        "long": ["long", "VARNAME", "LONGLIST"],
        "long": ["long", "VARNAME", "=", "INTVAL", "LONGLIST"]
    },
    
    "SHORTINIT": {
        "short": ["short", "VARNAME", "SHORTLIST"],
        "short": ["short", "VARNAME", "=", "INTVAL", "SHORTLIST"]
    },
    
    "INTLIST": {
        ",": [",", "VARNAME", "INTLIST"],
        ",": [",", "VARNAME", "=", "INTVAL", "INTLIST"],
        "ɛ": []
    },
    
    "FLOATLIST": {
        ",": [",", "VARNAME", "FLOATLIST"],
        ",": [",", "VARNAME", "=", "FLOATVAL", "FLOATLIST"],
        "ɛ": []
    },
    
    "CHARLIST": {
        ",": [",", "VARNAME", "CHARLIST"],
        ",": [",", "VARNAME", "=", "CHARVAL", "CHARLIST"],
        "ɛ": []
    },
    
    "STRINGLIST": {
        ",": [",", "VARNAME", "STRINGLIST"],
        ",": [",", "VARNAME", "=", "STRINGVAL", "STRINGLIST"],
        "ɛ": []
    },
    
    "DOUBLELIST": {
        ",": [",", "VARNAME", "DOUBLELIST"],
        ",": [",", "VARNAME", "=", "DOUBLEVAL", "DOUBLELIST"],
        "ɛ": []
    },
    
    "LONGLIST": {
        ",": [",", "VARNAME", "LONGLIST"],
        ",": [",", "VARNAME", "=", "INTVAL", "LONGLIST"],
        "ɛ": []
    },
    
    "SHORTLIST": {
        ",": [",", "VARNAME", "SHORTLIST"],
        ",": [",", "VARNAME", "=", "INTVAL", "SHORTLIST"],
        "ɛ": []
    },
    
    "VARVAL": {
        "VARNAME": ["ARITH_EXPR"],
        "INTVAL": ["ARITH_EXPR"],
        "FLOATVAL": ["ARITH_EXPR"],
        "CHARVAL": ["ARITH_EXPR"],
        "STRINGVAL": ["ARITH_EXPR"],
        "DOUBLEVAL": ["ARITH_EXPR"],
        "(": ["ARITH_EXPR"]
    },
    
    "ARITH_EXPR": {
        "VARNAME": ["TERM", "ARITH_EXPR'"],
        "INTVAL": ["TERM", "ARITH_EXPR'"],
        "FLOATVAL": ["TERM", "ARITH_EXPR'"],
        "CHARVAL": ["TERM", "ARITH_EXPR'"],
        "STRINGVAL": ["TERM", "ARITH_EXPR'"],
        "DOUBLEVAL": ["TERM", "ARITH_EXPR'"],
        "(": ["TERM", "ARITH_EXPR'"]
    },
    
    "ARITH_EXPR'": {
        "+": ["+", "TERM", "ARITH_EXPR'"],
        "-": ["-", "TERM", "ARITH_EXPR'"],
        "ɛ": []
    },
    
    "TERM": {
        "VARNAME": ["FACTOR", "TERM'"],
        "INTVAL": ["FACTOR", "TERM'"],
        "FLOATVAL": ["FACTOR", "TERM'"],
        "CHARVAL": ["FACTOR", "TERM'"],
        "STRINGVAL": ["FACTOR", "TERM'"],
        "DOUBLEVAL": ["FACTOR", "TERM'"],
        "(": ["FACTOR", "TERM'"]
    },
    
    "TERM'": {
        "*": ["*", "FACTOR", "TERM'"],
        "/": ["/", "FACTOR", "TERM'"],
        "ɛ": []
    },
    
    "FACTOR": {
        "VARNAME": ["VARNAME"],
        "INTVAL": ["INTVAL"],
        "FLOATVAL": ["FLOATVAL"],
        "CHARVAL": ["CHARVAL"],
        "STRINGVAL": ["STRINGVAL"],
        "DOUBLEVAL": ["DOUBLEVAL"],
        "(": ["(", "ARITH_EXPR", ")"]
    },
    
    "INTVAL": {
        "[0-9][0-9]*": ["[0-9][0-9]*"]
    },
    
    "FLOATVAL": {
        "[0-9][0-9]*.[0-9]+": ["[0-9][0-9]*.[0-9]+"],
        "[0-9][0-9]*f": ["[0-9][0-9]*f"]
    },
    
    "CHARVAL": {
        "'[a-zA-Z0-9$&+,:;=?@#|'<>.^*()%!-]*'": ["'[a-zA-Z0-9$&+,:;=?@#|'<>.^*()%!-]*'"]
    },
    
    "STRINGVAL": {
        "\"[a-zA-Z0-9$&+,:;=?@#|'<>.^*()%!-]*\"": ["\"[a-zA-Z0-9$&+,:;=?@#|'<>.^*()%!-]*\""]
    },
    
    "DOUBLEVAL": {
        "[0-9][0-9]*.[0-9]*d": ["[0-9][0-9]*.[0-9]*d"],
        "[0-9][0-9]*.[0-9]*": ["[0-9][0-9]*.[0-9]*"]
    },
    
    "VARCHANGELINE": {
        "VARNAME": ["VARCHANGESTATEMENT", ";"]
    },
    
    "VARCHANGESTATEMENT": {
        "VARNAME": ["VARNAME", "VARIABLE_MODIFICATION"]
    },
    
    "VARIABLE_MODIFICATION": {
        "++": ["++"],
        "--": ["--"],
        "=": ["=", "ARITH_EXPR"],
        "+=": ["+=", "ARITH_EXPR"],
        "-=": ["-=", "ARITH_EXPR"],
        "*=": ["*=", "ARITH_EXPR"],
        "/=": ["/=", "ARITH_EXPR"]
    },
    
    "VAROPLIST": {
        "ɛ": [],
        "+": ["PLUS_OPERATION"],
        "-": ["MINUS_OPERATION"],
        "*": ["MULTIPLY_OPERATION"],
        "/": ["DIVIDE_OPERATION"]
    },
    
    "PLUS_OPERATION": {
        "+": ["+", "VARNAME", "VAROPLIST"],
        "+": ["+", "ARITH_EXPR", "VAROPLIST"]
    },
    
    "MINUS_OPERATION": {
        "-": ["-", "VARNAME", "VAROPLIST"],
        "-": ["-", "ARITH_EXPR", "VAROPLIST"]
    },
    
    "MULTIPLY_OPERATION": {
        "*": ["*", "VARNAME", "VAROPLIST"],
        "*": ["*", "ARITH_EXPR", "VAROPLIST"]
    },
    
    "DIVIDE_OPERATION": {
        "/": ["/", "VARNAME", "VAROPLIST"],
        "/": ["/", "ARITH_EXPR", "VAROPLIST"]
    }
}


print(parse(tokens,parse_table))
""" ---------------------------SEMANTICO------------------------------------ """
#TODO: respuesta de parser 
parsed_structure = [
    {"type": "declaration", "name": "result", "var_type": "int", "value": 1},
    {"type": "declaration", "name": "i", "var_type": "int", "value": 1},
    {"type": "assignment", "name": "result", "value": "result * i"},
    {"type": "return", "value": "result"}
]

#llamando al analizador semantico
analyze_structure(parsed_structure)

""" ------------------------CODIGO INTERMEDIO------------------------------- """
# Generador de codigo intermedio
reset_intermediate_code()
intermediate_code = generate_code(parsed_structure)

""" -------------------------CODIGO OBJETO---------------------------------- """
reset_object_code()
generate_object_code(intermediate_code)
print_object_code()