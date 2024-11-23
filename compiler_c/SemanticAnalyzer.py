import re

class SemanticAnalyzerWithStack:
    def __init__(self, symbol_table, parse_tree):
        self.symbol_table = symbol_table
        self.parse_tree = parse_tree
        self.errors = []
        self.stack = []
        self.processed_define_statements = set()  # To track processed define statements

    # ---------------- Clean Data ----------------
    def clean_data(self):
        """
        Cleans the symbol table by normalizing data types:
        - Removes quotes around char values.
        - Converts float literals like '3.3f' to '3.3'.
        """
        for entry in self.symbol_table:
            value = entry.value
            if isinstance(value, str):
                # Clean char values: 'b' -> b
                if len(value) == 3 and value.startswith("'") and value.endswith("'"):
                    entry.value = value[1:-1]

                # Clean float literals: 3.3f -> 3.3
                elif value.endswith('f') and value[:-1].replace('.', '', 1).isdigit():
                    entry.value = float(value[:-1])

    # ---------------- Substitute Variables ----------------
    def substitute_variables(self, expression):
        """
        Replaces variables in an arithmetic expression with their values from the symbol table.
        """
        for entry in self.symbol_table:
            if entry.name in expression:
                value = entry.value
                if value is None:
                    raise ValueError(f"Variable '{entry.name}' is used in an expression but is not initialized.")
                expression = expression.replace(entry.name, str(value))
        return expression

    # ---------------- Evaluate Expressions ----------------
    def evaluate_expression(self, expression):
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
        except Exception as e:
            raise ValueError(f"Invalid arithmetic expression: {expression}")

    # ---------------- Validate Define Statements ----------------
    def validate_define_statements(self):
        """
        Validates the Define Statements in the symbol table.
        For example:
        - Treat 'for(int x = 0; x<n; ++x)' as a for statement and verify it semantically.
        - Allow expressions like '(x*10)' to combine parameters and numbers.
        """
        for entry in self.symbol_table:
            if entry.scope == "Define Statement":
                value = entry.value
                self.processed_define_statements.add(entry.name)  # Mark as processed

                # Handle 'for' statement in Define Statement
                if value.startswith("for("):
                    try:
                        self.validate_for_statement(value)
                    except ValueError as e:
                        self.errors.append(f"Type error: {e} in Define Statement '{entry.name}' at line {entry.line}.")
                        continue  # Skip further processing for this entry

                # Handle parameterized expressions like '(x*10)'
                elif "(" in value and ")" in value:
                    try:
                        self.validate_parameterized_expression(value)
                    except ValueError as e:
                        self.errors.append(f"Type error: {e} in Define Statement '{entry.name}' at line {entry.line}.")
                        continue  # Skip further processing for this entry

    def validate_for_statement(self, statement):
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

    def validate_parameterized_expression(self, expression):
        """
        Validates parameterized expressions like '(x*10)'.
        Allows string and numeric parameter combinations.
        """
        expression = expression.strip("()")  # Remove parentheses
        tokens = re.split(r"([+\-*/^])", expression)  # Split by operators

        for token in tokens:
            token = token.strip()
            if token and not re.match(r"^\w+$|^\d+(\.\d+)?$", token):
                raise ValueError(f"Invalid token '{token}' in expression.")

    # ---------------- Validate Symbol Table ----------------
    def validate_symbol_table(self):
        """
        Validates the symbol table for semantic errors.
        """
        for entry in self.symbol_table:
            # Skip entries already validated in Define Statement
            if entry.name in self.processed_define_statements:
                continue

            # Check for uninitialized variables
            if entry.value is None or entry.value == "" or entry.value == 'None':
                if entry.scope == "Function Initialization":
                    continue  # Allowed to be None or "" for Function Initialization scope
                if entry.scope == "Function":
                    continue  # Allowed to be None for Function scope
                else:
                    self.errors.append(f"Variable '{entry.name}' declared but not initialized at line {entry.line}.")

            # Check type consistency
            if entry.value is not None and entry.value != "":
                if isinstance(entry.value, str) and re.search(r"[+\-*/^]", entry.value):
                    try:
                        substituted_expression = self.substitute_variables(entry.value)
                        evaluated_value = self.evaluate_expression(substituted_expression)

                        # Type checks after evaluation
                        if entry.var_type == "int":
                            if isinstance(evaluated_value, float):
                                if evaluated_value.is_integer():
                                    evaluated_value = int(evaluated_value)
                                else:
                                    self.errors.append(
                                        f"Type error: Expression '{entry.value}' evaluates to '{evaluated_value}', which cannot be assigned to int variable '{entry.name}' at line {entry.line}."
                                    )
                            elif not isinstance(evaluated_value, int):
                                self.errors.append(
                                    f"Type error: Expression '{entry.value}' evaluates to '{evaluated_value}', which cannot be assigned to int variable '{entry.name}' at line {entry.line}."
                                )
                        elif entry.var_type == "float":
                            if not isinstance(evaluated_value, (int, float)):
                                self.errors.append(
                                    f"Type error: Expression '{entry.value}' evaluates to '{evaluated_value}', which cannot be assigned to float variable '{entry.name}' at line {entry.line}."
                                )
                    except ValueError as e:
                        self.errors.append(f"Type error: {e}")

    # ---------------- Analyze ----------------
    def analyze(self):
        """
        Main function for semantic analysis.
        Cleans the data, validates Define Statements, validates the symbol table, and checks the parse tree.
        """
        print("Starting semantic analysis...")
        print("----------------------------")
        self.clean_data()
        self.validate_define_statements()
        self.validate_symbol_table()

        print("\nSemantic Analysis Results")
        print("==============================")
        print("Errors:")
        if self.errors:
            for i, error in enumerate(self.errors, 1):
                print(f"{i}. {error}")
        else:
            print("No errors found.")

        print("\nFinal Verdict:")
        if self.errors:
            print("NO - Code not semantically correct.")
        else:
            print("YES - Code semantically correct.")
