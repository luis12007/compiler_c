# Object code instructions storage
object_code = []
registers = ["R1", "R2", "R3", "R4"]  # Simulated registers
register_usage = {}  # Track variable to register mappings

def reset_object_code():
    """Reset object code and register usage for fresh code generation."""
    global object_code, register_usage
    object_code.clear()
    register_usage.clear()

def get_register(var):
    """Allocate or reuse a register for a variable."""
    # Check if the variable is already in a register
    if var in register_usage:
        return register_usage[var]
    
    # Find an available register
    for reg in registers:
        if reg not in register_usage.values():
            register_usage[var] = reg
            return reg
    
    # Spill: if all registers are full, free one and reuse it (simple strategy)
    spilled_var, reg = register_usage.popitem()
    object_code.append(f"STORE {reg}, {spilled_var}")
    register_usage[var] = reg
    return reg

def add_instruction(instruction):
    """Add an instruction to the object code list."""
    object_code.append(instruction)

def generate_object_code(tac):
    """Generate object code from three-address code (TAC)."""
    for instruction in tac:
        parts = instruction.split()
        
        if len(parts) == 3 and parts[1] == '=':
            # Handle direct assignment (e.g., result = 1)
            var, value = parts[0], parts[2]
            reg = get_register(var)
            add_instruction(f"LOAD {reg}, {value}")
            add_instruction(f"STORE {reg}, {var}")
        
        elif len(parts) == 5 and parts[3] in {'+', '-', '*', '/'}:
            # Handle arithmetic operation (e.g., t0 = result * i)
            dest, left, op, right = parts[0], parts[2], parts[3], parts[4]
            reg_left = get_register(left)
            reg_right = get_register(right)
            reg_dest = get_register(dest)

            # Load left operand if not in register
            add_instruction(f"LOAD {reg_left}, {left}")
            add_instruction(f"LOAD {reg_right}, {right}")
            
            # Perform operation
            if op == '+':
                add_instruction(f"ADD {reg_dest}, {reg_left}, {reg_right}")
            elif op == '-':
                add_instruction(f"SUB {reg_dest}, {reg_left}, {reg_right}")
            elif op == '*':
                add_instruction(f"MUL {reg_dest}, {reg_left}, {reg_right}")
            elif op == '/':
                add_instruction(f"DIV {reg_dest}, {reg_left}, {reg_right}")
            
            # Store result
            add_instruction(f"STORE {reg_dest}, {dest}")

        elif parts[0] == "RETURN":
            # Handle return (e.g., RETURN result)
            reg = get_register(parts[1])
            add_instruction(f"LOAD {reg}, {parts[1]}")
            add_instruction(f"RETURN {reg}")

def print_object_code():
    """Print the generated object code."""
    print("Object Code:")
    for instruction in object_code:
        print(instruction)
