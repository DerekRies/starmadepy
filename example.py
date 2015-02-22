import starmadepy
import os
from starmadepy import starmade

"""
Sample file showing some basic usage of the starmadepy API
"""


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
    starmade.Blueprint.fromFolder(blueprint)

if __name__ == '__main__':
    # tutorial1()
    blueprint()