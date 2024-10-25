
from flask import Flask, request, jsonify, render_template
from rule_engine import create_rule as create_rule_ast, evaluate_rule, combine_rules as combine_rules_logic, reconstruct_ast




app = Flask(__name__)

# Home page route to render an index HTML template
@app.route('/')
def index():
    return render_template('index.html')

# Route to create a rule from a rule string and return its AST
@app.route('/api/create_rule', methods=['POST'])
def create_rule_endpoint():
    try:
        # Extract the rule string from the request body
        rule_string = request.json.get('rule_string', '')

        if not rule_string:
            return jsonify({'error': 'Rule string cannot be empty.'}), 400

        # Create the AST from the rule string
        ast = create_rule_ast(rule_string)
        print(f"Generated AST: {ast}")  # Debugging output

        if ast is None:
            return jsonify({"error": "Failed to create AST from rule. Please check the rule syntax."}), 400

        # Return the AST as a dictionary for JSON serialization
        return jsonify({'ast': ast.to_dict()}), 200
    except Exception as e:
        print(f"Error in create_rule_endpoint: {e}")  # Log the error for debugging
        return jsonify({'error': str(e)}), 400

# Route to combine multiple rules and return the combined AST
@app.route('/api/combine_rules', methods=['POST'])
def combine_rules_endpoint():
    try:
        data = request.get_json()
        print("Received data for combining rules:", data)  # Log the incoming data

        # Extract rules from the incoming data
        rule_strings = data.get('rules', [])
        if not isinstance(rule_strings, list) or not rule_strings:
            return jsonify({'error': 'No valid rules provided'}), 400

        # Parse each rule and ensure the AST is created successfully
        rules = []
        for rule in rule_strings:
            if isinstance(rule, str) and rule.strip():  # Ensure rule is a non-empty string
                ast = create_rule_ast(rule)
                if ast is None:
                    print(f"Failed to parse rule: {rule}")  # Debugging output
                    return jsonify({"error": f"Failed to parse rule: {rule}"}), 400
                rules.append(ast)
            else:
                return jsonify({"error": "All rules must be non-empty strings."}), 400

        print("Parsed ASTs:", [ast.to_dict() for ast in rules])  # Log the ASTs

        # Check if there are valid rules to combine
        if not rules:
            return jsonify({'error': 'No valid rules to combine'}), 400

        # Combine the rules using a logical operator (AND/OR, etc.)
        combined_ast = combine_rules_logic(rules)

        # Check if combined AST is None
        if combined_ast is None:
            return jsonify({'error': 'Failed to combine rules.'}), 500

        # Return the combined AST as a dictionary for JSON serialization
        return jsonify({"combined_ast": combined_ast.to_dict()}), 200
    except Exception as e:
        print(f"Error combining rules: {str(e)}")  # Debugging output
        return jsonify({"error": str(e)}), 500

# Route to evaluate a rule (AST) against provided data
@app.route('/api/evaluate_rule', methods=['POST'])
def evaluate_rule_endpoint():
    try:
        # Extract the AST and data from the request body
        ast_data = request.json.get('ast')
        data = request.json.get('data')

        if not ast_data or not data:
            return jsonify({"error": "AST and data must be provided."}), 400
        
        # Reconstruct the AST from the provided dictionary
        ast = reconstruct_ast(ast_data)

        # Evaluate the rule against the input data
        result = evaluate_rule(ast, data)

        return jsonify({"result": result}), 200
    except Exception as e:
        print(f"Error evaluating rule: {str(e)}")  # Debugging output
        return jsonify({"error": str(e)}), 400

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)











