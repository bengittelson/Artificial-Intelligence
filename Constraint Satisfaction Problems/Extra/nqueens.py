import Testing
import BinaryCSP

if __name__ == '__main__':
    lines = Testing.get_lines('nqueens.csp')
    my_csp = Testing.csp_parse(lines)
    print BinaryCSP.solve(my_csp)
