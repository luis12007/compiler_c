import pydot

def process_syntax_tree(syntax_tree, output_name):
    """
    Processes a syntax tree and generates a textual and graphical representation.

    :param syntax_tree: List of tuples representing the syntax tree.
    :param output_name: Base name of the output file (without extension).
    """
    # Prepare a textual representation of the tree
    lines = []
    current_line = []
    
    for node in syntax_tree:
        if node[2] in ["Rule Applied", "Regex Match"]:  # Start a new line for these cases
            if current_line:  # Add current line to lines if not empty
                lines.append(" -> ".join(current_line))
                current_line = []
            current_line.append(node[0])
            current_line.extend(node[1] if isinstance(node[1], list) else [node[1]])
        elif node[2] == "Terminal Match":  # End of the current line
            current_line.append(node[1])
            lines.append(" -> ".join(current_line))
            current_line = []

    # Write the textual representation to a file with UTF-8 encoding
    with open(f"{output_name}.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # Create a graph using pydot for visual representation
    graph = pydot.Dot(graph_type="digraph", rankdir="TB")

    # Add nodes and edges to the graph
    node_counter = 0
    parent_stack = []
    for node in syntax_tree:
        node_label = f"{node[0]} ({node[2]})"
        current_node = pydot.Node(str(node_counter), label=node_label)
        graph.add_node(current_node)

        # Connect to the parent node if available
        if parent_stack:
            graph.add_edge(pydot.Edge(parent_stack[-1], str(node_counter)))

        # Push or pop the stack based on rule type
        if node[2] == "Rule Applied":
            parent_stack.append(str(node_counter))
        elif node[2] == "Terminal Match":
            if parent_stack:
                parent_stack.pop()

        node_counter += 1

    # Save the graph in multiple formats
    graph.write_pdf(f"{output_name}.pdf")

    print(f"\nSyntax tree textual representation saved as {output_name}.txt and {output_name}.pdf \n")
