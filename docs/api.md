API Documentation
==============

- - -

Classes
--------------

## Block
The Block class represents Starmade's in-game blocks, and supports operations to easily change properties of a block while maitaining others.

### Properties

  >**name** *String*  
  The name of the block as it is referred to in Starmade. ex: 'Grey Hull'

  >**id** *Int*  
  The item ID as it is identified in Starmade. ex: 'Grey Standard Armor' is 5

  >**color**

  >**tier**

  >**shape**

  >**posx** *Int*  
  The x coordinate this block is located at

  >**posy** *Int*  
  The y coordinate this block is located at

  >**posz** *Int*  
  The z coordinate this block is located at

  >**orientation** *Int*  
  An integer 0-15 that represents which direction the block is oriented

  >**active** *Boolean*  
  Active state refers to the on/off of computers, logic, and lights; Additionally the closed/open state of doors. ON and OPEN are both a True state

  >**door** *Boolean*

**Class Methods**

  >**Block**( item_id, x=0, y=0, z=0 **)

  >Block.**from_itemname**(name)

  >Block.**map_name_to_id**(name)

  >Block.**map_id_to_name**(name)

  >Block.**search**(\*\*kwargs)


**Methods**

- - -

### Template
The Template class handles the loading and saving of `.smtpl` (Starmade Template) files, as well as some operations that support transforming groups of blocks.

**Properties**

**Class Methods**

**Methods**

- - -