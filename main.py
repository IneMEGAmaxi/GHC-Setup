from pathlib import Path
import sys

from src.problem import Problem
from src import solve_random
from src import solve_branch
from src import solve_local

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


@app.command()
def random(filename: Path = ExistingFile, sol_limit: int = 20, stuck_limit: int = 1000):
    problem = Problem.parse(filename)
    solution = solve_random.solve(problem, sol_limit=sol_limit, stuck_limit=stuck_limit)
    solution.write()


@app.command()
def branchbound(filename: Path = ExistingFile):
    problem = Problem.parse(filename)
    solution = solve_branch.solve(problem)
    solution.write()


@app.command()
def local(filename: Path = ExistingFile):
    problem = Problem.parse(filename)
    solution = solve_local.solve(problem)
    solution.write()


app()
