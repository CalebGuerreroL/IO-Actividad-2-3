# 1845935 - Angel Caleb Guerrero Luna
# 1844214 - Mario Eduardo Lara Loredo

from cplex import Cplex, infinity
from cplex.exceptions import CplexError
import os

def list_int(line: str) -> list:
  numbers = line.split(" ")
  values = []

  for number in numbers:
    try:
      values.append(int(number))
    except ValueError:
      continue

  return values


def get_data(path: str, mode: str) -> (list, list):
  with open(path, mode) as file:
    rows, columns = list_int(file.readline())
    costs = []
    restrictions = []

    while len(costs) != columns:
      costs += list_int(file.readline())

    for _ in range(rows):
      length = list_int(file.readline()).pop()
      restriction = []

      while len(restriction) != length:
        restriction += list_int(file.readline())
      
      restrictions.append(restriction)

    return restrictions, costs


# ubicación del problema a resolver
path = "./data/scpe/scpe5.txt"
restrictions, objective = get_data(path, "r")

col_number = len(objective)
row_number = len(restrictions)

constraints_matrix = []

for restriction in restrictions:
  constraint = []
  for i in range(1, col_number + 1):
    constraint.append(1 if i in restriction else 0)
  
  constraints_matrix.append(constraint)

objective = [float(i) for i in objective]  
col_names = [f"x{i}" for i in range(1, col_number + 1)]
row_names = [f"c{i}" for i in range(1, row_number + 1)]
rhs = [1.0] * row_number
types = ["I"] * col_number
senses = ["G"] * row_number

constraints = []

for i in constraints_matrix:
  new_item = [col_names]
  new_item.append(i)
  constraints.append(new_item)


problem = Cplex()

problem.objective.set_sense(problem.objective.sense.minimize)

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