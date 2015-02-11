import starmade

"""
Sample file showing some basic usage of the starmadepy API
"""


def main():
    t1 = starmade.Template.fromSMTPL(
        'data/test-templates/connections/pulse test 1.smtpl')
    t1._print_connections()
    # print len(t1.get_connection_groups())
    print t1.version
    print t1.bound_lower
    print t1.bound_upper
    print t1.box_dimensions()


if __name__ == '__main__':
    main()