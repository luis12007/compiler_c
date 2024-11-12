class Token:
    def __init__(self, tipo, valor, linea):
        self.tipo = tipo  # Token type, e.g., "Tipo de dato int"
        self.valor = valor  # Actual token value, e.g., "int"
        self.linea = linea  # Line number in the source code

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor}, Linea: {self.linea})"

def parse(tokens, parse_table):
    stack = ['$']
    stack.append('SOURCE')  # Start with the grammar's starting symbol

    tokens.append(Token('$', '$', -1))  # Add end-of-input marker
    index = 0  # Track the position in the token list

    print("\nStarting Parsing Process:")
    print(f"Initial Stack: {stack}\n")

    while stack:
        top = stack.pop()
        current_token = tokens[index]

        # Display current parsing state
        print(f"\nCurrent Stack: {stack}")
        print(f"Top of Stack: {top}")
        print(f"Current Token: {current_token.valor} (Type: {current_token.tipo}) at Line: {current_token.linea}")

        # Check if the top of the stack is a terminal that matches the current token's value
        if top == current_token.valor:
            print(f"Terminal match found: {top} == {current_token.valor}")
            index += 1  # Move to the next token
            continue

        # Check if top of stack is a non-terminal
        elif top in parse_table:
            print(f"Expanding non-terminal: {top}")

            # Attempt to find the correct rule in the parse table based on the token value
            token_key = current_token.valor if current_token.valor in parse_table[top] else current_token.tipo

            if token_key in parse_table[top]:
                rule = parse_table[top][token_key]
                print(f"  Rule found: {top} -> {rule}")

                # Push the selected rule onto the stack in reverse order, ignoring epsilon
                if rule != ['ε']:
                    print(f"  Expanding rule: Pushing {list(reversed(rule))} onto stack")
                    stack.extend(reversed(rule))
                else:
                    print(f"  Epsilon rule encountered: {top} -> ε (No action on stack)")
            else:
                # Handle unexpected token error with more context
                print(f"  Error: No rule for '{top}' with current token '{current_token.valor}' (Type: {current_token.tipo})")
                raise SyntaxError(
                    f"Unexpected token '{current_token.valor}' at line {current_token.linea}"
                )

        # Handle cases where the stack's top element is a terminal but does not match the current token
        else:
            print(f"Error: Expected '{top}', but got '{current_token.valor}' (Type: {current_token.tipo})")
            raise SyntaxError(
                f"Unexpected token '{current_token.valor}' (type '{current_token.tipo}') at line {current_token.linea}"
            )

    # Final check to confirm successful parsing
    if index == len(tokens) - 1 and not stack:
        print("\nParsing completed successfully: Syntax correct.")
        return "yes"
    else:
        print("\nParsing ended with issues: Stack or token list not empty.")
        return "no"
