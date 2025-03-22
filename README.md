# MILP Problem Solver

A web-based Mixed Integer Linear Programming (MILP) solver with a modern chat-like interface.

## Features

- **Modern Chat Interface**: Clean, intuitive interface inspired by AI chat applications
- **Real-time Problem Solving**: Instant feedback and solutions
- **Problem Management**: Save, load, and delete problems
- **Natural Language Input**: Add constraints using natural language
- **Comprehensive Validation**: Robust error checking and validation
- **Dark Mode**: Eye-friendly dark theme interface

## Input Format

The solver accepts problems in the following format:

```
OBJECTIVE: maximize
3*x1 + 2*x2 + 4*x3

VARIABLES:
x1, x2, x3

CONSTRAINTS:
2*x1 + 1*x2 + 3*x3 <= 10
1*x1 + 2*x2 + 1*x3 <= 8
3*x1 + 2*x2 + 2*x3 <= 12

BOUNDS:
x1 >= 0
x2 >= 0
x3 >= 0
```

## Validation Features

The solver includes comprehensive validation to ensure correct problem formulation:

1. **Model Structure Validation**:
   - Checks for required sections (OBJECTIVE, VARIABLES, CONSTRAINTS, BOUNDS)
   - Ensures proper section formatting
   - Validates section order

2. **Objective Function Validation**:
   - Verifies "maximize" or "minimize" directive
   - Validates mathematical expression
   - Ensures linearity of the objective function

3. **Variable Validation**:
   - Checks for proper variable format (x1, x2, etc.)
   - Ensures variables are declared in VARIABLES section
   - Validates variable usage in constraints

4. **Constraint Validation**:
   - Verifies valid inequality signs (<=, >=, =)
   - Checks for linear expressions
   - Validates both sides of constraints
   - Ensures proper mathematical formatting

5. **Mathematical Expression Validation**:
   - Prevents non-linear terms (e.g., x1 * x2)
   - Validates operators and coefficients
   - Checks for balanced parentheses
   - Ensures proper variable formatting

## Natural Language Input

You can add constraints using natural language. Examples:

- "The sum of x1 and x2 must be less than 15"
- "x3 should be at least twice x1"
- "x1 plus 2 times x2 cannot exceed 20"

The system will automatically convert these to proper mathematical constraints.

## Error Handling

The solver provides clear error messages for common issues:

- Missing or invalid sections
- Non-linear expressions
- Invalid variable formats
- Malformed constraints
- Unbalanced parentheses
- Invalid operators
- Missing required components

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/MILP-Modeling.git
cd MILP-Modeling
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://127.0.0.1:5000`

## Usage

1. Enter your MILP problem in the text area
2. Click the arrow button to solve
3. View the solution in the chat history
4. Add new constraints using natural language
5. Save problems for later use
6. Load or delete saved problems from the sidebar

## Requirements

- Python 3.7+
- Flask
- PuLP
- NumPy

## License

This project is licensed under the MIT License - see the LICENSE file for details. 