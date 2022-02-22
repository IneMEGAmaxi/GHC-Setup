

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
