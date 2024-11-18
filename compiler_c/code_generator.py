def generate_TAC_from_semantic(semantic_data):
    """
    Generates Three-Address Code (TAC) from the response of the semantic analyzer.
    Args:
        semantic_data (list of dict): The processed variables and functions from the semantic analyzer.
    Returns:
        tac (list): List of TAC instructions.
    """
    tac = []
    temp_count = 0  # Counter for temporary variables
    label_count = 0  # Counter for labels

    def new_temp():
        nonlocal temp_count
        temp = f"t{temp_count}"
        temp_count += 1
        return temp

    def new_label():
        nonlocal label_count
        label = f"L{label_count}"
        label_count += 1
        return label

    for entry in semantic_data:
        name = entry["Name"]
        var_type = entry["Type"]
        scope = entry["Scope"]
        value = entry["Value"]
        parameters = entry.get("Parameters")

        # Handle function declarations
        if scope == "Global" and var_type in ["int", "void", "float", "char"] and value == "null":
            tac.append(f"func {name}()")

        # Handle variable declarations with initialization
        elif scope.startswith("Function scope") or scope.startswith("main scope"):
            if value not in ["null", None]:
                tac.append(f"{name} = {value}")

        # Handle arithmetic operations inside loops or functions
        elif scope == "For Loop" and name != "return":
            if value:
                tac.append(f"{name} = {value}")

        # Handle conditionals
        elif scope == "If Statement":
            if name != "return":
                condition = new_temp()
                tac.append(f"{condition} = {value}")
                label = new_label()
                tac.append(f"if {condition} goto {label}")
                tac.append(f"label {label}")

        # Handle return statements
        elif name == "return":
            tac.append(f"return {value}")

        # Handle macros and defines
        elif scope == "DEFINE":
            if parameters:
                tac.append(f"#define {name}({parameters}) {value}")
            else:
                tac.append(f"#define {name} {value}")

    return tac
