# from flask import Flask, request, jsonify, render_template 
# from rule_engine import create_rule, evaluate_rule, combine_rules

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/api/create_rule', methods=['POST'])
# def create_rule_endpoint():
#     rule_string = request.json.get('rule')
#     try:
#         ast = create_rule(rule_string)
#         return jsonify({"ast": str(ast)}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400

# @app.route('/api/combine_rules', methods=['POST'])
# def combine_rules_endpoint():
#     rule_strings = request.json.get('rules')
#     try:
#         rules = [create_rule(rule) for rule in rule_strings]
#         combined_ast = combine_rules(rules)
#         return jsonify({"combined_ast": str(combined_ast)}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400

# @app.route('/api/evaluate_rule', methods=['POST'])
# def evaluate_rule_endpoint():
#     ast = request.json.get('ast')  # Assuming this is a string representation
#     data = request.json.get('data')
#     try:
#         result = evaluate_rule(ast, data)
#         return jsonify({"result": result}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400

# if __name__ == "__main__":
#     app.run(debug=True)



from flask import Flask, request, jsonify, render_template
from rule_engine import create_rule, evaluate_rule, combine_rules, reconstruct_ast

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/create_rule', methods=['POST'])
def create_rule_endpoint():
    rule_string = request.json.get('rule')
    try:
        ast = create_rule(rule_string)
        return jsonify({"ast": str(ast)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/combine_rules', methods=['POST'])
def combine_rules_endpoint():
    rule_strings = request.json.get('rules')
    try:
        rules = [create_rule(rule) for rule in rule_strings]
        combined_ast = combine_rules(rules)
        return jsonify({"combined_ast": str(combined_ast)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/evaluate_rule', methods=['POST'])
def evaluate_rule_endpoint():
    ast_data = request.json.get('ast')
    data = request.json.get('data')
    
    try:
        ast = reconstruct_ast(ast_data)  # Convert back to Node structure
        result = evaluate_rule(ast, data)
        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)


