from pathlib import Path
import sys

from src.problem import Problem
from src import solver1

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
def sol1(filename: Path = ExistingFile):
    problem = Problem.parse(filename)
    solution = solver1.solve(problem)
    solution.write()

@app.command()
def test():
    pass



app()
