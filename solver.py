from pulp import LpProblem, LpStatus
from typing import Dict, Any
import time

class MILPSolver:
    def __init__(self):
        self.solution_time = 0
        self.status = None
        self.objective_value = None
        self.variable_values = {}

    def solve(self, problem: LpProblem) -> Dict[str, Any]:
        """Solve the MILP problem and return the results."""
        start_time = time.time()
        
        # Solve the problem
        status = problem.solve()
        
        # Record solution time
        self.solution_time = time.time() - start_time
        
        # Get solution status
        self.status = LpStatus[status]
        
        # Get objective value
        self.objective_value = problem.objective.value()
        
        # Get variable values
        for var in problem.variables():
            self.variable_values[var.name] = var.value()
        
        return self._generate_report()

    def _generate_report(self) -> Dict[str, Any]:
        """Generate a detailed report of the solution."""
        return {
            'status': self.status,
            'objective_value': self.objective_value,
            'solution_time': self.solution_time,
            'variable_values': self.variable_values,
            'is_optimal': self.status == 'Optimal',
            'is_infeasible': self.status == 'Infeasible',
            'is_unbounded': self.status == 'Unbounded'
        }

    def print_solution(self):
        """Print a formatted solution report."""
        print("\n=== MILP Solution Report ===")
        print(f"Status: {self.status}")
        print(f"Objective Value: {self.objective_value}")
        print(f"Solution Time: {self.solution_time:.2f} seconds")
        
        print("\nVariable Values:")
        for var_name, value in self.variable_values.items():
            print(f"{var_name} = {value}")
        
        print("\nSolution Analysis:")
        if self.status == 'Optimal':
            print("✓ Optimal solution found")
        elif self.status == 'Infeasible':
            print("✗ No feasible solution exists")
        elif self.status == 'Unbounded':
            print("✗ Problem is unbounded")
        else:
            print("? Solution status unknown") 