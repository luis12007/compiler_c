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
    # Existing entries (# means comment and edditions) 
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
    
    # added voids
    "INCLUDEBLOCK": {
        "#include": ["INCLUDESTATEMENT", "INCLUDEBLOCK"],
        "int": ["ɛ"],
        "float": ["ɛ"],
        "char": ["ɛ"],
        "string": ["ɛ"],
        "double": ["ɛ"],
        "long": ["ɛ"],
        "short": ["ɛ"],
        "void": ["ɛ"],
        "#define": ["ɛ"] 
    },
    
    # added voids
    "DEFINEBLOCK": {
        "#define": ["DEFINESTATEMENT", "DEFINEBLOCK"],
        "int": ["ɛ"],
        "float": ["ɛ"],
        "char": ["ɛ"],
        "string": ["ɛ"],
        "double": ["ɛ"],
        "long": ["ɛ"],
        "short": ["ɛ"],
        "void": ["ɛ"],
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

    # New rules for FUNCDEC, FUNCTYPE, and FUNCTION they were missing
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
    
    "FUNCTION": {
        "VARNAME": ["VARNAME", "(", "INITLIST", ")", "{", "STATEMENT", "RETURNSTATEMENT", "}"]
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
    
    # Changed to allow for multiple statements like int, float, char, etc.
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
        "int": ["INITLIST", "STATEMENT"],    # Added int for variable declaration # TODO: add more
        "VARNAME": ["VARCHANGELINE", "STATEMENT"],
        "return": ["RETURNSTATEMENT", "STATEMENT"],
        "ɛ": [],                           # Allow the list to end on semicolon
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
    
    #TODO: ADD CONDITION TO CURRENT LL1 GRAMMAR
    "FORLOOP": {
        "for": ["for", "(", "FORVAR", ";", "CONDITION", ";", "VARCHANGESTATEMENT", ")", "{", "STATEMENT", "}"]
    },

    #Added CONDITION FOR 
    "CONDITION": {
        "VARNAME": ["SIMPLE_CONDITION"],
        "(": ["LOGICAL_CONDITION"],
        "!": ["NEGATION"]
    },

    "SIMPLE_CONDITION": {
        "VARNAME": ["VARNAME", "CONDOPERATOR", "VARNAME"],
        "VARVAL": ["VARNAME", "CONDOPERATOR", "VARVAL", "VARVAL", "CONDOPERATOR", "VARNAME", "VARVAL", "CONDOPERATOR", "VARVAL"]
    },

    "LOGICAL_CONDITION": {
        "(": ["(", "LOGICAL_EXPR", ")"]
    },

    "LOGICAL_EXPR": {
        "0": ["LOGICAL_VAL", "+", "LOGICAL_VAL"],
        "1": ["LOGICAL_VAL", "+", "LOGICAL_VAL"],
        "true": ["LOGICAL_VAL", "+", "LOGICAL_VAL"],
        "false": ["LOGICAL_VAL", "+", "LOGICAL_VAL"]
    },

    "LOGICAL_VAL": {
        "0": ["0"],
        "1": ["1"],
        "true": ["true"],
        "false": ["false"]
    },

    "NEGATION": {
        "!": ["!", "CONDITION"]
    },

    "CONDOPERATOR": {
        "==": ["=="],
        "<": ["<"],
        "<=": ["<="],
        ">": [">"],
        ">=": [">="]
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
    "[a-zA-Z_][a-zA-Z0-9_]*": ["ε"]
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
        "ɛ": []
    },
    
    # Shrinked 
    "INITLIST'": {
        ",": ["INITSTATEMENT", "INITLIST'"],  # Continue with additional declarations
        ")": ["ɛ"],
        ";": ["ɛ"],                             # Allow the list to end on semicolon
        "ɛ": []  # Allows the parameter list to end without requiring assignment
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
        "int": ["int", "VARNAME", "INTLIST_NO_ASSIGNMENT_OR_WITH_ASSIGNMENT"],
        ";": ["ɛ"],                             # Allow the list to end on semicolon
    },

    # Added `INTLIST_WITH_ASSIGNMENT` to handle cases with initial assignment
    "INTLIST_NO_ASSIGNMENT_OR_WITH_ASSIGNMENT": {
        "=": ["=", "INTVAL", "INTLIST"],  # Allow assignment
        ",": ["INTLIST"],                 # Continue declaration list without assignment
        ")": ["ɛ"],                       # Recognize end of parameter list in functions
        "ɛ": []                           # Allow an empty list if no assignment or additional items
    },

    # allow ; to end the list
    "INTLIST": {
        ",": [",", "VARNAME", "INTLIST"],            # Additional declarations without assignment
        "=": [",", "VARNAME", "=", "INTVAL", "INTLIST"],  # Additional declarations with assignment
        ";": ["ɛ"],                             # Allow the list to end on semicolon
        "ɛ": []                                      # Allows the list to end without further entries
        
    },
    
    #TODO: change for each one of them
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
