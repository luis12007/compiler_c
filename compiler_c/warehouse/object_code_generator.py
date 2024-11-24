def object_parser(tac):
    """
    Converts TAC (Three-Address Code) into object code or assembly-like instructions.
    Args:
        tac (list): List of TAC instructions.
    Returns:
        object_code (list): List of object code or assembly instructions.
    """
    object_code = []
    label_count = 0  # Keep track of labels for jumps

    def get_next_label():
        nonlocal label_count
        label = f"label_{label_count}"
        label_count += 1
        return label

    for instruction in tac:
        if instruction.startswith("#define"):
            # Skip macros and defines; no direct object code mapping
            continue

        elif instruction.startswith("func"):
            # Translate function definitions
            function_name = instruction.split()[1].replace("()", "")
            object_code.append(f"{function_name}_entry:")
            object_code.append("PUSH BP")  # Save base pointer
            object_code.append("MOV BP, SP")  # Set new base pointer
            continue

        elif instruction.startswith("return"):
            # Handle return statements
            return_value = instruction.split('=')[1].strip()
            object_code.append(f"MOV AX, {return_value}")  # Move return value to accumulator
            object_code.append("POP BP")  # Restore base pointer
            object_code.append("RET")  # Return from function
            continue

        elif instruction.startswith("if"):
            # Handle conditional jumps
            condition = instruction.split()[1]
            label = get_next_label()
            object_code.append(f"CMP {condition}, 0")
            object_code.append(f"JE {label}")
            continue

        elif instruction.startswith("label"):
            # Handle labels
            label_name = instruction.split()[1]
            object_code.append(f"{label_name}:")
            continue

        else:
            # Handle general assignments
            if "=" in instruction:
                dest, expr = instruction.split("=")
                dest = dest.strip()
                expr = expr.strip()

                if "+" in expr or "-" in expr or "*" in expr or "/" in expr:
                    # Handle arithmetic operations
                    operands = expr.split()
                    op1 = operands[0]
                    operator = operands[1]
                    op2 = operands[2]

                    object_code.append(f"MOV AX, {op1}")
                    if operator == "+":
                        object_code.append(f"ADD AX, {op2}")
                    elif operator == "-":
                        object_code.append(f"SUB AX, {op2}")
                    elif operator == "*":
                        object_code.append(f"MUL {op2}")
                    elif operator == "/":
                        object_code.append(f"DIV {op2}")
                    object_code.append(f"MOV {dest}, AX")
                else:
                    # Simple assignment
                    object_code.append(f"MOV {dest}, {expr}")
    print(object_code)
    return object_code


def object_code_to_binary(object_code):
    """
    Converts object code to binary instructions based on a predefined ISA.
    Args:
        object_code (list): List of assembly-like instructions.
    Returns:
        binary_code (list): List of binary instructions.
    """

    # Define an example ISA with opcodes
    isa = {
        "MOV": "0001",  
        "ADD": "0010",  
        "SUB": "0011",  
        "MUL": "0100",  
        "DIV": "0101",  
        "CMP": "0110",  
        "JE": "0111",   
        "PUSH": "1000", 
        "POP": "1001",  
        "RET": "1010",  
        "label": "1011"
    }

    # Example register mapping
    registers = {
        "AX": "000",
        "BP": "001",
        "SP": "010",
        "t0": "011", 
        "t1": "100"  
    }

    binary_code = []

    for line in object_code:
        parts = line.split()

        # Process instructions
        if parts[0] in isa:
            opcode = isa[parts[0]]

            if parts[0] == "MOV":
                dest = registers.get(parts[1].strip(","), "111")  # Destination register
                src = registers.get(parts[2], "000")  # Source register or immediate value
                binary_code.append(f"{opcode} {dest} {src}")

            elif parts[0] in {"ADD", "SUB", "MUL", "DIV"}:
                dest = registers.get(parts[1].strip(","), "111")
                src = registers.get(parts[2], "000")
                binary_code.append(f"{opcode} {dest} {src}")

            elif parts[0] == "CMP":
                src = registers.get(parts[1].strip(","), "000")
                binary_code.append(f"{opcode} {src}")

            elif parts[0] == "JE":
                label = parts[1]
                binary_code.append(f"{opcode} {label}")

            elif parts[0] == "PUSH":
                reg = registers.get(parts[1], "111")
                binary_code.append(f"{opcode} {reg}")

            elif parts[0] == "POP":
                reg = registers.get(parts[1], "111")
                binary_code.append(f"{opcode} {reg}")

            elif parts[0] == "RET":
                binary_code.append(opcode)

        # Process labels
        elif line.endswith(":"):
            label_name = line.replace(":", "")
            binary_code.append(f"{isa['label']} {label_name}")

    return binary_code
