from lexer import lexer
from parser_tokens import parse, variable_parse, variable_print, Var
from printer import process_syntax_tree
from SemanticAnalyzer import semantic_analysis
from parser_without_errors import parse_without_errors

def compile(source, flag):
    # Leer el archivo source_code.c
    with open(source, 'r') as file:
        codigo = file.read()

    """ -----------------------------LEXER-------------------------------------- """
    tokens = lexer(codigo)
    tokens2 = tokens.copy() 
    """ -----------------------------PARSER------------------------------------- """
    Grammar_table = {
        # Existing entries (# means comment and edditions) 
        "SOURCE": {
            "#include": ["SOURCEBLOCK", "MAINFUNCTION"],
            "#define": ["SOURCEBLOCK", "MAINFUNCTION"],
            "int": ["SOURCEBLOCK", "MAINFUNCTION"],
            "float": ["SOURCEBLOCK", "MAINFUNCTION"],
            "char": ["SOURCEBLOCK", "MAINFUNCTION"],
            "string": ["SOURCEBLOCK", "MAINFUNCTION"],
            "double": ["SOURCEBLOCK", "MAINFUNCTION"],
            "long": ["SOURCEBLOCK", "MAINFUNCTION"],
            "short": ["SOURCEBLOCK", "MAINFUNCTION"],
            "void": ["SOURCEBLOCK", "MAINFUNCTION"],
            "$": ["ɛ"]
        },

        "SOURCEBLOCK":{
            "#include": ["INCLUDEBLOCK", "SOURCEBLOCK"],
            "#define": ["DEFINEBLOCK", "SOURCEBLOCK"],
            "int": ["FUNCTIONBLOCK", "SOURCEBLOCK"],
            "float": ["FUNCTIONBLOCK", "SOURCEBLOCK"],
            "char": ["FUNCTIONBLOCK", "SOURCEBLOCK"],
            "string": ["FUNCTIONBLOCK", "SOURCEBLOCK"],
            "double": ["FUNCTIONBLOCK", "SOURCEBLOCK"],
            "long": ["FUNCTIONBLOCK", "SOURCEBLOCK"],
            "short": ["FUNCTIONBLOCK", "SOURCEBLOCK"],
            "void": ["FUNCTIONBLOCK", "SOURCEBLOCK"],
            "main": ["ɛ"],
            "$": ["ɛ"],
            "ɛ": []
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
            "main": ["ɛ"],
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
            "void": ["FUNCTYPE", "VOID_FUNCTION"]
        },

        "VOID_FUNCTION":{
            "VARNAME": ["VARNAME", "(", "FUNCINIT", ")", "{", "STATEMENT", "VOID_RETURN", "}"],
            "main": ["ɛ"]
        },

        "VOID_RETURN": {
            "return": ["return", ";"],
            "}": ["ɛ"]
        },

        "FUNCINIT": {
            "int": ["FUNCINITSTATEMENT", "FUNCINIT'"],
            "float": ["FUNCINITSTATEMENT", "FUNCINIT'"],
            "char": ["FUNCINITSTATEMENT", "FUNCINIT'"],
            "string": ["FUNCINITSTATEMENT", "FUNCINIT'"],
            "double": ["FUNCINITSTATEMENT", "FUNCINIT'"],
            "long": ["FUNCINITSTATEMENT", "FUNCINIT'"],
            "short": ["FUNCINITSTATEMENT", "FUNCINIT'"],
            "ɛ": [],
            ")": ["ɛ"]
        },
        
        # Shrinked 
        "FUNCINIT'": {
            ",": [",", "FUNCINITSTATEMENT", "FUNCINIT'"],  # Continue with additional declarations
            ")": ["ɛ"],
            "ɛ": []  # Allows the parameter list to end without requiring assignment
        },
        
        "FUNCINITSTATEMENT": {
            "int": ["FUNCINTINIT"],
            "float": ["FUNCFLOATINIT"],
            "char": ["FUNCCHARINIT"],
            "string": ["FUNCSTRINGINIT"],
            "double": ["FUNCDOUBLEINIT"],
            "long": ["FUNCLONGINIT"],
            "short": ["FUNCSHORTINIT"]
        },

        "FUNCINTINIT": {
            "int": ["int", "VARNAME", "FUNCINTAUX"],
            ")": ["ɛ"]
        },

        "FUNCINTAUX":{
            ",":["ɛ"],
            ")":["ɛ"],
            "=":["=", "INTVAL", "FUNCINTAUX"]
        },
        
        "FUNCFLOATINIT": {
            "float": ["float", "VARNAME", "FUNCFLOATAUX"],
            ")": ["ɛ"]
        },

        "FUNCFLOATAUX":{
            ",":["ɛ"],
            ")":["ɛ"],
            "=":["=", "FLOATVAL", "FUNCFLOATAUX"]
        },
        
        "FUNCCHARINIT": {
            "char": ["char", "VARNAME", "FUNCCHARAUX"],
            ";": ["ɛ"]
        },

        "FUNCCHARAUX":{
            ",":["ɛ"],
            ")":["ɛ"],
            "=":["=", "CHARVAL", "FUNCCHARAUX"]
        },
        
        "FUNCSTRINGINIT": {
            "string": ["string", "VARNAME", "FUNCSTRINGAUX"],
            ")": ["ɛ"]
        },

        "FUNCSTRINGAUX":{
            ",":["ɛ"],
            ")":["ɛ"],
            "=":["=", "STRINGVAL", "FUNCSTRINGAUX"]
        },
        
        "FUNCDOUBLEINIT": {
            "double": ["double", "VARNAME", "FUNCDOUBLEAUX"],
            ")": ["ɛ"]
        },

        "FUNCDOUBLEAUX":{
            ",":["ɛ"],
            ")":["ɛ"],
            "=":["=", "DOUBLEVAL", "FUNCDOUBLEAUX"]
        },
        
        "FUNCLONGINIT": {
            "long": ["long", "VARNAME", "FUNCLONGAUX"],
            ")": ["ɛ"]
        },

        "FUNCLONGAUX":{
            ",":["ɛ"],
            ")":["ɛ"],
            "=":["=", "LONGVAL", "FUNCLONGAUX"]
        },
        
        "FUNCSHORTINIT": {
            "short": ["short", "VARNAME", "FUNCSHORTAUX"],
            ")": ["ɛ"]
        },

        "FUNCSHORTAUX":{
            ",":["ɛ"],
            ")":["ɛ"],
            "=":["=", "SHORTVAL", "FUNCSHORTAUX"]
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
            "VARNAME": ["VARNAME", "(", "FUNCINIT", ")", "{", "STATEMENT", "RETURNSTATEMENT", "}"],
            "main": ['ɛ']
        },
        
        # added "$":["ɛ"]
        "MAINFUNCTION": {
            "main": ["main", "(", "FUNCINIT", ")", "{", "STATEMENT", "RETURNSTATEMENT", "}", "SOURCEBLOCK"],
            "$":["ɛ"]
        },
        
        # Changed to allow for multiple statements like int, float, char, etc.
        "STATEMENT": {
            "static": ["INITLINE", "STATEMENT"],
            "const": ["INITLINE", "STATEMENT"],
            "volatile": ["INITLINE", "STATEMENT"],
            "inline": ["INITLINE", "STATEMENT"],
            "if": ["IF", "STATEMENT"],
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
            "VARNAME": ["VARNAME", "VARNAMELINE", "STATEMENT"],
            "+": ["VARCHANGESTATEMENT", "STATEMENT"],
            "-": ["VARCHANGESTATEMENT", "STATEMENT"],
            "return": ["ɛ"],
            "break": ["break", ";", "STATEMENT"],
            "case": ["ɛ"],
            "default": ["ɛ"],
            "}": ["ɛ"],
            "ɛ": []                               # Allow the list to end on semicolon
        },

        "IF":{
            "if": ["if", "(", "CONDITION", ")", "{", "STATEMENT", "}", "ELSE"]
        },

        "ELSE":{
            "else": ["else", "ELSEIF"],
            "ɛ": []
        },

        "ELSEIF":{
            "if": ["if", "(", "CONDITION", ")", "{", "STATEMENT", "}", "ELSE"],
            "{": ["{", "STATEMENT", "}"]
        },
        
        "SWITCHSTATEMENT": {
            "switch": ["switch", "(", "VARNAME", ")", "{", "SWITCHCASELIST", "}"]
        },
        
        "SWITCHCASELIST": {
            "case": ["case", "FACTOR", ":", "STATEMENT", "SWITCHCASELIST"],
            "default": ["DEFAULTCASE"]
        },
        
        "DEFAULTCASE": {
            "default": ["default", ":", "STATEMENT"],
            "}": ["ɛ"]
        },
        
        #TODO: ADD CONDITION TO CURRENT LL1 GRAMMAR
        "FORLOOP": {
            "for": ["for", "(", "FORVAR", ";", "CONDITION", ";", "VARCHANGESTATEMENT", ")", "{", "STATEMENT", "}", "STATEMENT"]
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
        "INTVAL": ["INTVAL", "FLOAT_AUX"],
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

        "PARAM_MACRO_BODY": {
            "(": ["(", "PARAMLIST", ")", "MACRO_BODY"]
        },

        "PARAMLIST": {
            "VARNAME": ["VARNAME", "PARAMLIST'"],                   # Start with one parameter and use recursion for more
            "INTVAL": ["ARITH_EXPR", "PARAMLIST'"],
            "FLOATVAL": ["ARITH_EXPR", "PARAMLIST'"],
            "CHARVAL": ["ARITH_EXPR", "PARAMLIST'"],
            "STRINGVAL": ["ARITH_EXPR", "PARAMLIST'"],
            "DOUBLEVAL": ["ARITH_EXPR", "PARAMLIST'"],
        },

        "PARAMLIST'": {
            ",": [",", "PARAMLIST"],                    # Allows additional parameters separated by commas
            ")": ["ɛ"]                                              # Ends the parameter list
        },

        "MACRO_BODY": {
            "for": ["for", "(", "FORVAR",";", "CONDITION", ";", "VARCHANGESTATEMENT", ")"],
            "(": ["(", "CONDITION", ")"],
        },

        # CHANGED
        "RETURNSTATEMENT": {
            "return": ["return", "OPTIONAL_VARVAL", ";"]
        },

        "OPTIONAL_VARVAL": {
            "VARNAME": ["VARNAME", "EXPRESSION_TAIL"],    
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
            "int": ["INITSTATEMENT", "INITLIST'", ";"],
            "float": ["INITSTATEMENT", "INITLIST'", ";"],
            "char": ["INITSTATEMENT", "INITLIST'", ";"],
            "string": ["INITSTATEMENT", "INITLIST'", ";"],
            "double": ["INITSTATEMENT", "INITLIST'", ";"],
            "long": ["INITSTATEMENT", "INITLIST'", ";"],
            "short": ["INITSTATEMENT", "INITLIST'", ";"],
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
        "FLOATINIT": {  # Entry point for `float` declarations
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
        
        #----------------------#
        # INTLIST_NO_ASSIGNMENT_OR_WITH_ASSIGNMENT updated
        "INTLIST_NO_ASSIGNMENT_OR_WITH_ASSIGNMENT": {
            "=": ["=", "EXPRESSION_INT", "INTLIST"], 
            ",": [",", "VARNAME", "INTLIST_NO_ASSIGNMENT_OR_WITH_ASSIGNMENT"],  
            ";": [";"],  
            "ɛ": []
        },
        # EXPRESSION added (New Rule)
        "EXPRESSION_INT": {
            "VARNAME": ["TERM_INT", "EXPRESSION_TAIL"], 
            "INTVAL": ["TERM_INT", "EXPRESSION_TAIL"], 
            "(": ["(", "EXPRESSION_INT", ")", "EXPRESSION_TAIL"],
            ",": ["ɛ"],
        },

        "TERM_INT": {
            "VARNAME": ["VARNAME"],
            "[0-9][0-9]*": ["[0-9][0-9]*"],
            "-": ["ɛ"],
            "+": ["ɛ"],
            "-": ["ɛ"],
            "*": ["ɛ"],
            "/": ["ɛ"],
            "^": ["ɛ"] 
        },

        "EXPRESSION_TAIL": {
            "+": ["OPERATOR", "TERM_INT", "EXPRESSION_TAIL"],
            "-": ["OPERATOR", "TERM_INT", "EXPRESSION_TAIL"],
            "*": ["OPERATOR", "TERM_INT", "EXPRESSION_TAIL"],
            "/": ["OPERATOR", "TERM_INT", "EXPRESSION_TAIL"],
            "^": ["OPERATOR", "TERM_INT", "EXPRESSION_TAIL"],
            ";": ["ɛ"],  
            "ɛ": ["ɛ"],
            ",": ["ɛ"],
            ".": ["OPERATOR", "TERM_INT", "EXPRESSION_TAIL"]
        },

        "OPERATOR": {
            "+": ["+"],
            "-": ["-"],
            "*": ["*"],
            "/": ["/"],
            "^": ["^"],
            ".": ["."]
        },
        #----------------------#
        
        # FLOATLIST_NO_ASSIGNMENT_OR_WITH_ASSIGNMENT
        "FLOATLIST_NO_ASSIGNMENT_OR_WITH_ASSIGNMENT": {  
            "=": ["=", "EXPRESSION_FLOAT", "FLOATLIST"],  
            ",": ["FLOATLIST"],
            ")": ["ɛ"],
            "ɛ": []
        },
        
        "EXPRESSION_FLOAT": {
            "VARNAME": ["TERM_FLOAT", "EXPRESSION_TAIL_FLOAT"], 
            "INTVAL": ["TERM_FLOAT", "EXPRESSION_TAIL_FLOAT"], 
            "(": ["(", "EXPRESSION_FLOAT", ")", "EXPRESSION_TAIL_FLOAT"],
            ",": ["ɛ"],
        },

        "EXPRESSION_TAIL_FLOAT": {
            "+": ["OPERATOR", "TERM_FLOAT", "EXPRESSION_TAIL_FLOAT"],
            "-": ["OPERATOR", "TERM_FLOAT", "EXPRESSION_TAIL_FLOAT"],
            "*": ["OPERATOR", "TERM_FLOAT", "EXPRESSION_TAIL_FLOAT"],
            "/": ["OPERATOR", "TERM_FLOAT", "EXPRESSION_TAIL_FLOAT"],
            "^": ["OPERATOR", "TERM_FLOAT", "EXPRESSION_TAIL_FLOAT"],
            ";": ["ɛ"],  
            "ɛ": ["ɛ"],
            ",": ["ɛ"],
            ".": ["OPERATOR", "TERM_INT", "EXPRESSION_TAIL"]
        },

        "TERM_FLOAT": {
            "VARNAME": ["VARNAME"],
            "INTVAL": ["FLOATVAL"],
            "-": ["ɛ"],
            "+": ["ɛ"],
            "-": ["ɛ"],
            "*": ["ɛ"],
            "/": ["ɛ"],
            "^": ["ɛ"] 
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
            "*": ["*", "TERM", "ARITH_EXPR'"],
            "/": ["/", "TERM", "ARITH_EXPR'"],
            ";": ["ɛ"],
            ")": ["ɛ"],
            "(": ["(", "PARAMLIST", ")"],
            "ɛ": []
        },
        
        "TERM": {
            "VARNAME": ["FACTOR"],
            "INTVAL": ["FACTOR"],
            "FLOATVAL": ["FACTOR"],
            "CHARVAL": ["FACTOR"],
            "STRINGVAL": ["FACTOR"],
            "DOUBLEVAL": ["FACTOR"],
            "(": ["FACTOR"],
            ";": ["ɛ"],
        },
        
        "FACTOR": {
            "VARNAME": ["VARNAME"],
            "INTVAL": ["INTVAL", "FLOAT_AUX"],
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
            "INTVAL": ["INTVAL"],
            "[0-9][0-9]*f": ["[0-9][0-9]*f"],
            ";": ["ɛ"],
            "}": ["ɛ"],
            ")": ["ɛ"],
            "ɛ": [],
            "+": ["ɛ"],
            "-": ["ɛ"],
            "*": ["ɛ"],
            "/": ["ɛ"],
            "^": ["ɛ"]  

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

        "VARNAMELINE":{
            "(":["(", "PARAMLIST", ")", ";"],
            "+":["VARCHANGESTATEMENT", ";"],
            "-":["VARCHANGESTATEMENT", ";"],
            "=":["VARCHANGESTATEMENT", ";"]
        },
        
        "VARCHANGESTATEMENT": {
            "VARNAME": ["VARNAME", "VARIABLE_MODIFICATION"],
            "+": ["VARIABLE_MODIFICATION", "VARNAME"],                   # Handles prefix increment (e.g., ++VARNAME)
            "-": ["VARIABLE_MODIFICATION", "VARNAME"],
            "=": ["VARIABLE_MODIFICATION"]
        },
        
        "VARIABLE_MODIFICATION": {
            "+": ["+", "MOD_EQUAL"],
            "-": ["-", "MOD_EQUAL"],
            "*": ["*", "MOD_EQUAL"],
            "/": ["/", "MOD_EQUAL"],
            "=": ["=", "ARITH_EXPR"]
        },

        "MOD_EQUAL": {
            "ɛ": [],
            "=": ["="],
            "+": ["+"],
            "-": ["-"],

        }
    }

    # parse_tree = parse(tokens, Grammar_table)
    parse_tree = parse_without_errors(tokens, Grammar_table)
    """ print(parse_tree) """
    if(flag):
        process_syntax_tree(parse_tree, "syntax_tree_output")

    symbol_table = variable_parse(tokens2, Grammar_table)
    variable_print(symbol_table)
    """ print(symbol_table) """

    """ ---------------------------SEMANTICO------------------------------------ """
    print("\n SEMANTICO\n")
    """ TODO:parse_tree? """
    semantic_analysis(symbol_table, parse_tree)

