# Starmadepy v0.1

A Python library for manipulating Starmade game data.

## Overview

Starmadepy is a simple python library that makes parsing and manipulating Starmade game data easy. As this project is fairly new, the only file type that is currently supported is the `.smtpl`, or **Starmade Template** file type.

[Docs](http://starmadepy.readthedocs.org/en/latest/)


## Example

Maybe you created a really nice component that utilizes blocks, wedges, corners, pentas, and tetras in a couple different colors and you'd like to generate some copies of this template in different colors.

The following code will open a template file, select all the blocks with the color grey and then replace them with orange.

```python
from starmadepy import starmade

# Loads a template file named sometemplatefile.smtpl
# Replaces all grey colored blocks, with orange equivalents

template = starmade.Template.fromSMTPL('sometemplatefile.smtpl')
template.replace({'color': 'grey'}, {'color': 'orange'})
template.save('outtemplatefile.smtpl')
```

![Converted Template](docs/img/tutorial1.png)

## Installation

It is recommended that you use virtualenv or the virtualenvwrapper.

    pip install starmadepy


## Contributing

Fork, clone, `pip install -r requirements.txt` and run the tests with `py.test`
Full guide in the [docs](http://starmadepy.readthedocs.org/en/latest/contributing/)


