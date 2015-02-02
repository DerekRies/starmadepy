# Starmadepy v0.1

A Python library for manipulating Starmade game data

## Overview

Starmadepy is a simple python library that makes parsing and manipulating Starmade game data easy. As this project is fairly new, the only file type that is currently supported is the `.smtpl`, or **Template** file type.


    from starmadepy import starmade

    # Loads a template file named sometemplatefile.smtpl
    # Replaces all grey colored blocks, with orange equivalents
    template = starmade.Template.fromSMTPL('sometemplatefile.smtpl')
    template.replace({'color': 'grey'}, {'color': 'orange'})


## Installation

It is recommended that you use virtualenv or the virtualenvwrapper.

    pip install starmadepy


## Projects using Starmadepy

Coming soon