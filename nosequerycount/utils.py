class ColoredString(str):
    """
    Utility string class for colored terminal output
    """
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

    def __new__(cls, seq, color):
        return str.__new__(cls, '\033[1;%dm%s\033[0m' % (30 + color, seq))
