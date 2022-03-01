
class Project:

    #make roles a list of tuples
    def __init__(self, name:str, days_to_complete:int, max_score:int, best_before:int):
        self.name = name
        self.days_to_complete = days_to_complete
        self.max_score = max_score
        self.best_before = best_before
        self.roles = list()
        self.levels = list()

    def addRole(self, role, level):
        self.roles.append(role)
        self.levels.append(level)

    @property
    def roleLevels(self):
        return zip(self.roles, self.levels)

    def scoreIfStarted(self, timestamp):
        penalty = timestamp + self.days_to_complete - 1 - self.best_before
        if penalty < 0:
            penalty = 0
        return max(0, self.max_score - penalty)

    def heuristic(self, timestamp):
        # optimise score increase: max score per time invested
        opt = self.scoreIfStarted(timestamp)/self.days_to_complete
        # slight preference for projects completed close to/ after deadline
        #TODO preference for project with high number of contributers?
        a = 10 #TODO Tune parameter
        days_left = self.best_before - (timestamp + self.days_to_complete -1)
        opt -= days_left/a
        return opt
        #TODO: IMPROVE HEURISTIC
        #for lvl in self.levels:
        #   overtime = overtime - lvl

    def __str__(self):
        return self.name + \
               "\ndtc: " + str(self.days_to_complete) + \
               "\nmaxscore:" + str(self.max_score) +\
               "\nbb:" + str(self.best_before) + \
               "\nroles:" + str(self.roles) +\
               "\nrolelvls:"+ str(self.roleLevels)

    def __repr__(self):
        return str(self)


class SolvedProject:
    def __init__(self, project, start_day):
        self.project = project

        # list of role assignment with same order as project.roles
        self.role_assignment = list()

        self.start_day = start_day
        self.end_day = start_day + self.project.days_to_complete - 1
