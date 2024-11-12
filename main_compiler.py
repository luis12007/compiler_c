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
        "#define": ["DEFINEBLOCK", "FUNCTIONBLOCK", "MAINFUNCTION"],
        "int": ["FUNCTIONBLOCK", "MAINFUNCTION"],
        "float": ["FUNCTIONBLOCK", "MAINFUNCTION"],
        "char": ["FUNCTIONBLOCK", "MAINFUNCTION"],
        "string": ["FUNCTIONBLOCK", "MAINFUNCTION"],
        "double": ["FUNCTIONBLOCK", "MAINFUNCTION"],
        "long": ["FUNCTIONBLOCK", "MAINFUNCTION"],
        "short": ["FUNCTIONBLOCK", "MAINFUNCTION"],
        "void": ["MAINFUNCTION"],
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
        "#include": ["ε"],
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
        "#include": ["ε"],
        "#define": ["ε"],
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
    "MAINFUNCTION": {
        "int": ["FUNCTYPE", "main", "(", "INITLIST", ")", "{", "STATEMENT", "RETURNSTATEMENT", "}"],
        "void": ["void", "main", "(", "INITLIST", ")", "{", "STATEMENT", "RETURNSTATEMENT", "}"],
    },
    "INCLUDESTATEMENT": {
        "#include": ["#include", "<", "VARNAME", ">"],
    },
    "DEFINESTATEMENT": {
        "#define": ["#define", "VARNAME", "VARNAME"],
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
        "while": ["LOOPSTATEMENT", "STATEMENT"],
        "do": ["LOOPSTATEMENT", "STATEMENT"],
        "ID": ["VARCHANGELINE", "STATEMENT"],
        "return": ["RETURNSTATEMENT", "STATEMENT"],
        "}": ["ε"]
    },
    "INITLINE": {
        "int": ["KEYWORD", "INITSTATEMENT"],
        "float": ["KEYWORD", "INITSTATEMENT"],
        "char": ["KEYWORD", "INITSTATEMENT"],
        "string": ["KEYWORD", "INITSTATEMENT"],
        "double": ["KEYWORD", "INITSTATEMENT"],
        "long": ["KEYWORD", "INITSTATEMENT"],
        "short": ["KEYWORD", "INITSTATEMENT"],
    },
    "KEYWORD": {
        "static": ["static"],
        "const": ["const"],
        "volatile": ["volatile"],
        "inline": ["inline"],
        "int": ["ε"],
        "float": ["ε"],
        "char": ["ε"],
        "string": ["ε"],
        "double": ["ε"],
        "long": ["ε"],
        "short": ["ε"]
    },
    "INITSTATEMENT": {
        "int": ["INTINIT"],
        "float": ["FLOATINIT"],
        "char": ["CHARINIT"],
        "string": ["STRINGINIT"],
        "double": ["DOUBLEINIT"],
        "long": ["LONGINIT"],
        "short": ["SHORTINIT"],
    },
    "INTINIT": {
        "int": ["int", "VARNAME", "INTLIST"],
    },
    "FLOATINIT": {
        "float": ["float", "VARNAME", "FLOATLIST"],
    },
    "CHARINIT": {
        "char": ["char", "VARNAME", "CHARLIST"],
    },
    "STRINGINIT": {
        "string": ["string", "VARNAME", "STRINGLIST"],
    },
    "DOUBLEINIT": {
        "double": ["double", "VARNAME", "DOUBLELIST"],
    },
    "LONGINIT": {
        "long": ["long", "VARNAME", "LONGLIST"],
    },
    "SHORTINIT": {
        "short": ["short", "VARNAME", "SHORTLIST"],
    },
    "VARNAME": {
        "ID": ["ID"],
    },
    "SWITCHSTATEMENT": {
        "switch": ["switch", "(", "VARNAME", ")", "{", "SWITCHCASELIST", "}"],
    },
    "SWITCHCASELIST": {
        "case": ["SWITCHCASE", "SWITCHCASELIST'", "DEFAULTCASE"],
    },
    "SWITCHCASELIST'": {
        "case": ["SWITCHCASE", "SWITCHCASELIST'"],
        "default": ["ε"]
    },
    "DEFAULTCASE": {
        "default": ["default:", "STATEMENT", "break;"],
    },
    "CONDITIONAL": {
        "if": ["if", "(", "CONDITION", ")", "{", "STATEMENT", "}", "CONDITIONAL_ELSE"],
    },
    "CONDITIONAL_ELSE": {
        "else": ["else", "{", "STATEMENT", "}"],
        "}": ["ε"]
    },
    "LOOPSTATEMENT": {
        "for": ["FORLOOP"],
        "while": ["WHILELOOP"],
        "do": ["DOWHILELOOP"],
    },
    "FORLOOP": {
        "for": ["for", "(", "FORVAR", ";", "CONDITION", ";", "VARCHANGESTATEMENT", ")", "{", "STATEMENT", "}"],
    },
    "WHILELOOP": {
        "while": ["while", "(", "CONDITION", ")", "{", "STATEMENT", "}"],
    },
    "DOWHILELOOP": {
        "do": ["do", "{", "STATEMENT", "}", "while", "(", "CONDITION", ")"],
    },
    "VARCHANGESTATEMENT": {
        "ID": ["VARNAME", "VARIABLE_MODIFICATION"]
    },
    "RETURNSTATEMENT": {
        "return": ["return", "VARVAL", ";"],
    },
    # Remaining arithmetic expressions and value types based on provided rules
    "VARVAL": {
        "ID": ["ARITH_EXPR"],
        "INTVAL": ["ARITH_EXPR"],
        "FLOATVAL": ["ARITH_EXPR"],
        "CHARVAL": ["ARITH_EXPR"],
        "STRINGVAL": ["ARITH_EXPR"],
        "DOUBLEVAL": ["ARITH_EXPR"],
        "(": ["ARITH_EXPR"]
    },
    "ARITH_EXPR": {
        "ID": ["TERM", "ARITH_EXPR'"],
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
        ")": ["ε"],
        ";": ["ε"]
    },
    "TERM": {
        "ID": ["FACTOR", "TERM'"],
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
        "+": ["ε"],
        "-": ["ε"],
        ")": ["ε"],
        ";": ["ε"]
    },
    "FACTOR": {
        "ID": ["VARNAME"],
        "INTVAL": ["INTVAL"],
        "FLOATVAL": ["FLOATVAL"],
        "CHARVAL": ["CHARVAL"],
        "STRINGVAL": ["STRINGVAL"],
        "DOUBLEVAL": ["DOUBLEVAL"],
        "(": ["(", "ARITH_EXPR", ")"]
    },
}

print(parse(tokens,parse_table))