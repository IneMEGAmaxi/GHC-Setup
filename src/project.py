
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

    def scoreIfStartedOn(self, timestamp):
        overtime = self.best_before - (timestamp + self.days_to_complete) + 1
        return max(0, self.max_score - overtime)

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
    def __init__(self, project, role_assignment: dict, start_day):
        self.project = project
        self.role_assignment = role_assignment
        self.start_day = start_day
        self.end_day = start_day + self.project.days_to_complete -1
        pass
