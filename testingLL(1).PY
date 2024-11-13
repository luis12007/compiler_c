from collections import defaultdict

class LL1GrammarChecker:
    def __init__(self, grammar):
        self.grammar = grammar
        self.first = defaultdict(set)
        self.follow = defaultdict(set)
        self.calculate_first_sets()
        self.calculate_follow_sets()
    
    def calculate_first_sets(self):
        for non_terminal in self.grammar:
            self.first[non_terminal] = self.calculate_first(non_terminal)

    def calculate_first(self, symbol):
        if symbol not in self.grammar:
            return {symbol}

        first_set = set()
        for production in self.grammar[symbol]:
            for sym in production:
                symbol_first = self.calculate_first(sym)
                first_set.update(symbol_first - {"ɛ"})
                if "ɛ" not in symbol_first:
                    break
            else:
                first_set.add("ɛ")
        return first_set
    
    def calculate_follow_sets(self):
        start_symbol = next(iter(self.grammar))
        self.follow[start_symbol].add('$')

        changed = True
        while changed:
            changed = False
            for non_terminal in self.grammar:
                for production in self.grammar[non_terminal]:
                    for i, B in enumerate(production):
                        if B in self.grammar:
                            follow_before = self.follow[B].copy()
                            for symbol in production[i + 1:]:
                                self.follow[B].update(self.first[symbol] - {"ɛ"})
                                if "ɛ" not in self.first[symbol]:
                                    break
                            else:
                                self.follow[B].update(self.follow[non_terminal])
                            if follow_before != self.follow[B]:
                                changed = True

    def is_ll1(self):
        for non_terminal in self.grammar:
            first_sets = []
            for production in self.grammar[non_terminal]:
                first_set = set()
                for symbol in production:
                    first_set.update(self.first[symbol] - {"ɛ"})
                    if "ɛ" not in self.first[symbol]:
                        break
                else:
                    first_set.add("ɛ")
                first_sets.append(first_set)
            
            for i in range(len(first_sets)):
                for j in range(i + 1, len(first_sets)):
                    if first_sets[i] & first_sets[j]:
                        print(f"Conflict in First sets for {non_terminal}: {first_sets[i]} & {first_sets[j]}")
                        return False

            if any("ɛ" in fs for fs in first_sets):
                if any(self.follow[non_terminal] & (fs - {"ɛ"}) for fs in first_sets if "ɛ" in fs):
                    print(f"Conflict between First and Follow sets for {non_terminal} due to ε-production.")
                    return False
        return True

# Define the full grammar 
grammar = {
    "SOURCE": [["INCLUDEBLOCK", "DEFINEBLOCK", "FUNCTIONBLOCK", "MAINFUNCTION"]],

    "INCLUDEBLOCK": [["INCLUDESTATEMENT", "INCLUDEBLOCK"], ["ɛ"]],
    "DEFINEBLOCK": [["DEFINESTATEMENT", "DEFINEBLOCK"], ["ɛ"]],
    "FUNCTIONBLOCK": [["FUNCDEC", "FUNCTIONBLOCK"], ["ɛ"]],

    "STATEMENT": [
        ["INITLINE", "STATEMENT"],
        ["SWITCHSTATEMENT", "STATEMENT"],
        ["CONDITIONAL", "STATEMENT"],
        ["LOOPSTATEMENT", "STATEMENT"],
        ["VARCHANGELINE", "STATEMENT"],
        ["RETURNSTATEMENT", "STATEMENT"],
        ["ɛ"]
    ],

    "CONDITIONAL": [["if", "(", "CONDITION", ")", "{", "STATEMENT", "}", "CONDITIONAL_ELSE"]],
    "CONDITIONAL_ELSE": [["else", "{", "STATEMENT", "}"], ["ɛ"]],

    "SWITCHSTATEMENT": [["switch", "(", "VARNAME", ")", "{", "SWITCHCASELIST", "}"]],
    "SWITCHCASELIST": [["SWITCHCASE", "SWITCHCASELIST'", "DEFAULTCASE"]],
    "SWITCHCASELIST'": [["SWITCHCASE", "SWITCHCASELIST'"], ["ɛ"]],
    "DEFAULTCASE": [["default:", "STATEMENT", "break;"]],

    "LOOPSTATEMENT": [["FORLOOP"], ["WHILELOOP"], ["DOWHILELOOP"]],
    "FORLOOP": [["for", "(", "FORVAR", ";", "CONDITION", ";", "VARCHANGESTATEMENT", ")", "{", "STATEMENT", "}"]],
    "FORVAR": [["INITSTATEMENT"], ["VARNAME"]],
    "WHILELOOP": [["while", "(", "CONDITION", ")", "{", "STATEMENT", "}"]],
    "DOWHILELOOP": [["do", "{", "STATEMENT", "}", "while", "(", "CONDITION", ")"]],

    "VARNAME": [["[a-zA-Z_][a-zA-Z0-9_]*"]],
    "KEYWORD": [["static"], ["const"], ["volatile"], ["inline"], ["ɛ"]],

    "INCLUDESTATEMENT": [["#include", "<", "VARNAME", ".", "VARNAME", ">"], ["#include", "\"", "VARNAME", ".", "VARNAME", "\""]],
    "DEFINESTATEMENT": [["#define", "VARNAME", "VARNAME"], ["#define", "VARNAME", "{", "STATEMENT", "}"], ["#define", "FUNCTION"]],

    "RETURNSTATEMENT": [["return", "VARVAL", ";"], ["return;"]],
    "INITLINE": [["KEYWORD", "INITSTATEMENT"]],

    "INITLIST": [["INITSTATEMENT", "INITLIST'"]],
    "INITLIST'": [["INITSTATEMENT", "INITLIST'"], ["ɛ"]],

    # Updated initialization rules for each type to allow assignment
    "INITSTATEMENT": [["INTINIT"], ["FLOATINIT"], ["CHARINIT"], ["STRINGINIT"], ["DOUBLEINIT"], ["LONGINIT"], ["SHORTINIT"]],

    "INTINIT": [["int", "VARNAME", "INTLIST"], ["int", "VARNAME", "=", "INTVAL", "INTLIST"]],
    "FLOATINIT": [["float", "VARNAME", "FLOATLIST"], ["float", "VARNAME", "=", "FLOATVAL", "FLOATLIST"]],
    "CHARINIT": [["char", "VARNAME", "CHARLIST"], ["char", "VARNAME", "=", "CHARVAL", "CHARLIST"]],
    "STRINGINIT": [["string", "VARNAME", "STRINGLIST"], ["string", "VARNAME", "=", "STRINGVAL", "STRINGLIST"]],
    "DOUBLEINIT": [["double", "VARNAME", "DOUBLELIST"], ["double", "VARNAME", "=", "DOUBLEVAL", "DOUBLELIST"]],
    "LONGINIT": [["long", "VARNAME", "LONGLIST"], ["long", "VARNAME", "=", "INTVAL", "LONGLIST"]],
    "SHORTINIT": [["short", "VARNAME", "SHORTLIST"], ["short", "VARNAME", "=", "INTVAL", "SHORTLIST"]],

    # Updated list rules with optional initialization and empty lists
    "INTLIST": [[",", "VARNAME", "INTLIST"], [",", "VARNAME", "=", "INTVAL", "INTLIST"], ["ɛ"]],
    "FLOATLIST": [[",", "VARNAME", "FLOATLIST"], [",", "VARNAME", "=", "FLOATVAL", "FLOATLIST"], ["ɛ"]],
    "CHARLIST": [[",", "VARNAME", "CHARLIST"], [",", "VARNAME", "=", "CHARVAL", "CHARLIST"], ["ɛ"]],
    "STRINGLIST": [[",", "VARNAME", "STRINGLIST"], [",", "VARNAME", "=", "STRINGVAL", "STRINGLIST"], ["ɛ"]],
    "DOUBLELIST": [[",", "VARNAME", "DOUBLELIST"], [",", "VARNAME", "=", "DOUBLEVAL", "DOUBLELIST"], ["ɛ"]],
    "LONGLIST": [[",", "VARNAME", "LONGLIST"], [",", "VARNAME", "=", "INTVAL", "LONGLIST"], ["ɛ"]],
    "SHORTLIST": [[",", "VARNAME", "SHORTLIST"], [",", "VARNAME", "=", "INTVAL", "SHORTLIST"], ["ɛ"]],

    # Arithmetic expressions and value types
    "VARVAL": [["ARITH_EXPR"]],
    "ARITH_EXPR": [["TERM", "ARITH_EXPR'"]],
    "ARITH_EXPR'": [["+", "TERM", "ARITH_EXPR'"], ["-", "TERM", "ARITH_EXPR'"], ["ɛ"]],
    "TERM": [["FACTOR", "TERM'"]],
    "TERM'": [["*", "FACTOR", "TERM'"], ["/", "FACTOR", "TERM'"], ["ɛ"]],
    "FACTOR": [["VARNAME"], ["INTVAL"], ["FLOATVAL"], ["CHARVAL"], ["STRINGVAL"], ["DOUBLEVAL"], ["(", "ARITH_EXPR", ")"]],

    # Literal values
    "INTVAL": [["[0-9][0-9]*"]],
    "FLOATVAL": [["[0-9][0-9]*\\.[0-9]+"], ["[0-9][0-9]*f"]],
    "CHARVAL": [["'[a-zA-Z0-9$&+,:;=?@#|'<>.^*()%!-]*'"]],
    "STRINGVAL": [["\"[a-zA-Z0-9$&+,:;=?@#|'<>.^*()%!-]*\""]],
    "DOUBLEVAL": [["[0-9][0-9]*\\.[0-9]*d"], ["[0-9][0-9]*\\.[0-9]*"]],

    # Main function and function declarations
    "MAINFUNCTION": [
        ["FUNCTYPE", "main", "(", "INITLIST", ")", "{", "STATEMENT", "RETURNSTATEMENT", "}"],
        ["void", "main", "(", "INITLIST", ")", "{", "STATEMENT", "RETURNSTATEMENT", "}"]
    ],
    "FUNCDEC": [["FUNCTYPE", "FUNCTION"]],
    "FUNCTION": [["VARNAME", "(", "INITLIST", ")", "{", "STATEMENT", "RETURNSTATEMENT", "}"]],
    "FUNCTYPE": [["int"], ["float"], ["char"], ["string"], ["double"], ["long"], ["short"], ["void"]],

    # Variable change line
    "VARCHANGELINE": [["VARCHANGESTATEMENT", ";"]],
    "VARCHANGESTATEMENT": [["VARNAME", "VARIABLE_MODIFICATION"]],

    # Operations and modifications
    "VARIABLE_MODIFICATION": [
        ["++"], ["--"], ["=", "ARITH_EXPR"], ["+=", "ARITH_EXPR"],
        ["-=", "ARITH_EXPR"], ["*=", "ARITH_EXPR"], ["/=", "ARITH_EXPR"]
    ],
    "VAROPLIST": [["ɛ"], ["PLUS_OPERATION"], ["MINUS_OPERATION"], ["MULTIPLY_OPERATION"], ["DIVIDE_OPERATION"]],
    "PLUS_OPERATION": [["+", "VARNAME", "VAROPLIST"], ["+", "ARITH_EXPR", "VAROPLIST"]],
    "MINUS_OPERATION": [["-", "VARNAME", "VAROPLIST"], ["-", "ARITH_EXPR", "VAROPLIST"]],
    "MULTIPLY_OPERATION": [["*", "VARNAME", "VAROPLIST"], ["*", "ARITH_EXPR", "VAROPLIST"]],
    "DIVIDE_OPERATION": [["/", "VARNAME", "VAROPLIST"], ["/", "ARITH_EXPR", "VAROPLIST"]],
}


# Instantiate the LL(1) checker and test
ll1_checker = LL1GrammarChecker(grammar)
is_ll1 = ll1_checker.is_ll1()

print("The grammar is LL(1):", is_ll1)
