
class Worker:

    def __init__(self, name):
        self.name = name
        self.skills = dict()

    def __str__(self):
        return self.name + ": "+str(self.skills)

    def __repr__(self):
        return str(self)


def get_workers(workers, skill, minimal_lvl, ideal_level = -1):
    out = list()
    for w in workers:
        if skill in w.skills.keys():
            out.append(w)
    return out


if __name__ == '__main__':
    w = Worker("tim")
    w.skills = {"html":3, "cpp": 2}
    j = Worker("Joey")
    j.skills = {"ai dingen": 8, "python": 5}

    print(get_workers([j, w], "ai dingen", 3))


