

def parse_list(line):
    c, *entries = line.strip().split(' ')
    assert int(c) == len(entries)
    return entries


def write_list(l):
    pass


def parse_problem(path):
    customer_likes = list()
    customer_dislikes = list()
    with open(path) as f:
        customers = int(f.readline())
        for c in range(customers):
            customer_likes.append(parse_list(f.readline()))
            customer_dislikes.append(parse_list(f.readline()))
        while line := f.readline():
            print("extra line", line.strip())
        
    return customer_likes, customer_dislikes


def write_solution(solution, path):
    pass
