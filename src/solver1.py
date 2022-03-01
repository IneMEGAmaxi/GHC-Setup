from .problem import Problem


from tqdm.auto import tqdm
from .project import Project, SolvedProject
from .worker import Worker


def pick_workers(project: Project, availableWorkers) -> list:
    """ Return role -> person """
    roleCandidates = list()

    def initial_domains():
        for role, level in project.roleLevels:
            candidates = list()
            for candidate in availableWorkers:
                if candidate.skills.get(role, 0) >= level:
                    candidates.append(candidate)

            roleCandidates.append(candidates)
        return roleCandidates

    def update_domains(assignment, domains, assignedIndex):
        # print("domains", len(domains))
        # print("roleLevels", len(list(project.roleLevels)))
        newdomains = [list(candidates) for candidates in domains]
        assignedWorker = assignment[assignedIndex]
        for (role, level), candidates in zip(project.roleLevels, newdomains):
            if assignedWorker in candidates:
                candidates.remove(assignedWorker)

            if assignedWorker.skills.get(role, 0) >= level:
                for candidate in availableWorkers:
                    if candidate in assignment:
                        continue
                    if candidate.skills.get(role, 0) == level-1:
                        if candidate not in candidates:
                            candidates.append(candidate)

            # roleCandidates.append(candidates)
        return newdomains

    def best_variables(assignment, domains):
        to_sort = [(len(domains[index]), index) for index in range(len(assignment)) if assignment[index] is None]
        if len(to_sort) == 0:
            return None
        best = max(to_sort, key=lambda x: x[0])[1]
        return best
        # for index, domain in enumerate(domains):
        #     if assignment[index] is None:
        #         return index
        # return None

    def sort_values(index, domain):
        to_sort = list()
        for value in domain:
            score = 0
            role = project.roles[index]
            roleLevel = project.levels[index]
            skillLevel = value.skills.get(role, 0)
            if  roleLevel == skillLevel or roleLevel == skillLevel + 1:
                score += 10

            to_sort.append((score, value))

        return [v for k, v in sorted(to_sort, key=lambda x: x[0], reverse=False)][:1]

    def csp_solve(assignment, domains):
        # depth = sum(1 for a in assignment if a is not None)
        # print("depth", depth)
        if all([a is not None for a in assignment]):
            return assignment
        index = best_variables(assignment, domains)
        var_domain = domains[index]
        for value in sort_values(index, var_domain):
            newAssignment = assignment.copy()
            newAssignment[index] = value
            newDomains = update_domains(newAssignment, domains, index)
            newAssignment = csp_solve(newAssignment, newDomains)
            if newAssignment is None:
                continue
            if all([a is not None for a in newAssignment]):
                return newAssignment

        return None

    assignment = [None for _ in range(len(project.roles))]
    init_domains = initial_domains()

    return csp_solve(assignment, init_domains)


def solve(problem: Problem):
    timestamp = 0
    #remove max time_stamp
    # max_timestamp = 1000

    in_progress_projects = list()
    finished_projects = list()

    worker_pool = problem.workers.copy()

    projects = problem.projects.copy()
    while True:
        assignedOneProject = False
        print("current timestamp: " + str(timestamp))
        # handling finished projects
        for p in in_progress_projects:
            if p.end_day <= timestamp:
                in_progress_projects.remove(p)
                finished_projects.append(p)
                for index, worker in enumerate(p.role_assignment):
                    worker_pool.append(worker)
                    role, roleLevel = list(p.project.roleLevels)[index]
                    level = worker.skills.get(role, 0)
                    if level <= roleLevel:
                        worker.skills[role] = level + 1

        # looking to start new projects
        promising_projects = list(sorted(projects, key=lambda item: item.heuristic(timestamp), reverse=True))[:200]

        # print("workers", worker_pool)

        for project in promising_projects:
            # print(len(project.roles))
            # print(project.name)

            # try:
            wl = pick_workers(project, worker_pool)
            # except KeyboardInterrupt as e:
            #     print("exception!")
                # continue

            if wl:
                # print(wl)
                #found workers
                #remove workers form pool
                pp = SolvedProject(project, timestamp)
                for w in wl:
                    worker_pool.remove(w)
                    pp.role_assignment.append(w)

                assignedOneProject = True
                in_progress_projects.append(pp)
                projects.remove(project)

        maxPossibleScore = max(p.scoreIfStarted(timestamp) for p in promising_projects)
        if maxPossibleScore == 0:
            print("no more promising projects with score > 0")
            break

        if not assignedOneProject:
            # Nothing possible anymore
            if len(in_progress_projects) == 0:
                print("couldn't schedule anything anymore")
                break

            timestamp = min(p.end_day for p in in_progress_projects)
        else:
            timestamp += 1
        # if(timestamp > max_timestamp):
        #     break


    s = problem.new_solution()
    s.completed = finished_projects
    return s


