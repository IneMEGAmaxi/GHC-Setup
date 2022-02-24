from functools import lru_cache

from . import io
from . import util
from .worker import Worker
from .project import Project

import src.solution as solution


class Problem:
    def __init__(self, path, workers, projects):
        self.path = path

        self.workers = workers
        self.projects = projects

    def __str__(self):
        return f"workers: {str(self.workers)} \nprojects: {str(self.projects)}"

    def new_solution(self):
        return solution.Solution(self)

    @property
    @lru_cache(maxsize=1)
    def ingredients(self):
        return list(util.unique_entries_multiple(self.likes, self.dislikes))

    @property
    @lru_cache(maxsize=1)
    def L(self):
        return util.list_of_lists_to_matrix(self.likes, self.ingredients)

    @property
    @lru_cache(maxsize=1)
    def D(self):
        return util.list_of_lists_to_matrix(self.dislikes, self.ingredients)

    @staticmethod
    def parse(path):
        # TODO: Change
        workers = list()
        projects = list()
        with open(path) as f:
            worker_count, project_count = io.parse_ints(f.readline())

            # Workers / Contributors
            for c in range(worker_count):
                name, skill_count = io.parse_name_int(f.readline())
                w = Worker(name)
                for s in range(skill_count):
                    name, level = io.parse_name_int(f.readline())
                    w.skills[name] = level

                workers.append(w)

            for p in range(project_count):
                name, (days, max_score, best_before, role_count) = io.parse_name_ints(f.readline())
                project = Project(name, days, max_score, best_before)
                for r in range(role_count):
                    role, level = io.parse_name_int(f.readline())
                    project.addRole(role, level)

                projects.append(project)

            while line := f.readline():
                print("extra line", line.strip())

        return Problem(path, workers, projects)
