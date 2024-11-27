from prettytable import PrettyTable
import re

class Token:
    def __init__(self, tipo, valor, linea):
        self.tipo = tipo  # Token type
        self.valor = valor  # Token value
        self.linea = linea  # Line number

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor}, Linea: {self.linea})"


def parse_without_errors(tokens, parse_table):
    stack = ['$']
    stack.append('SOURCE')  # Start with the grammar's starting symbol

    tokens.append(Token('$', '$', -1))  # End-of-input marker
    index = 0  # Track the position in the token list

    # Syntax tree data structure
    syntax_tree = []  # List to store the syntax tree nodes

    # Precompile regex patterns from the parse table for only the non-terminals that are regex-based
    regex_patterns = {
        non_terminal: {pattern: re.compile(pattern) for pattern in parse_table[non_terminal] if "[" in pattern}
        for non_terminal in parse_table
    }


    while stack:
        top = stack.pop()
        current_token = tokens[index]


        result = ""
        transition = f"{top} -> ɛ"  # Default transition for empty rules

        # Check if `top` is a regex-based non-terminal
        if top in regex_patterns and regex_patterns[top]:  # Only attempt regex if patterns exist for this non-terminal
            matched = False
            for pattern, compiled_regex in regex_patterns[top].items():
                if compiled_regex.fullmatch(current_token.valor):
                    if(top == "VARNAME" and current_token.tipo == "VARNAME"):
                        result = f"Regex match: {current_token.valor}"
                        matched = True
                        index += 1  # Move to the next token
                        syntax_tree.append((top, current_token.valor, "Regex Match"))  # Save to syntax tree
                    else:
                        handle_error(f"'{current_token.valor}' is a reserved word in '{top}' rule expansion", stack, index, tokens)
                    break
            if matched:
                continue
            else:
                if top in parse_table:
                    token_key = current_token.valor if current_token.valor in parse_table[top] else current_token.tipo
                    if token_key in parse_table[top]:
                        rule = parse_table[top][token_key]
                        result = f"Rule found: {top} -> {rule}"
                        transition = f"{top} -> {rule}"
                        if rule != ['ɛ']:
                            stack.extend(reversed(rule))
                        syntax_tree.append((top, rule, "Rule Applied"))  # Save rule to syntax tree
                    else:
                        handle_error(f"No rule for '{top}' with current token '{current_token.valor}'", stack, index, tokens)
                        continue
                    continue
                elif top == current_token.valor:
                    result = f"Terminal match: {top} == {current_token.valor}"
                    transition = f"{top} -> terminal"
                    index += 1  # Move to the next token
                    syntax_tree.append((top, current_token.valor, "Terminal Match"))  # Save to syntax tree
                    continue
                else:
                    handle_error(f"No matching regex rule for '{top}' with token '{current_token.valor}'", stack, index, tokens)
                    continue

        # Non-regex non-terminal handling
        elif top in parse_table:
            token_key = current_token.valor if current_token.valor in parse_table[top] else current_token.tipo

            if token_key in parse_table[top]:
                rule = parse_table[top][token_key]
                result = f"Rule found: {top} -> {rule}"
                transition = f"{top} -> {rule}"
                if rule != ['ɛ']:
                    stack.extend(reversed(rule))
                syntax_tree.append((top, rule, "Rule Applied"))  # Save rule to syntax tree
            else:
                handle_error(f"No rule for '{top}' with current token '{current_token.valor}'", stack, index, tokens)
                continue

        elif top == current_token.valor:
            result = f"Terminal match: {top} == {current_token.valor}"
            transition = f"{top} -> terminal"
            index += 1  # Move to the next token
            syntax_tree.append((top, current_token.valor, "Terminal Match"))  # Save to syntax tree
            continue

        else:
            handle_error(f"Expected '{top}', but got '{current_token.valor}'", stack, index, tokens)

    if index == len(tokens) and not stack:
        print(len(tokens), index, stack)
        print("\nParsing completed successfully: Syntax correct.")
        print("Yes")
        return syntax_tree  # Return the syntax tree
    else:
        print(len(tokens), index, stack)
        print("\nParsing ended with issues: Stack or token list not empty.")
        print("No")
        return syntax_tree  # Return the syntax tree even if parsing fails

    

"""-----------------------ERROR HANDLER--------------------"""

# New function: Error handler
def handle_error(message, stack, index, tokens):
    
    print("\nParsing error:")
    print(message)
    print("\nStack:", stack)
    print("Current token index:", index)
    print("Current token:", tokens[index])


    return index