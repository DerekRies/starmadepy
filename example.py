import starmadepy
import os
from starmadepy import starmade

"""
Sample file showing some basic usage of the starmadepy API
"""

def print_logic(l):
    # print l
    print '===================================='
    print 'Found %s Controller Entities' % l.get('size')
    print '===================================='
    for entity in l['entities']:
        print '  Entity at %s' % str(entity['pos'])
        print '  Found %s groups' % entity.get('ngroups')
        for group in entity.get('groups'):
            bid = group.get('id')
            print '    Group of: %s' % starmade.Block.map_id_to_name(bid)
            print '    Found %s blocks in group' % group.get('nblocks')
            for pos in group.get('positions'):
                print '      %s' % str(pos)
        print '-------------------'

def main():
    # template = starmade.Template.fromSMTPL('starmadepy/data/test-templates/AAAstandardgrey.smtpl', debug=True)
    t_dir = 'starmadepy/data/test-templates/activeorientation/'
    template = starmade.Template.fromSMTPL(
        t_dir + 'factoryoff.smtpl', debug=True)
    print template.count_by_block()


def tutorial1():
    tpl_name = 'starmadepy/data/test-templates/tutorial1.smtpl'
    template = starmade.Template.fromSMTPL(tpl_name)
    template.replace({'color': 'grey'}, {'color': 'orange'})
    template.save('starmadepy/data/test-templates/tutorial(out).smtpl')


def blueprint():
    # blueprint = 'starmadepy/data/test-blueprints/Isanth-VI'
    blueprint = 'starmadepy/data/test-blueprints/bptest4'
    bp = starmade.Blueprint.fromFolder(blueprint)
    logic = bp[1]
    print_logic(logic)

if __name__ == '__main__':
    # tutorial1()
    blueprint()