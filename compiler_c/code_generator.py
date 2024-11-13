# Intermediate code instructions storage
intermediate_code = []
temp_count = 0  # Counter for temporary variables

def generate_temp():
    """Generate a unique temporary variable name for TAC operations."""
    global temp_count
    temp_var = f"t{temp_count}"
    temp_count += 1
    return temp_var

def add_instruction(instruction):
    """Add an instruction to the TAC list."""
    intermediate_code.append(instruction)

def generate_code(parsed_structure):
    """Generate three-address code for the parsed structure."""
    for statement in parsed_structure:
        if statement["type"] == "declaration":
            handle_declaration(statement["name"], statement["var_type"], statement.get("value"))
        elif statement["type"] == "assignment":
            handle_assignment(statement["name"], statement["value"])
        elif statement["type"] == "return":
            handle_return(statement["value"])

def handle_declaration(name, var_type, value=None):
    """Generate TAC for variable declaration with optional initialization."""
    if value is not None:
        add_instruction(f"{name} = {value}")
    else:
        add_instruction(f"{name} = 0  # default initialization")

def handle_assignment(name, expression):
    """Generate TAC for variable assignment, handling expressions."""
    # Assuming expression is a simple "x op y" or "value"
    if isinstance(expression, str) and " " in expression:
        left, operator, right = expression.split()
        temp_var = generate_temp()
        add_instruction(f"{temp_var} = {left} {operator} {right}")
        add_instruction(f"{name} = {temp_var}")
    else:
        # Direct assignment, e.g., `name = value`
        add_instruction(f"{name} = {expression}")

def handle_return(value):
    """Generate TAC for return statement."""
    add_instruction(f"RETURN {value}")

def print_intermediate_code():
    """Print the generated TAC."""
    print("Three-Address Code (TAC):")
    for instruction in intermediate_code:
        print(instruction)

def reset_intermediate_code():
    """Reset TAC and temporary counter for fresh code generation."""
    global intermediate_code, temp_count
    intermediate_code.clear()
    temp_count = 0
