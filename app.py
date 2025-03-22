from flask import Flask, request, jsonify, render_template
from model_parser import ModelParser
import tempfile
import os
import traceback

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    try:
        # Get the problem description from the request
        problem_text = request.json.get('problem')
        if not problem_text:
            return jsonify({'error': 'No problem text provided'}), 400
        
        # Create a temporary file to store the problem
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp:
            tmp.write(problem_text)
            tmp_path = tmp.name
        
        try:
            # Parse and solve the problem
            parser = ModelParser()
            problem = parser.parse_file(tmp_path)
            
            # Solve the problem
            status = problem.solve()
            
            # Get the solution details
            solution = {
                'status': status,
                'objective_value': problem.objective.value(),
                'variables': {var.name: var.value() for var in problem.variables()},
                'solution_time': problem.solutionTime if hasattr(problem, 'solutionTime') else None,
                'is_optimal': status == 1,
                'is_infeasible': status == -1,
                'is_unbounded': status == -2
            }
            
            return jsonify(solution)
            
        except Exception as e:
            error_msg = f"Error solving problem: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)  # Log the error
            return jsonify({'error': str(e)}), 400
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(tmp_path)
            except:
                pass
    
    except Exception as e:
        error_msg = f"Server error: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)  # Log the error
        return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True) 