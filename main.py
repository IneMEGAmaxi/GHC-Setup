import sys
import src.io as io
import src.solve as solve


def main(filename):
    problem = io.parse_problem(filename)
    solution = solve.solve(*problem)
    io.write_solution(solution, filename + ".sol")


if __name__ == "__main__":
    assert len(sys.argv) == 2
    filename = sys.argv[1]
    main(filename)
