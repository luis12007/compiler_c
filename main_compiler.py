from lexer_c import lexer, imprimir_tabla, imprimir_variables, trabajar_variables, Token
from parser import parse

# Leer el archivo example_one.c
with open('example_one.c', 'r') as file:
    codigo = file.read()

# Ejecutar el lexer
tokens = lexer(codigo)

# Obtener valores
variables = trabajar_variables(tokens)

# Imprimir la tabla de símbolos

imprimir_variables(variables)
imprimir_tabla(tokens)

parse_table = {
    "SOURCE": {
        "#include": ["INCLUDEBLOCK", "DEFINEBLOCK", "FUNCTIONBLOCK", "MAINFUNCTION"],
        "#define": ["INCLUDEBLOCK", "DEFINEBLOCK", "FUNCTIONBLOCK", "MAINFUNCTION"],
        "int": ["INCLUDEBLOCK", "DEFINEBLOCK", "FUNCTIONBLOCK", "MAINFUNCTION"],
        "void": ["INCLUDEBLOCK", "DEFINEBLOCK", "FUNCTIONBLOCK", "MAINFUNCTION"],
        "float": ["INCLUDEBLOCK", "DEFINEBLOCK", "FUNCTIONBLOCK", "MAINFUNCTION"],
        "char": ["INCLUDEBLOCK", "DEFINEBLOCK", "FUNCTIONBLOCK", "MAINFUNCTION"],
        "string": ["INCLUDEBLOCK", "DEFINEBLOCK", "FUNCTIONBLOCK", "MAINFUNCTION"],
        "double": ["INCLUDEBLOCK", "DEFINEBLOCK", "FUNCTIONBLOCK", "MAINFUNCTION"],
        "long": ["INCLUDEBLOCK", "DEFINEBLOCK", "FUNCTIONBLOCK", "MAINFUNCTION"],
        "short": ["INCLUDEBLOCK", "DEFINEBLOCK", "FUNCTIONBLOCK", "MAINFUNCTION"],
        "$": ["ε"]
    },

    "INCLUDEBLOCK": {
        "#include": ["INCLUDESTATEMENT", "INCLUDEBLOCK"],
        "#define": ["ε"],
        "int": ["ε"],
        "void": ["ε"],
        "float": ["ε"],
        "char": ["ε"],
        "string": ["ε"],
        "double": ["ε"],
        "long": ["ε"],
        "short": ["ε"],
        "$": ["ε"]
    },

    "DEFINEBLOCK": {
        "#define": ["DEFINESTATEMENT", "DEFINEBLOCK"],
        "int": ["ε"],
        "void": ["ε"],
        "float": ["ε"],
        "char": ["ε"],
        "string": ["ε"],
        "double": ["ε"],
        "long": ["ε"],
        "short": ["ε"],
        "$": ["ε"]
    },

    "FUNCTIONBLOCK": {
        "int": ["FUNCDEC", "FUNCTIONBLOCK"],
        "void": ["FUNCDEC", "FUNCTIONBLOCK"],
        "float": ["FUNCDEC", "FUNCTIONBLOCK"],
        "char": ["FUNCDEC", "FUNCTIONBLOCK"],
        "string": ["FUNCDEC", "FUNCTIONBLOCK"],
        "double": ["FUNCDEC", "FUNCTIONBLOCK"],
        "long": ["FUNCDEC", "FUNCTIONBLOCK"],
        "short": ["FUNCDEC", "FUNCTIONBLOCK"],
        "$": ["ε"]
    },

    "INCLUDESTATEMENT": {
        "#include": ["#include", "<", "VARNAME", ">"]
    },

    "DEFINESTATEMENT": {
        "#define": ["#define", "VARNAME", "VARNAME"],
        "{": ["#define", "VARNAME", "{", "STATEMENT", "}"],
        "FUNCTION": ["#define", "FUNCTION"]
    },

    "MAINFUNCTION": {
        "int": ["FUNCTYPE", "main", "(", "INITLIST", ")", "{", "STATEMENT", "RETURNSTATEMENT", "}"],
        "void": ["void", "main", "(", "INITLIST", ")", "{", "STATEMENT", "RETURNSTATEMENT", "}"]
    },

    "FUNCDEC": {
        "int": ["FUNCTYPE", "FUNCTION"],
        "float": ["FUNCTYPE", "FUNCTION"],
        "char": ["FUNCTYPE", "FUNCTION"],
        "string": ["FUNCTYPE", "FUNCTION"],
        "double": ["FUNCTYPE", "FUNCTION"],
        "long": ["FUNCTYPE", "FUNCTION"],
        "short": ["FUNCTYPE", "FUNCTION"],
        "void": ["FUNCTYPE", "FUNCTION"]
    },

    "FUNCTION": {
        "VARNAME": ["VARNAME", "(", "INITLIST", ")", "{", "STATEMENT", "RETURNSTATEMENT", "}"]
    },

    "FUNCTYPE": {
        "int": ["int"],
        "float": ["float"],
        "char": ["char"],
        "string": ["string"],
        "double": ["double"],
        "long": ["long"],
        "short": ["short"],
        "void": ["void"]
    },

    "STATEMENT": {
        "int": ["INITLINE", "STATEMENT"],
        "float": ["INITLINE", "STATEMENT"],
        "char": ["INITLINE", "STATEMENT"],
        "string": ["INITLINE", "STATEMENT"],
        "double": ["INITLINE", "STATEMENT"],
        "long": ["INITLINE", "STATEMENT"],
        "short": ["INITLINE", "STATEMENT"],
        "switch": ["SWITCHSTATEMENT", "STATEMENT"],
        "if": ["CONDITIONAL", "STATEMENT"],
        "for": ["LOOPSTATEMENT", "STATEMENT"],
        "return": ["RETURNSTATEMENT", "STATEMENT"],
        "$": ["ε"]
    },
    "INITLINE": {
        "static": ["KEYWORD", "INITSTATEMENT"],
        "const": ["KEYWORD", "INITSTATEMENT"],
        "volatile": ["KEYWORD", "INITSTATEMENT"],
        "inline": ["KEYWORD", "INITSTATEMENT"],
        "int": ["INITSTATEMENT"],
        "float": ["INITSTATEMENT"],
        "char": ["INITSTATEMENT"],
        "string": ["INITSTATEMENT"],
        "double": ["INITSTATEMENT"],
        "long": ["INITSTATEMENT"],
        "short": ["INITSTATEMENT"]
    },

    "INITLIST": {
        "int": ["INITSTATEMENT", "INITLIST'"],
        "float": ["INITSTATEMENT", "INITLIST'"],
        "char": ["INITSTATEMENT", "INITLIST'"],
        "string": ["INITSTATEMENT", "INITLIST'"],
        "double": ["INITSTATEMENT", "INITLIST'"],
        "long": ["INITSTATEMENT", "INITLIST'"],
        "short": ["INITSTATEMENT", "INITLIST'"]
    },

    "INITLIST'": {
        ",": [",", "INITSTATEMENT", "INITLIST'"],
        ")": ["ε"],
    },

    "CONDITIONAL": {
        "if": ["if", "(", "CONDITION", ")", "{", "STATEMENT", "}", "CONDITIONAL_ELSE"]
    },

    "CONDITIONAL_ELSE": {
        "else": ["else", "{", "STATEMENT", "}"],
        "$": ["ε"]
    },

    "LOOPSTATEMENT": {
        "for": ["FORLOOP"],
        "while": ["WHILELOOP"],
        "do": ["DOWHILELOOP"]
    },

    "FORLOOP": {
        "for": ["for", "(", "FORVAR", ";", "CONDITION", ";", "VARCHANGESTATEMENT", ")", "{", "STATEMENT", "}"]
    },

    "WHILELOOP": {
        "while": ["while", "(", "CONDITION", ")", "{", "STATEMENT", "}"]
    },

    "DOWHILELOOP": {
        "do": ["do", "{", "STATEMENT", "}", "while", "(", "CONDITION", ")"]
    },

    "RETURNSTATEMENT": {
        "return": ["return", "VARVAL", ";"],
        "$": ["ε"]
    },

    "VARVAL": {
        "ID": ["ARITH_EXPR"],
        "INTVAL": ["ARITH_EXPR"],
        "FLOATVAL": ["ARITH_EXPR"]
    },

    "ARITH_EXPR": {
        "ID": ["TERM", "ARITH_EXPR'"],
        "INTVAL": ["TERM", "ARITH_EXPR'"],
        "FLOATVAL": ["TERM", "ARITH_EXPR'"]
    },

    "ARITH_EXPR'": {
        "+": ["+", "TERM", "ARITH_EXPR'"],
        "-": ["-", "TERM", "ARITH_EXPR'"],
        "$": ["ε"]
    },

    "TERM": {
        "ID": ["FACTOR", "TERM'"],
        "INTVAL": ["FACTOR", "TERM'"],
        "FLOATVAL": ["FACTOR", "TERM'"]
    },

    "TERM'": {
        "*": ["*", "FACTOR", "TERM'"],
        "/": ["/", "FACTOR", "TERM'"],
        "$": ["ε"]
    },

    "FACTOR": {
        "ID": ["VARNAME"],
        "INTVAL": ["INTVAL"],
        "FLOATVAL": ["FLOATVAL"],
        "(": ["(", "ARITH_EXPR", ")"]
    },

    "INTINIT": {
        "int": ["int", "VARNAME", "INTLIST"],
    },

    "FLOATINIT": {
        "float": ["float", "VARNAME", "FLOATLIST"]
    },

    "INTLIST": {
        ",": [",", "VARNAME", "INTLIST"],
        "$": ["ε"]
    },

    "FLOATLIST": {
        ",": [",", "VARNAME", "FLOATLIST"],
        "$": ["ε"]
    },

    "SWITCHSTATEMENT": {
        "switch": ["switch", "(", "VARNAME", ")", "{", "SWITCHCASELIST", "}"]
    },

    "SWITCHCASELIST": {
        "case": ["SWITCHCASE", "SWITCHCASELIST'"],
        "default": ["DEFAULTCASE"]
    },

    "SWITCHCASELIST'": {
        "case": ["SWITCHCASE", "SWITCHCASELIST'"],
        "default": ["ε"]
    },

    "DEFAULTCASE": {
        "default": ["default:", "STATEMENT", "break;"]
    },

    "VARCHANGELINE": {
        "ID": ["VARCHANGESTATEMENT", ";"]
    },

    "VARCHANGESTATEMENT": {
        "ID": ["VARNAME", "VARIABLE_MODIFICATION"]
    },

    # Updated initialization rules for each type to allow assignment
    "INITSTATEMENT": [["INTINIT"], ["FLOATINIT"], ["CHARINIT"], ["STRINGINIT"], ["DOUBLEINIT"], ["LONGINIT"], ["SHORTINIT"]],


    "VARIABLE_MODIFICATION": {
        "++": ["++"],
        "--": ["--"],
        "=": ["=", "ARITH_EXPR"],
        "+=": ["+=", "ARITH_EXPR"],
        "-=": ["-=", "ARITH_EXPR"],
        "*=": ["*=", "ARITH_EXPR"],
        "/=": ["/=", "ARITH_EXPR"]
    },

    "KEYWORD": {
        "static": ["static"],
        "const": ["const"],
        "volatile": ["volatile"],
        "inline": ["inline"]
    }
}

print(parse(tokens,parse_table))