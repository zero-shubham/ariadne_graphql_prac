test = None


def set_var(value):
    global test
    test = value


def get_var():
    return test


def yo(f):
    print(f, "==")
    return f