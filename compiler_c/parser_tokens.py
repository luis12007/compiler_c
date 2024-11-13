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
    tokens.append(Token('$', '$', -1))  # End-of-input marker
    index = 0  # Track the position in the token list

    print("\nStarting Parsing Process")
    print(f"Initial Stack: {stack}")
    print(f"Tokens: {tokens}\n")

    while stack:
        top = stack.pop()
        current_token = tokens[index]
        
        # Log the current parsing state
        print(f"\nCurrent Stack: {stack}")
        print(f"Top of Stack: {top}")
        print(f"Current Token: {current_token.valor} (Type: {current_token.tipo}) at Line: {current_token.linea}")

        if top in parse_table:  # Non-terminal case
            token_key = current_token.valor if current_token.valor in parse_table[top] else current_token.tipo

            # Log grammar lookup
            print(f"Looking up parse table entry for non-terminal '{top}' with token '{token_key}'")

            if token_key in parse_table[top]:
                rule = parse_table[top][token_key]
                print(f"Expanding '{top}' -> {rule}")
                
                if rule != ['ε']:
                    stack.extend(reversed(rule))
                else:
                    print(f"Rule is ε (epsilon), no change to stack")
            else:
                # Error if no matching rule in the parse table
                error_message = (
                    f"Error: No rule for '{top}' with current token '{current_token.valor}' "
                    f"(Type: '{current_token.tipo}') at line {current_token.linea}."
                )
                print(error_message)
                raise SyntaxError(error_message)

        elif top == current_token.valor:  # Terminal match based on value
            print(f"Terminal match found: {top} == {current_token.valor}")
            index += 1  # Move to the next token

        elif top == current_token.tipo:  # Alternative match based on type if value fails
            print(f"Alternative type match: {top} == {current_token.tipo}")
            index += 1  # Move to the next token

        else:
            # Error if terminal or type doesn't match
            error_message = (
                f"Error: Expected '{top}', but got '{current_token.valor}' "
                f"(Type: '{current_token.tipo}') at line {current_token.linea}"
            )
            print(error_message)
            raise SyntaxError(error_message)

    # Success if stack is empty and all tokens are parsed
    if index == len(tokens) - 1 and not stack:
        print("\nParsing completed successfully: Syntax is correct.")
        return "Parsing completed successfully"
    else:
        error_message = "Parsing ended with issues: Stack or token list not fully processed."
        print(error_message)
        raise SyntaxError(error_message)
