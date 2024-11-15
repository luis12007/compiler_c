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
        "void": ["INCLUDEBLOCK", "DEFINEBLOCK", "FUNCTIONBLOCK", "MAINFUNCTION"],
        "$": ["ɛ"]
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
        "#define": ["ɛ"],
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
    
    # added "$":["ɛ"]
    "FUNCTIONBLOCK": {
        "int": ["FUNCDEC", "FUNCTIONBLOCK"],
        "float": ["FUNCDEC", "FUNCTIONBLOCK"],
        "char": ["FUNCDEC", "FUNCTIONBLOCK"],
        "string": ["FUNCDEC", "FUNCTIONBLOCK"],
        "double": ["FUNCDEC", "FUNCTIONBLOCK"],
        "long": ["FUNCDEC", "FUNCTIONBLOCK"],
        "short": ["FUNCDEC", "FUNCTIONBLOCK"],
        "void": ["FUNCDEC", "FUNCTIONBLOCK"],
        "ɛ": [],
        "$":["ɛ"]
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
    
    # added "$":["ɛ"]
    "MAINFUNCTION": {
        "int": ["FUNCTYPE", "main", "(", "INITLIST", ")", "{", "STATEMENT", "RETURNSTATEMENT", "}"],
        "float": ["FUNCTYPE", "main", "(", "INITLIST", ")", "{", "STATEMENT", "RETURNSTATEMENT", "}"],
        "char": ["FUNCTYPE", "main", "(", "INITLIST", ")", "{", "STATEMENT", "RETURNSTATEMENT", "}"],
        "string": ["FUNCTYPE", "main", "(", "INITLIST", ")", "{", "STATEMENT", "RETURNSTATEMENT", "}"],
        "double": ["FUNCTYPE", "main", "(", "INITLIST", ")", "{", "STATEMENT", "RETURNSTATEMENT", "}"],
        "long": ["FUNCTYPE", "main", "(", "INITLIST", ")", "{", "STATEMENT", "RETURNSTATEMENT", "}"],
        "short": ["FUNCTYPE", "main", "(", "INITLIST", ")", "{", "STATEMENT", "RETURNSTATEMENT", "}"],
        "void": ["void", "main", "(", "INITLIST", ")", "{", "STATEMENT", "RETURNSTATEMENT", "}"],
        "$":["ɛ"]
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
        "int": ["INITLIST", "STATEMENT"],   
        "float": ["INITLIST", "STATEMENT"],   
        "double": ["INITLIST", "STATEMENT"],   
        "long": ["INITLIST", "STATEMENT"],   
        "short": ["INITLIST", "STATEMENT"],   
        "char": ["INITLIST", "STATEMENT"],   
        "string": ["INITLIST", "STATEMENT"],   
        "VARNAME": ["VARCHANGELINE", "STATEMENT"],
        "return": ["RETURNSTATEMENT", "STATEMENT"],
        "ɛ": [],                               # Allow the list to end on semicolon
        "}": ["ɛ"]
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
        "(": ["(", "CONDITION", ")"],
        "!": ["!", "CONDITION"],
        "true": ["true"],
        "false": ["false"],
        "0": ["0"],
        "INTVAL": ["SIMPLE_CONDITION"],
        "FLOATVAL": ["SIMPLE_CONDITION"]

    },

    #Changed to allow for multiple conditions
    "SIMPLE_CONDITION": {
    "VARNAME": ["EXPRESSION", "CONDOPERATOR", "EXPRESSION"],
    "INTVAL": ["EXPRESSION", "CONDOPERATOR", "EXPRESSION"],
    "FLOATVAL": ["EXPRESSION", "CONDOPERATOR", "EXPRESSION"]
    },

    "EXPRESSION": {
    "VARNAME": ["VARNAME"],
    "INTVAL": ["INTVAL"],
    "FLOATVAL": ["FLOATVAL"]
},


    "CONDOPERATOR": {
        "=": ["=", "="],
        "<": ["<", "OREQUAL"],
        ">": [">", "OREQUAL"],
        "*": ["*", "OREQUAL"],
    },

    "OREQUAL":{
        "ɛ": [],
        "=": ["="],
        "VARNAME": ["ɛ"],
        "INTVAL": ["ɛ"],
        "FLOATVAL": ["ɛ"]
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
    
    #Changing for ambiguity
    "DEFINESTATEMENT": {
    "#define": ["#define", "VARNAME", "DEFINEBODY"]
    },

    "DEFINEBODY": {
        "VARNAME": ["VARNAME"],                             
        "<": ["<", "VARNAME", ">", "VARNAME"],                          
        "{": ["{", "STATEMENT", "}"],                           
        "(": ["PARAM_MACRO_BODY"]                                      
    },

    # Added
    "PARAM_MACRO_BODY": {
        "(": ["(", "PARAMLIST", ")", "MACRO_BODY"]
    },


    "PARAMLIST": {
        "VARNAME": ["VARNAME", "PARAMLIST'"]                    # Start with one parameter and use recursion for more
    },

    "PARAMLIST'": {
        ",": [",", "VARNAME", "PARAMLIST'"],                    # Allows additional parameters separated by commas
        ")": ["ɛ"]                                              # Ends the parameter list
    },

    "MACRO_BODY": {
        "for": ["for", "(", "FORVAR",";", "CONDITION", ";", "VARCHANGESTATEMENT", ")"],
        "(": ["(", "CONDITION", ")"],
    },

    # CHANGED
    "RETURNSTATEMENT": {
    "return": ["return", "OPTIONAL_VARVAL", ";"],
    "}": ["ɛ"]                    
    },

    "OPTIONAL_VARVAL": {
    "VARNAME": ["ARITH_EXPR"],    
    "INTVAL": ["ARITH_EXPR"],       
    "FLOATVAL": ["ARITH_EXPR"],    
    "CHARVAL": ["ARITH_EXPR"],      
    "STRINGVAL": ["ARITH_EXPR"],   
    "DOUBLEVAL": ["ARITH_EXPR"],      
    "(": ["ARITH_EXPR"],             
    "ɛ": [],
    ";": ["ɛ"]                    
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
        "ɛ": [],
        ")": ["ɛ"]
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
    

    # INTINIT updated
    "INTINIT": {
        "int": ["int", "VARNAME", "INTLIST_NO_ASSIGNMENT_OR_WITH_ASSIGNMENT"],
        ";": ["ɛ"]  # Allow the list to end on semicolon
    },
    
    # FLOATINIT updated
    "FLOATINIT": {
        "float": ["float", "VARNAME", "FLOATLIST_NO_ASSIGNMENT_OR_WITH_ASSIGNMENT"],
        ";": ["ɛ"]
    },
    
    # CHARINIT updated
    "CHARINIT": {
        "char": ["char", "VARNAME", "CHARLIST_NO_ASSIGNMENT_OR_WITH_ASSIGNMENT"],
        ";": ["ɛ"]
    },
    
    # STRINGINIT updated
    "STRINGINIT": {
        "string": ["string", "VARNAME", "STRINGLIST_NO_ASSIGNMENT_OR_WITH_ASSIGNMENT"],
        ";": ["ɛ"]
    },
    
    # DOUBLEINIT updated
    "DOUBLEINIT": {
        "double": ["double", "VARNAME", "DOUBLELIST_NO_ASSIGNMENT_OR_WITH_ASSIGNMENT"],
        ";": ["ɛ"]
    },
    
    # LONGINIT updated
    "LONGINIT": {
        "long": ["long", "VARNAME", "LONGLIST_NO_ASSIGNMENT_OR_WITH_ASSIGNMENT"],
        ";": ["ɛ"]
    },
    
    # SHORTINIT updated
    "SHORTINIT": {
        "short": ["short", "VARNAME", "SHORTLIST_NO_ASSIGNMENT_OR_WITH_ASSIGNMENT"],
        ";": ["ɛ"]
    },
    
    # INTLIST_NO_ASSIGNMENT_OR_WITH_ASSIGNMENT
    "INTLIST_NO_ASSIGNMENT_OR_WITH_ASSIGNMENT": {
        "=": ["=", "INTVAL", "INTLIST"],
        ",": ["INTLIST"],
        ")": ["ɛ"],
        "ɛ": []
    },
    
    # FLOATLIST_NO_ASSIGNMENT_OR_WITH_ASSIGNMENT
    "FLOATLIST_NO_ASSIGNMENT_OR_WITH_ASSIGNMENT": {
        "=": ["=", "FLOATVAL", "FLOATLIST"],
        ",": ["FLOATLIST"],
        ")": ["ɛ"],
        "ɛ": []
    },
    
    # CHARLIST_NO_ASSIGNMENT_OR_WITH_ASSIGNMENT
    "CHARLIST_NO_ASSIGNMENT_OR_WITH_ASSIGNMENT": {
        "=": ["=", "CHARVAL", "CHARLIST"],
        ",": ["CHARLIST"],
        ")": ["ɛ"],
        "ɛ": []
    },
    
    # STRINGLIST_NO_ASSIGNMENT_OR_WITH_ASSIGNMENT
    "STRINGLIST_NO_ASSIGNMENT_OR_WITH_ASSIGNMENT": {
        "=": ["=", "STRINGVAL", "STRINGLIST"],
        ",": ["STRINGLIST"],
        ")": ["ɛ"],
        "ɛ": []
    },
    
    # DOUBLELIST_NO_ASSIGNMENT_OR_WITH_ASSIGNMENT
    "DOUBLELIST_NO_ASSIGNMENT_OR_WITH_ASSIGNMENT": {
        "=": ["=", "DOUBLEVAL", "DOUBLELIST"],
        ",": ["DOUBLELIST"],
        ")": ["ɛ"],
        "ɛ": []
    },
    
    # LONGLIST_NO_ASSIGNMENT_OR_WITH_ASSIGNMENT
    "LONGLIST_NO_ASSIGNMENT_OR_WITH_ASSIGNMENT": {
        "=": ["=", "INTVAL", "LONGLIST"],
        ",": ["LONGLIST"],
        ")": ["ɛ"],
        "ɛ": []
    },
    
    # SHORTLIST_NO_ASSIGNMENT_OR_WITH_ASSIGNMENT
    "SHORTLIST_NO_ASSIGNMENT_OR_WITH_ASSIGNMENT": {
        "=": ["=", "INTVAL", "SHORTLIST"],
        ",": ["SHORTLIST"],
        ")": ["ɛ"],
        "ɛ": []
    },
    
    # INTLIST with semicolon handling
    "INTLIST": {
        ",": [",", "VARNAME", "INTLIST"],
        "=": ["=", "INTVAL", "INTLIST"],
        ";": ["ɛ"],
        "ɛ": []
    },
    
    # FLOATLIST with semicolon handling
    "FLOATLIST": {
        ",": [",", "VARNAME", "FLOATLIST"],
        "=": ["=", "FLOATVAL", "FLOATLIST"],
        ";": ["ɛ"],
        "ɛ": []
    },
    
    # CHARLIST with semicolon handling
    "CHARLIST": {
        ",": [",", "VARNAME", "CHARLIST"],
        "=": ["=", "CHARVAL", "CHARLIST"],
        ";": ["ɛ"],
        "ɛ": []
    },
    
    # STRINGLIST with semicolon handling
    "STRINGLIST": {
        ",": [",", "VARNAME", "STRINGLIST"],
        "=": ["=", "STRINGVAL", "STRINGLIST"],
        ";": ["ɛ"],
        "ɛ": []
    },
    
    # DOUBLELIST with semicolon handling
    "DOUBLELIST": {
        ",": [",", "VARNAME", "DOUBLELIST"],
        "=": ["=", "DOUBLEVAL", "DOUBLELIST"],
        ";": ["ɛ"],
        "ɛ": []
    },
    
    # LONGLIST with semicolon handling
    "LONGLIST": {
        ",": [",", "VARNAME", "LONGLIST"],
        "=": ["=", "INTVAL", "LONGLIST"],
        ";": ["ɛ"],
        "ɛ": []
    },
    
    # SHORTLIST with semicolon handling
    "SHORTLIST": {
        ",": [",", "VARNAME", "SHORTLIST"],
        "=": ["=", "INTVAL", "SHORTLIST"],
        ";": ["ɛ"],
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
        "ɛ": [],
        ";": ["ɛ"]
    },
    
    "TERM": {
        "VARNAME": ["FACTOR", "TERM'"],
        "INTVAL": ["FACTOR", "TERM'"],
        "FLOATVAL": ["FACTOR", "TERM'"],
        "CHARVAL": ["FACTOR", "TERM'"],
        "STRINGVAL": ["FACTOR", "TERM'"],
        "DOUBLEVAL": ["FACTOR", "TERM'"],
        "(": ["FACTOR", "TERM'"],
        ";": ["ɛ"],

    },
    
    "TERM'": {
        "*": ["*", "FACTOR", "TERM'"],
        "/": ["/", "FACTOR", "TERM'"],
        "ɛ": [],
        ";": ["ɛ"]
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
        "INTVAL": ["INTVAL", "FLOAT_AUX"],
        "[0-9][0-9]*f": ["[0-9][0-9]*f"]
    },

    "FLOAT_AUX":{
        ".": [".", "FLOAT_AUX"],
        "ɛ": [],
        "INTVAL": ["INTVAL"],
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
        "VARNAME": ["VARNAME", "VARIABLE_MODIFICATION"],
        "+": ["VARIABLE_MODIFICATION", "VARNAME"],                   # Handles prefix increment (e.g., ++VARNAME)
        "-": ["VARIABLE_MODIFICATION", "VARNAME"]   
    },
    
    "VARIABLE_MODIFICATION": {
        "+": ["+", "MOD_EQUAL"],
        "-": ["-", "MOD_EQUAL"],
        "*": ["*", "MOD_EQUAL"],
        "/": ["/", "MOD_EQUAL"],
        "=": ["=", "ARITH_EXPR"],
        "++": ["++"],
        "--": ["--"]
    },

    "MOD_EQUAL": {
        "ɛ": [],
        "=": ["="],
        "+": ["+"],
        "-": ["-"],

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
