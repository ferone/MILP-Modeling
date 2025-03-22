import re
from typing import Dict, List, Tuple
from pulp import LpProblem, LpVariable, LpMaximize, LpMinimize

class ModelParser:
    def __init__(self):
        self.variables = {}
        self.constraints = []
        self.objective = None
        self.objective_type = None
        self.bounds = []

    def parse_file(self, file_path: str) -> LpProblem:
        """Parse the input file and create a PuLP problem."""
        with open(file_path, 'r') as file:
            content = file.read()

        # Parse variables first
        variables_section = re.search(r'VARIABLES:\s*(.*?)(?=\n\n|\Z)', content, re.DOTALL)
        if variables_section:
            var_names = [v.strip() for v in variables_section.group(1).split(',')]
            for var_name in var_names:
                if var_name:  # Skip empty strings
                    self.variables[var_name] = LpVariable(var_name, lowBound=0)

        # Parse objective
        objective_match = re.search(r'OBJECTIVE:\s*(maximize|minimize)\s*(.*?)(?=\n\n|\Z)', content, re.DOTALL)
        if objective_match:
            self.objective_type = LpMaximize if objective_match.group(1) == 'maximize' else LpMinimize
            # Parse the objective function expression
            objective_expr = objective_match.group(2).strip()
            self._parse_objective(objective_expr)

        # Create PuLP problem
        problem = LpProblem("MILP_Problem", self.objective_type)
        
        # Set the objective function
        if self.objective:
            problem += self.objective

        # Parse constraints
        constraints_section = re.search(r'CONSTRAINTS:\s*(.*?)(?=\n\n|\Z)', content, re.DOTALL)
        if constraints_section:
            constraints = [line.strip() for line in constraints_section.group(1).split('\n') if line.strip()]
            for constraint in constraints:
                constraint_expr = self._parse_expression(constraint)
                if constraint_expr:
                    problem += constraint_expr

        # Parse bounds
        bounds_section = re.search(r'BOUNDS:\s*(.*?)(?=\n\n|\Z)', content, re.DOTALL)
        if bounds_section:
            for line in bounds_section.group(1).split('\n'):
                if line.strip():
                    self._parse_bound(line.strip())

        return problem

    def _parse_expression(self, line: str):
        """Parse a mathematical expression into PuLP format."""
        try:
            # Split into left and right sides
            parts = re.split(r'(<=|>=|==)', line)
            if len(parts) != 3:
                return None

            left_expr, operator, right_value = parts
            right_value = float(right_value.strip())

            # Parse terms
            terms = re.findall(r'([+-]?\d*\.?\d*)\*?([a-zA-Z0-9_]+)', left_expr)
            pulp_expr = 0
            for coef, var_name in terms:
                if not coef or coef in ['+', '-']:
                    coef = float(coef + '1') if coef == '-' else 1.0
                else:
                    coef = float(coef)
                if var_name in self.variables:
                    pulp_expr += coef * self.variables[var_name]

            # Create constraint
            if operator == '<=':
                return pulp_expr <= right_value
            elif operator == '>=':
                return pulp_expr >= right_value
            else:  # ==
                return pulp_expr == right_value
        except Exception as e:
            print(f"Error parsing expression: {line}")
            print(f"Error details: {str(e)}")
            return None

    def _parse_objective(self, line: str):
        """Parse the objective function."""
        try:
            # Parse terms
            terms = re.findall(r'([+-]?\d*\.?\d*)\*?([a-zA-Z0-9_]+)', line)
            pulp_expr = 0
            for coef, var_name in terms:
                if not coef or coef in ['+', '-']:
                    coef = float(coef + '1') if coef == '-' else 1.0
                else:
                    coef = float(coef)
                if var_name in self.variables:
                    pulp_expr += coef * self.variables[var_name]
            self.objective = pulp_expr
        except Exception as e:
            print(f"Error parsing objective: {line}")
            print(f"Error details: {str(e)}")
            raise

    def _parse_bound(self, line: str):
        """Parse a single bound line."""
        try:
            parts = re.split(r'(<=|>=)', line)
            if len(parts) == 3:
                var_name, operator, value = parts
                var_name = var_name.strip()
                value = float(value.strip())
                
                if var_name in self.variables:
                    if operator == '<=':
                        self.variables[var_name].upBound = value
                    else:  # >=
                        self.variables[var_name].lowBound = value
        except Exception as e:
            print(f"Error parsing bound: {line}")
            print(f"Error details: {str(e)}") 