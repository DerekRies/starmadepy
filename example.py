import starmadepy
import os
from starmadepy import starmade

"""
Sample file showing some basic usage of the starmadepy API
"""


def main():
    # pkg_loc = starmadepy.__file__
    # print pkg_loc
    # t1 = starmade.Template.fromSMTPL(
    #     'starmadepy/data/test-templates/connections/pulse test 1.smtpl')
    # t1._print_connections()
    # # print len(t1.get_connection_groups())
    # print t1.version
    # print t1.bound_lower
    # print t1.bound_upper
    # print t1.box_dimensions()

    # template = starmade.Template.fromSMTPL(
    #     'starmadepy/data/test-templates/tutorial1.smtpl')
    # print template.count_by_block()
    # template._print_block_orientations()
    # print '-------------'
    # saved_name = 'starmadepy/data/test-templates/tutorial1-save.smtpl'
    # template.save(saved_name)
    # t2 = starmade.Template.fromSMTPL(saved_name)
    # t2._print_block_orientations()
    # os.remove(saved_name)

    # template = starmade.Template.fromSMTPL('starmadepy/data/test-templates/AAAstandardgrey.smtpl', debug=True)
    t_dir = 'starmadepy/data/test-templates/activeorientation/'
    template = starmade.Template.fromSMTPL(
        t_dir + 'cornertest.smtpl', debug=True)
    print template.count_by_block()
    # template._print_block_orientations()
    # template._print_block_states()


if __name__ == '__main__':
    main()