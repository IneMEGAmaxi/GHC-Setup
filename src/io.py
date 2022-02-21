

#####################
#   I/O functions   #
#####################


def parse_list(line):
    c, *entries = line.strip().split(' ')
    assert int(c) == len(entries)
    return entries


def list_to_str(l):
    """ Input: list
    Outputs formatted string with first size and then items split by spaces """
    return f"{len(l)} {' '.join(l)}"


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
    """ Writes the solution to new file
    Solution = type list """
    with open(path, mode='w') as f:
        pizza = list_to_str(solution)
        f.write(pizza + '\n')
