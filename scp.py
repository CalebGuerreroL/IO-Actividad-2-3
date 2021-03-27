from cplex import Cplex, infinity
from cplex.exceptions import CplexError
import os

def list_int(line: str) -> list:
  list_line = line.split(" ")
  values = []

  for number in list_line:
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

    while costs.__len__() != columns:
      costs += list_int(file.readline())

    for _ in range(rows):
      length = list_int(file.readline()).pop()
      restriction = []

      while restriction.__len__() != length:
        restriction += list_int(file.readline())
      
      restrictions.append(restriction)

    return restrictions, costs


path = "./scpa1.txt"
mode = "r"

problem = Cplex()

problem.objective.set_sense(problem.objective.sense.minimize)

restrictions, objective = get_data(path, mode)

constraints_matrix = []

for restriction in restrictions:
  constraint = []
  for i in range(1, objective.__len__()+1):
    constraint.append(1 if i in restriction else 0)
  
  constraints_matrix.append(constraint)

objective = list(map(float, objective))  

col_names = []
row_names = []
rhs = []
types = []
senses = []

for i in range(1, objective.__len__()+1):
  col_names.append(f"x{i}")
  types.append("I")

for i in range(1, restrictions.__len__()+1):
  row_names.append(f"c{i}")
  senses.append("G")
  rhs.append(1.0)

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