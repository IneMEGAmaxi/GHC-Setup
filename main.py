from pathlib import Path
import sys

import src.io as io
import src.solve as solve
from src import solve_random
from src import solve_branch

from typer import Typer
import typer

ExistingFile = typer.Argument(
    ...,
    exists=True,
    file_okay=True,
    dir_okay=False,
    writable=False,
    readable=True,
    resolve_path=True,
)

app = Typer()

OUTPUT_DIR = Path('output')

@app.command()
def random(filename: Path = ExistingFile, sol_limit: int = 20, stuck_limit: int = 1000):
    problem = io.parse_problem(filename)
    solution = solve_random.solve(*problem, sol_limit=sol_limit, stuck_limit=stuck_limit)
    io.write_solution(solution, OUTPUT_DIR / Path(filename).name.replace('.in', '.out'))


@app.command()
def branchbound(filename: Path = ExistingFile):
    problem = io.parse_problem(filename)
    solution = solve_branch.solve(*problem)
    io.write_solution(solution, OUTPUT_DIR / Path(filename).name.replace('.in', '.out'))


app()
