import re

class Token:
    def __init__(self, tipo, valor, linea):
        self.tipo = tipo  # Token type
        self.valor = valor  # Token value
        self.linea = linea  # Line number

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor}, Linea: {self.linea})"

def parse(tokens, parse_table):
    stack = ['$']
    stack.append('SOURCE')  # Start with the grammar's starting symbol

    tokens.append(Token('$', '$', -1))  # End-of-input marker
    index = 0  # Track the position in the token list

    # Precompile regex patterns from the parse table for only the non-terminals that are regex-based
    regex_patterns = {
        non_terminal: {pattern: re.compile(pattern) for pattern in parse_table[non_terminal] if "[" in pattern}
        for non_terminal in parse_table
    }

    print("\nStarting Parsing Process:")
    print(f"Initial Stack: {stack}\n")
    print(f"Tokens: {tokens}\n")

    while stack:
        top = stack.pop()
        current_token = tokens[index]

        print(f"\nCurrent Stack: {stack}")
        print(f"Top of Stack: {top}")
        print(f"Current Token: {current_token.valor} (Type: {current_token.tipo}) at Line: {current_token.linea}")
        
        # Check if `top` is a regex-based non-terminal
        if top in regex_patterns and regex_patterns[top]:  # Only attempt regex if patterns exist for this non-terminal
            matched = False
            for pattern, compiled_regex in regex_patterns[top].items():
                if compiled_regex.fullmatch(current_token.valor):
                    print(f"Regex match found for '{top}' pattern '{pattern}' with token '{current_token.valor}'")
                    matched = True
                    index += 1  # Move to the next token
                    break
            if matched:
                continue
            else:
                if top in parse_table:
                    token_key = current_token.valor if current_token.valor in parse_table[top] else current_token.tipo
                    if token_key in parse_table[top]:
                        rule = parse_table[top][token_key]
                        print(f"Rule found: {top} -> {rule}")
                        if rule != ['ɛ']:
                            print(f"Expanding rule: Pushing {list(reversed(rule))} onto stack")
                            stack.extend(reversed(rule))
                    else:
                        print(f"Error: No rule for '{top}' with current token '{current_token.valor}' (Type: '{current_token.tipo}')")
                        raise SyntaxError(
                            f"Unexpected token '{current_token.valor}' (type '{current_token.tipo}') at line {current_token.linea}"
                        )
                    continue
                elif top == current_token.valor:
                    print(f"Terminal match found: {top} == {current_token.valor}")
                    index += 1  # Move to the next token
                    continue
                else:
                    print(f"Error: No matching regex rule for '{top}' with token '{current_token.valor}'")
                    raise SyntaxError(
                        f"Unexpected token '{current_token.valor}' (type '{current_token.tipo}') at line {current_token.linea}"
                    )

        # Non-regex non-terminal handling
        elif top in parse_table:
            token_key = current_token.valor if current_token.valor in parse_table[top] else current_token.tipo

            if token_key in parse_table[top]:
                rule = parse_table[top][token_key]
                print(f"Rule found: {top} -> {rule}")
                if rule != ['ɛ']:
                    print(f"Expanding rule: Pushing {list(reversed(rule))} onto stack")
                    stack.extend(reversed(rule))
            else:
                print(f"Error: No rule for '{top}' with current token '{current_token.valor}' (Type: '{current_token.tipo}')")
                raise SyntaxError(
                    f"Unexpected token '{current_token.valor}' (type '{current_token.tipo}') at line {current_token.linea}"
                )

        elif top == current_token.valor:
            print(f"Terminal match found: {top} == {current_token.valor}")
            index += 1  # Move to the next token
            continue

        else:
            print(f"Error: Expected '{top}', but got '{current_token.valor}' (Type: {current_token.tipo})")
            raise SyntaxError(
                f"Unexpected token '{current_token.valor}' (type '{current_token.tipo}') at line {current_token.linea}"
            )

    if index == len(tokens) and not stack:
        print("\nParsing completed successfully: Syntax correct.")
        return "yes"
    else:
        print(stack)
        print(index)
        print(len(tokens))
        print("\nParsing ended with issues: Stack or token list not empty.")
        return "no"

"""---------------------------VARIABLES--------------------"""
class Var:
    def __init__(self, name, value, type, source, linea):
        self.name = name
        self.value = value
        self.type = type
        self.source = source
        self.linea = linea

    def __repr__(self):
        return f'Var({self.name}, {self.value}, {self.type}, {self.source}, Linea: {self.linea})'

def variable_parse(tokens, parse_table):
    variable_declaration = False
    variables = []
    stack = ['$']
    stack.append('SOURCE')  # Start with the grammar's starting symbol
    tokens.append(Token('$', '$', -1))  # End-of-input marker
    index = 0  # Track the position in the token list
    # Precompile regex patterns from the parse table for only the non-terminals that are regex-based
    regex_patterns = {
        non_terminal: {pattern: re.compile(pattern) for pattern in parse_table[non_terminal] if "[" in pattern}
        for non_terminal in parse_table
    }
    while stack:
        top = stack.pop()
        current_token = tokens[index]

        # Handle semicolon within `STATEMENT` by skipping it
        if top == "INITLIST'" and current_token.valor == ";" :
            print("Skipping semicolon within STATEMENT context.")
            index += 1
            continue
        
        # Check if `top` is a regex-based non-terminal
        if top in regex_patterns and regex_patterns[top]:  # Only attempt regex if patterns exist for this non-terminal
            matched = False
            for pattern, compiled_regex in regex_patterns[top].items():
                if compiled_regex.fullmatch(current_token.valor):
                    print(f"Regex match found for '{top}' pattern '{pattern}' with token '{current_token.valor}'")
                    matched = True
                    index += 1  # Move to the next token
                    break
            if matched:
                continue
            else:
                if top in parse_table:
                    token_key = current_token.valor if current_token.valor in parse_table[top] else current_token.tipo
                    if token_key in parse_table[top]:
                        rule = parse_table[top][token_key]
                        print(f"Rule found: {top} -> {rule}")
                        if rule != ['ɛ']:
                            print(f"Expanding rule: Pushing {list(reversed(rule))} onto stack")
                            stack.extend(reversed(rule))
                    else:
                        print(f"Error: No rule for '{top}' with current token '{current_token.valor}' (Type: '{current_token.tipo}')")
                        raise SyntaxError(
                            f"Unexpected token '{current_token.valor}' (type '{current_token.tipo}') at line {current_token.linea}"
                        )
                    continue
                elif top == current_token.valor:
                    print(f"Terminal match found: {top} == {current_token.valor}")
                    index += 1  # Move to the next token
                    continue
                else:
                    print(f"Error: No matching regex rule for '{top}' with token '{current_token.valor}'")
                    raise SyntaxError(
                        f"Unexpected token '{current_token.valor}' (type '{current_token.tipo}') at line {current_token.linea}"
                    )

        # Non-regex non-terminal handling
        elif top in parse_table:
            token_key = current_token.valor if current_token.valor in parse_table[top] else current_token.tipo

            if token_key in parse_table[top]:
                rule = parse_table[top][token_key]
                print(f"Rule found: {top} -> {rule}")
                if rule != ['ɛ']:
                    print(f"Expanding rule: Pushing {list(reversed(rule))} onto stack")
                    stack.extend(reversed(rule))
            else:
                print(f"Error: No rule for '{top}' with current token '{current_token.valor}' (Type: '{current_token.tipo}')")
                raise SyntaxError(
                    f"Unexpected token '{current_token.valor}' (type '{current_token.tipo}') at line {current_token.linea}"
                )

        elif top == current_token.valor:
            print(f"Terminal match found: {top} == {current_token.valor}")
            index += 1  # Move to the next token
            continue

        else:
            print(f"Error: Expected '{top}', but got '{current_token.valor}' (Type: {current_token.tipo})")
            raise SyntaxError(
                f"Unexpected token '{current_token.valor}' (type '{current_token.tipo}') at line {current_token.linea}"
            )

    if index == len(tokens) and not stack:
        print("\nParsing completed successfully: Syntax correct.")
        return "yes"
    else:
        print(stack)
        print(index)
        print(len(tokens))
        print("\nParsing ended with issues: Stack or token list not empty.")
        return "no"
    return tokens