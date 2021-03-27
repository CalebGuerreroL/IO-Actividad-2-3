from cplex import Cplex, infinity
from cplex.exceptions import CplexError


problem = Cplex()

problem.objective.set_sense(problem.objective.sense.minimize)

objective = [5.0, 4.0]

constraints_matrix = [
  [1.0, 1.0],
  [10.0, 6.0]
]

col_names = ["x1", "x2"]

row_names = ["c1", "c2"]

rhs = [5.0, 45.0]

types = ["I", "I"]

senses = ["L", "L"]

constraints = []

for i in constraints_matrix:
  new_item = [col_names]
  new_item.append(i)
  constraints.append(new_item)

problem.variables.add(
  obj = objective,
  names =  col_names,
  types = types
)

problem.linear_constraints.add(
  lin_expr = constraints,
  senses = senses,
  rhs = rhs,
  names = row_names
)

problem.solve()

print(f"Objective value: {problem.solution.get_objective_value()}")
print(list(zip(col_names, problem.solution.get_values())))