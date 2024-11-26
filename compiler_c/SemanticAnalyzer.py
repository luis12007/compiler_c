import re

# Shared data
errors = []
stack = []
processed_define_statements = set()  # To track processed define statements

# ---------------- Clean Data ----------------
def clean_data(symbol_table):
    """
    Cleans the symbol table by normalizing data types:
    - Removes quotes around char values.
    - Converts float literals like '3.3f' to '3.3'.
    """
    for entry in symbol_table:
        value = entry.value
        if isinstance(value, str):
            # Clean char values: 'b' -> b
            if len(value) == 3 and value.startswith("'") and value.endswith("'"):
                entry.value = value[1:-1]

            # Clean float literals: 3.3f -> 3.3
            elif value.endswith('f') and value[:-1].replace('.', '', 1).isdigit():
                entry.value = float(value[:-1])


# ---------------- Substitute Variables ----------------
def substitute_variables(expression, symbol_table, parameters=None):
    """
    Replaces variables in an arithmetic expression with their values from the symbol table.
    For Define Statements, also validates parameter names.
    """
    if parameters is None:
        parameters = []
    for entry in symbol_table:
        if entry.name in expression:
            value = entry.value
            if value is None:
                raise ValueError(f"Variable '{entry.name}' is used in an expression but is not initialized.")
            expression = expression.replace(entry.name, str(value))
    for param in parameters:
        expression = expression.replace(param, "0")  # Replace parameters with dummy values
    return expression


# ---------------- Evaluate Expressions ----------------
def evaluate_expression(expression):
    """
    Evaluates arithmetic expressions like '2/2*x^2' safely.
    Returns the evaluated result or raises a ValueError for invalid expressions.
    """
    try:
        # Replace `^` with `**` for Python exponentiation
        expression = expression.replace('^', '**')

        # Evaluate the expression safely
        result = eval(expression, {"__builtins__": None}, {})

        # Special handling for floats ending with .0
        if isinstance(result, float) and result.is_integer():
            return int(result)  # Convert to int only if it's an exact integer (e.g., 16.0 -> 16)
        return result
    except Exception:
        raise ValueError(f"Invalid arithmetic expression: {expression}")


# ---------------- Validate Define Statements ----------------
def validate_define_statements(symbol_table):
    """
    Validates the Define Statements in the symbol table.
    """
    global errors, processed_define_statements

    for entry in symbol_table:
        if entry.scope == "Define Statement":
            value = entry.value
            processed_define_statements.add(entry.name)  # Mark as processed

            # Handle 'for' statement in Define Statement
            if value.startswith("for("):
                try:
                    validate_for_statement(value)
                except ValueError as e:
                    errors.append(f"Type error: {e} in Define Statement '{entry.name}' at line {entry.line}.")
                    continue  # Skip further processing for this entry

            # Handle parameterized expressions like '(x*10)'
            elif "(" in value and ")" in value:
                try:
                    validate_parameterized_expression(value, entry.parameters)
                except ValueError as e:
                    errors.append(f"Type error: {e} in Define Statement '{entry.name}' at line {entry.line}.")
                    continue  # Skip further processing for this entry


def validate_for_statement(statement):
    """
    Validates a for loop statement like 'for(int x = 0; x<n; ++x)'.
    """
    # Extract the components of the for loop
    match = re.match(r"for\((.*?);(.*?);(.*?)\)", statement)
    if not match:
        raise ValueError(f"Invalid arithmetic expression: {statement}")

    initialization, condition, increment = match.groups()

    # Validate initialization (e.g., 'int x = 0')
    if not re.match(r"(int|float|char) \w+ = .*", initialization.strip()):
        raise ValueError(f"Invalid initialization in for statement: {initialization}")

    # Validate condition (e.g., 'x < n')
    if not re.match(r".*<.*|.*>.*|.*==.*", condition.strip()):
        raise ValueError(f"Invalid condition in for statement: {condition}")

    # Validate increment (e.g., '++x')
    if not re.match(r"\+\+.*|.*\+\+|--.*|.*--", increment.strip()):
        raise ValueError(f"Invalid increment in for statement: {increment}")


def validate_parameterized_expression(expression, parameters):
    """
    Validates parameterized expressions like '(x*10)'.
    Allows string and numeric parameter combinations.
    """
    expression = expression.strip("()")  # Remove parentheses
    tokens = re.split(r"([+\-*/^<>=])", expression)  # Split by operators

    for token in tokens:
        token = token.strip()
        if token:
            # Check if the token is a valid variable, parameter, number, or operator
            if not re.match(r"^\w+$|^\d+(\.\d+)?$|^[+\-*/^<>=]$", token) and token not in parameters:
                raise ValueError(f"Invalid token '{token}' in expression.")


# ---------------- Validate Symbol Table ----------------
# ---------------- Validate Symbol Table ----------------
def validate_symbol_table(symbol_table):
    """
    Validates the symbol table for semantic errors.
    """
    global errors, processed_define_statements
    variable_names = set()  # Track variable names to detect duplicates

    for entry in symbol_table:
        # Skip entries already validated in Define Statement
        if entry.name in processed_define_statements:
            continue

        # Check for duplicate variable names
        if entry.name in variable_names:
            errors.append(
                f"Semantic error: Duplicate variable name '{entry.name}' found at line {entry.line}."
            )
        else:
            variable_names.add(entry.name)

        # Check for uninitialized variables
        if entry.value is None or entry.value == "" or entry.value == 'None':
            if entry.scope in ["Function Initialization", "Function"]:
                continue  # Allowed to be None for these scopes
            else:
                errors.append(f"Variable '{entry.name}' declared but not initialized at line {entry.line}.")

        # Check type consistency
        if entry.value is not None and entry.value != "":
            if isinstance(entry.value, str) and re.search(r"[+\-*/^]", entry.value):
                try:
                    substituted_expression = substitute_variables(entry.value, symbol_table)
                    evaluated_value = evaluate_expression(substituted_expression)

                    # Type checks after evaluation
                    if entry.var_type == "int":
                        if isinstance(evaluated_value, float) and not evaluated_value.is_integer():
                            errors.append(
                                f"Type error: Expression '{entry.value}' evaluates to '{evaluated_value}', which cannot be assigned to int variable '{entry.name}' at line {entry.line}."
                            )
                        elif not isinstance(evaluated_value, int):
                            errors.append(
                                f"Type error: Expression '{entry.value}' evaluates to '{evaluated_value}', which cannot be assigned to int variable '{entry.name}' at line {entry.line}."
                            )
                    elif entry.var_type == "float":
                        if not isinstance(evaluated_value, (int, float)):
                            errors.append(
                                f"Type error: Expression '{entry.value}' evaluates to '{evaluated_value}', which cannot be assigned to float variable '{entry.name}' at line {entry.line}."
                            )
                except ValueError as e:
                    errors.append(f"Type error: {e}")
            elif entry.var_type == "int":
                # Direct value checks for int
                if isinstance(entry.value, float) and not entry.value.is_integer():
                    errors.append(
                        f"Type error: Value '{entry.value}' cannot be assigned to int variable '{entry.name}' at line {entry.line}."
                    )
                elif not isinstance(entry.value, int) and not entry.value.isdigit():
                    errors.append(
                        f"Type error: Value '{entry.value}' is not a valid integer for variable '{entry.name}' at line {entry.line}."
                    )
            elif entry.var_type == "float":
                # Direct value checks for float
                if not isinstance(entry.value, (int, float)) and not re.match(r"^\d+(\.\d+)?$", str(entry.value)):
                    errors.append(
                        f"Type error: Value '{entry.value}' cannot be assigned to float variable '{entry.name}' at line {entry.line}."
                    )

# ---------------- Analyze ----------------
def semantic_analysis(symbol_table, parse_tree):
    """
    Main function for semantic analysis.
    Cleans the data, validates Define Statements, validates the symbol table, and checks the parse tree.
    """
    global errors, stack

    print("Starting semantic analysis...")
    print("----------------------------")

    # Clean data
    clean_data(symbol_table)

    # Validate Define Statements
    validate_define_statements(symbol_table)

    # Validate Symbol Table
    validate_symbol_table(symbol_table)

    print("\nSemantic Analysis Results")
    print("==============================")
    print("Errors:")
    if errors:
        for i, error in enumerate(errors, 1):
            print(f"{i}. {error}")
    else:
        print("No errors found.")

    print("\nFinal Verdict:")
    if errors:
        print("NO - Code not semantically correct.")
    else:
        print("YES - Code semantically correct.")
