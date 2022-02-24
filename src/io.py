

#####################
#   I/O functions   #
#####################

# def parse_list(line):
#     c, *entries = line.strip().split(' ')
#     assert int(c) == len(entries)
#     return entries

def parse_name_int(line):
    """ parse a string followed by int """
    name, i = line.strip().split(' ')
    return name, int(i)


# def parse_int(line):
#     return int(line.strip())


def parse_ints(line):
    """ parse a string followed by int """
    ii = line.strip().split(' ')
    return [int(i) for i in ii]


def parse_name_ints(line):
    """ parse a string followed by int """
    name, *ii = line.strip().split(' ')
    return name, [int(i) for i in ii]


def list_to_str(l):
    """ Input: list
    Outputs formatted string with first size and then items split by spaces """
    return f"{len(l)} {' '.join(l)}"

