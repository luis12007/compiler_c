def semantic_analyzer(vars_list):
    """
    Receives a list of Var objects and performs semantic analysis.
    Validates:
        - Type consistency (including 'return' statements matching scope type)
        - Redefinitions
        - Proper function declarations
        - Initialization checks for variables (but ignores 'null' as a value)
    Logs:
        - Errors
        - Warnings
        - Pass messages
    Returns:
        - Intermediate code representation
        - List of errors and warnings
    """
    intermediate_code = []
    errors = []
    warnings = []
    scope_tracker = {}

    for var in vars_list:
        # Debug: Start analyzing variable
        print(f"Analyzing: {var}")

        # Check for redefinitions within the same scope
        if var.scope not in scope_tracker:
            scope_tracker[var.scope] = set()
        
        if var.name in scope_tracker[var.scope]:
            if var.scope != "DEFINE":  # Allows macros to reuse names
                errors.append(f"Redefinition of variable '{var.name}' in scope '{var.scope}' at line {var.line}.")
        else:
            scope_tracker[var.scope].add(var.name)

        # Check type consistency
        if var.var_type == "float" and var.value not in [None, "null"]:
            try:
                # Allow float literals with or without 'f'
                if var.value.endswith("f"):
                    float(var.value[:-1])  # Try converting after removing 'f'
                else:
                    float(var.value)  # Try converting directly
            except ValueError:
                errors.append(f"Type mismatch: Variable '{var.name}' expected 'float' but got '{var.value}' at line {var.line}.")
        elif var.var_type == "int" and var.value not in [None, "null"]:
            try:
                int(var.value)  # Try converting to int
            except ValueError:
                errors.append(f"Type mismatch: Variable '{var.name}' expected 'int' but got '{var.value}' at line {var.line}.")
        elif var.var_type == "char" and var.value not in [None, "null"]:
            if not (isinstance(var.value, str) and len(var.value) == 3 and var.value.startswith("'") and var.value.endswith("'")):
                errors.append(f"Type mismatch: Variable '{var.name}' expected 'char' but got '{var.value}' at line {var.line}.")
        
        # Check return statements
        if var.name == "return":
            function_scope = var.scope.split(":")[-1].strip()  # Extract function name from scope
            for scope_var in vars_list:
                if scope_var.name == function_scope and scope_var.scope == "Global":
                    if scope_var.var_type != var.var_type:
                        errors.append(f"Type mismatch in 'return' statement at line {var.line}: Expected '{scope_var.var_type}' but got '{var.var_type}'.")
                    break

        # Validate missing initialization (but ignore 'null')
        if var.var_type not in ["void", "MACRO"] and var.value in [None, ""]:
            warnings.append(f"Variable '{var.name}' declared but not initialized in scope '{var.scope}' at line {var.line}.")

        # Validate macros for proper structure
        if var.scope == "DEFINE" and var.parameters and not var.parameters.startswith("("):
            errors.append(f"Improper macro declaration for '{var.name}' at line {var.line}. Parameters should start with '('.")

        # Convert valid vars to intermediate representation
        entry = {
            "Name": var.name,
            "Type": var.var_type,
            "Scope": var.scope,
            "Value": var.value,
            "Parameters": var.parameters if var.parameters else None,
        }
        intermediate_code.append(entry)

    # Debug: Summary messages
    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("\nSemantic analysis passed with no errors.")

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"  - {warning}")
    else:
        print("\nNo warnings during semantic analysis.")

    print("\nFinal Intermediate Code:")
    for entry in intermediate_code:
        print(f"  - {entry}")

    return intermediate_code, errors, warnings
