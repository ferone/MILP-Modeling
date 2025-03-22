import sys
import argparse
from model_parser import ModelParser
from solver import MILPSolver

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='MILP Modeling and Solver')
    parser.add_argument('input_file', help='Path to the input file containing the MILP problem')
    args = parser.parse_args()

    try:
        # Create parser and solver instances
        parser = ModelParser()
        solver = MILPSolver()

        # Parse the input file
        print(f"\nParsing problem from {args.input_file}...")
        problem = parser.parse_file(args.input_file)

        # Solve the problem
        print("Solving the MILP problem...")
        results = solver.solve(problem)

        # Print the solution
        solver.print_solution()

    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 