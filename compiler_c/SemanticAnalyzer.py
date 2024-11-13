# Global symbol table and error log
symbol_table = {}
errors = []

def declare_variable(name, var_type, value=None):
    """Declare a variable with a given type."""
    if name in symbol_table:
        errors.append(f"Warning: Variable '{name}' redeclared.")
    symbol_table[name] = {"tipo": var_type, "initialized": value is not None}
    if value is not None:
        symbol_table[name]["value"] = value
        print(f"Declared '{name}' as '{var_type}' with initial value {value}")

def get_type_of_value(value):
    """Determine the type of a given value."""
    if isinstance(value, int):
        return "int"
    elif isinstance(value, float):
        return "float"
    elif isinstance(value, str):
        if value.startswith('"') and value.endswith('"'):
            return "string"
        elif value.startswith("'") and value.endswith("'"):
            return "char"
    return None  # Unknown type

def assign_variable(name, expression):
    """Assign a value to a variable, checking for declaration, initialization, and type consistency."""
    if name not in symbol_table:
        errors.append(f"Error: Variable '{name}' used before declaration.")
        return
    
    # Assuming 'expression' is a single value for simplicity; expand if handling complex expressions
    expression_type = get_type_of_value(expression)
    variable_type = symbol_table[name]["tipo"]

    if expression_type and expression_type != variable_type:
        errors.append(f"TypeError: Cannot assign value of type '{expression_type}' to variable '{name}' of type '{variable_type}'.")
    else:
        symbol_table[name]["initialized"] = True
        print(f"Assigned '{name}' to '{expression}'")

def check_return(value):
    """Check if the return value has been initialized before returning."""
    if value in symbol_table and not symbol_table[value]["initialized"]:
        print(f"Warning: Variable '{value}' may be uninitialized when returned.")

def print_symbol_table():
    """Print the symbol table for debugging purposes."""
    print("Symbol Table:")
    for name, info in symbol_table.items():
        print(f"{name}: {info}")

def reset_symbol_table():
    """Reset the symbol table to start fresh."""
    global symbol_table, errors
    symbol_table.clear()
    errors.clear()

def analyze_structure(parsed_structure):
    """Analyze the parsed structure for semantic correctness."""
    for statement in parsed_structure:
        if statement["type"] == "declaration":
            declare_variable(statement["name"], statement["var_type"], statement.get("value"))
        elif statement["type"] == "assignment":
            assign_variable(statement["name"], statement["value"])
        elif statement["type"] == "return":
            check_return(statement["value"])

    # Report all errors after analysis
    if errors:
        print("Semantic Analysis Errors:")
        for error in errors:
            print(error)
    else:
        print("No semantic errors detected.")
