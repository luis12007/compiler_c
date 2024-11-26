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

    # Get function names and types from the parse tree
    # Validate function returns
    validate_function_returns(get_function_names_and_types(parse_tree), symbol_table)

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


def get_function_names_and_types(parse_tree):
    """
    Extracts and prints function names and their types from the parse tree.
    """
    function_details = []  # To store the function names and types

    # Iterate through the parse tree to find FUNCDEC nodes
    for i, node in enumerate(parse_tree):

        if node[0] == 'FUNCDEC':  # Look for FUNCDEC node
            func_type = None
            func_name = None
            return_type = None
            print("---------------------------------")

            # Check the next nodes for FUNCTYPE and FUNCTION int, string, float, char, void
            if i + 1 < len(parse_tree) and parse_tree[i + 1][0] == 'FUNCTYPE':
                func_type = parse_tree[i + 1][1][0]  # Extract type (e.g., 'int', 'void')
            if i + 4 < len(parse_tree) and parse_tree[i + 3][0] == 'FUNCTION':
                if parse_tree[i + 4][0] == 'VARNAME':
                    func_name = parse_tree[i + 4][1]

            if i + 3 < len(parse_tree) and parse_tree[i + 3][0] == 'VOID_FUNCTION':
                func_type = "void"
                func_name = "main"

            # Store function details if both name and type are found
            
        if node[0] == 'OPTIONAL_VARVAL':
            


            """ print("OPTIONAL_VARVAL")
            print("plus 1" + str(parse_tree[i + 1]))
            print("plus 2" + str(parse_tree[i + 2]))
            print("plus 3" + str(parse_tree[i + 3]))
            print("plus 4" + str(parse_tree[i + 4]))
            print("plus 5" + str(parse_tree[i + 5]))
            print("plus 6" + str(parse_tree[i + 6]))
            print("plus 7" + str(parse_tree[i + 7]))
            print("plus 8" + str(parse_tree[i + 8]))
            print("plus 9" + str(parse_tree[i + 9]))
            print("plus 10" + str(parse_tree[i + 10]))
            print("plus 11" + str(parse_tree[i + 11]))
            print("plus 12" + str(parse_tree[i + 12]))
            print("plus 13" + str(parse_tree[i + 13]))
            print("plus 14" + str(parse_tree[i + 14]))
            print("plus 15" + str(parse_tree[i + 15])) """

            # String and charts
            if i + 1 < len(parse_tree) and parse_tree[i + 1][1] != 'ARITH_EXPR':
                return_type = parse_tree[i][1]
                if parse_tree[i][1] == ['VARNAME', 'EXPRESSION_TAIL']:
                    return_type = parse_tree[i + 1][1]
            
            # string and floats
            if i + 4 < len(parse_tree) and parse_tree[i + 1][0] == 'ARITH_EXPR':
                print("view" + str(parse_tree[i + 5][1]))
            
                if i + 5 < len(parse_tree) and parse_tree[i + 5][1] == ['ɛ']:
                    return_type = parse_tree[i + 4][1]
                elif i + 8 < len(parse_tree) and parse_tree[i + 5][1] != ['ɛ']:
                    return_type = float(str(parse_tree[i + 4][1]) + str(parse_tree[i + 6][1]) + str(parse_tree[i + 8][1]))

            print(func_name)
            print(func_type)
            print(return_type)

            if func_name and func_type and return_type:
                function_details.append((func_name, func_type, return_type ))

    # Print all function names and types
    """ print(function_details)
    print("Function Names and Types:")
    for func_name, func_type, return_type in function_details:
        print(f"Function Name: {func_name}, Type: {func_type} return type: {return_type}") """

    return function_details

def validate_function_returns(function_details, symbol_table):
    """
    Validates that each function's return type matches its declared type.
    Ensures literals are correctly identified, variables are declared, and match the expected type.
    """
    global errors

    for func_name, func_type, return_type in function_details:
        # Check for "main" function which can have 'None' or 'ɛ' as return
        if func_name == "main":
            if return_type not in [None, ['ɛ']]:
                errors.append(f"Error in function 'main': Return value must be 'None' or ['ɛ'], but found {return_type}.")
            continue

        # Case 1: Literal return (e.g., string, char, int, float)
        if isinstance(return_type, str) and (return_type.startswith('"') and return_type.endswith('"') or return_type.startswith("'") and return_type.endswith("'")):
            # Ensure it matches the correct type
            if func_type == "string" and return_type.startswith('"') and return_type.endswith('"'):
                continue  # Valid string
            elif func_type == "char" and return_type.startswith("'") and return_type.endswith("'") and len(return_type) == 3:
                continue  # Valid char
            else:
                errors.append(f"Type error in function '{func_name}': Literal return value '{return_type}' does not match function type {func_type}.")
        
        # Case 2: Numeric literals
        elif isinstance(return_type, int) or (isinstance(return_type, str) and return_type.isdigit()):
            if func_type != "int":
                errors.append(f"Type error in function '{func_name}': Return value '{return_type}' is an integer but expected {func_type}.")
        
        elif isinstance(return_type, float):
            if func_type != "float":
                errors.append(f"Type error in function '{func_name}': Return value '{return_type}' is a float but expected {func_type}.")

        # Case 3: Variable return
        elif isinstance(return_type, str):  # Variable name case
            # Ensure the variable is declared
            variable_entry = next((entry for entry in symbol_table if entry.name == return_type), None)
            if not variable_entry:
                errors.append(f"Error in function '{func_name}': Return variable '{return_type}' is not declared.")
            else:
                # Validate type consistency
                if variable_entry.var_type != func_type:
                    errors.append(f"Type error in function '{func_name}': Return variable '{return_type}' is of type {variable_entry.var_type}, but expected {func_type}.")
        
        else:
            errors.append(f"Type error in function '{func_name}': Invalid return type '{return_type}'.")
