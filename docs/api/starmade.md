# `starmade` Module

    from starmadepy import starmade

The starmade module is the main module at this time containing several classes related to deserializing, manipulating blocks, and reserializing starmade template files.

- - -

## `Block` Class

The Block class provides an interface for accessing data from the starmade block list, as well as to represent an actual block in a BlockGroup to be modified.

### **Example**

```
from starmadepy import starmade

# Creating a Block in two different ways, the first with the item ID
# and second, by using the item's in game name

block = starmade.Block(5)
block2 = starmade.Block.from_itemname('Grey Standard Armor')
block.info()
```

### **Properties**

  - `active` **Boolean** Represents the active state of blocks like lights, factories, logic, and doors. ON/ACTIVE/OPEN states are all represented as true, whereas OFF/INACTIVE/CLOSED are all False values

  - `color` **String** This block's color. Only supported by hull and lights.

  - `door` **Boolean** True if this block is a door object.

  - `hitpoints` **Integer** The health value of this block.

  - `item_id` **Integer** The Block ID used by Starmade

  - `name` **String** This block's in-game name.

  - `orientation` **Integer** An integer 0-23 depending on this blocks shape that represents the blocks current rotation. Corners have the most options in orientation (24) while most blocks will only support 6 orientations (0-5). **Warning:** This is likely to change, and an easier interface will replace it, one that represents each axis of rotation individually.

  - `posx` **Integer** Represents this block's current x coordinate in space, relative to the origin. (Origin changes depending on the BlockGroup)

  - `posy` **Integer** Represents this block's current y coordinate in space, relative to the origin. (Origin changes depending on the BlockGroup)

  - `posz` **Integer** Represents this block's current z coordinate in space, relative to the origin. (Origin changes depending on the BlockGroup)

  - `shape` **Integer** Represents which shape this block is:
      1. Normal Block
      2. Wedge
      3. Corner
      4. Penta
      5. Tetra

  - `tier` **Integer** Represents which armor tier level this block is:
      1. Basic
      2. Standard
      3. Advanced
      4. Crystal
      5. Non-Hull is also represented as 0


### **@classmethods**

These are the methods that are attached to the class themselves, and not a particular instance of `Block`

###starmade.Block(item_id)
Constructor method to create a new `Block` instance.

>**Parameters**

 >- **item_id** - Item id to create a new block of that type.

 >**Returns**

 >- A `Block` object of type `item_id`

- - -

###starmade.Block.from_itemname(item_name)
Additional Constructor method to create new `Block` instances by supplying an item name instead of an ID.

>**Parameters**

 >- **item_name** - Item Name to create a new block of that type.

>**Returns**

 >- A `Block` object of type `item_name`

- - -

###starmade.Block.from_stream(stream)
**Private Method** used to deserialize the 3 bytes of block data from a `BinaryStream` that can be reused by Templates and Blueprints alike

>**Parameters**

 >- **stream** - A `BinaryStream` object currently being read from.

>**Returns**

 >- A `Block` object with the properties that were stored in the binary file.

- - -

###starmade.Block.map_id_to_name(item_id) 
A convenience method to get the name of an item if you know the ID of it.

>**Parameters**

 >- **item_id** - An `integer` of the blocks id you wish to get the name of

>**Returns**

 >- A `string` containing the blocks name.

- - -

###starmade.Block.map_name_to_id(name) 
A convenience method to get the ID of an item if you know the name of it.

>**Parameters**

 >- **item_name** - A `string` of the blocks name.

>**Returns**

 >- An `integer` of the blocks ID.

- - -

###starmade.Block.search(**kwargs) 
Searches the list of blocks to find those matching the parameters provided. Keep in mind this doesn't search through block instances, just the block "database". If you're looking to query for block instances, those methods are handled in the BlockGroup class and children. Generally used to get back a block of the same type with a differing detail to then be fed into the `change_block_data()` method.

>**Parameters**

 >- **kwargs** - A dictionary of block properties you wish to search.

>**Returns**

 >- A list of dictionaries holding block data, these are not Block objects though.

- - -


### **Methods**

- - -

###starmade.Block.serialize_to_stream(stream)
**Private Method** used to serialize the 3 bytes of block data into a `BinaryStream` that can be reused by Templates and Blueprints alike

>**Parameters**

 >- **stream** - A `BinaryStream` object currently being written to.

>**Returns**

 >- `None`

- - -

###starmade.Block.copy()
Generates a copy of this block, with the same attributes (including position).

>**Returns**

 >- A new `Block` instance

- - -

###starmade.Block.change_block_data(new_block)
Replaces the attributes of a `Block` with some new provided block data. Can cause unexpected errors if not used in conjunction with `search()` because of improper new_block data.

>**Parameters**

 >- **new_block** - A `dictionary` with Block properties as keys that you wish to change.

>**Returns**

 >- `None`

- - -

###starmade.Block.change_color(new_color)
Changes a block's color while preserving it's other attributes.

>**Parameters**

 >- **new_color** - A `string` of the block's new color.

>**Returns**

 >- `None`

- - -

###starmade.Block.change_tier(new_tier)
Changes a block's armor tier level while preserving it's other attributes.

>**Parameters**

 >- **new_tier** - An `integer` of the blocks new tier level.

>**Returns**

 >- `None`

- - -

###starmade.Block.change_tier_word(new_tier)
Convenience method to change a block's armor tier level, with the English representation of the tier level, while preserving it's other attributes.

>**Parameters**

 >- **new_tier** - A `string` of the blocks new tier level.

>**Returns**

 >- `None`

- - -

###starmade.Block.change_shape(new_shape)
Changes a block's shape while preserving it's other attributes.

>**Parameters**

 >- **new_shape** - An `integer` of the blocks new shape.

>**Returns**

 >- `None`

- - -

###starmade.Block.change(**kwargs)
Convenience method for `change_block_data()` that preserves attributes not provided.

>**Parameters**

 >- **new_tier** - An `integer` of the blocks new tier level.

>**Returns**

 >- `None`

- - -

###starmade.Block.move_to(nx=0, ny=0, nz=0)
Moves this block to a new position

>**Parameters**

 >- **nx** - `integer` - Block's new x coordinate.
 >- **ny** - `integer` - Block's new y coordinate
 >- **nz** - `integer` - Block's new z coordinate

>**Returns**

 >- `None`

- - -

###starmade.Block.get_position()
Get's the position of this block. Coordinates are relative to the origin of whatever group they may be a part of.

>**Returns**

 >- A `Tuple` of coordinates in the form of (x,y,z)


###starmade.Block.info()
**Debug Method** used for printing some of the attributes of this block.

- - -

## `BlockGroup` Class

`BlockGroup` is a base class that provides the common interface for interacting with blocks at a group level wherever `Block`s are found, either generated, in Templates, or in Blueprints.

### **Properties**

 - `blocks` - A list of `Blocks` belonging to the group
 - `bound_lower` - (x,y,z) coordinates for the lower bound in the bounding box
 - `bound_upper` - (x,y,z) coordinates for the upper bound in the bounding box
 - `connections` - A list of tuples, or connection pairs. `(Block, Block)`

### **Methods**

- - -

###starmade.BlockGroup()
Creates a new BlockGroup. It is not normally recommended to create BlockGroups as they have no way serialize their content. But in the future you may be able to create a template or blueprint from a BlockGroup and vice versa for more flexibility.

>**Returns**

 >- `BlockGroup` instance

- - -

###starmade.BlockGroup.empty()
Removes all the blocks and connections from the BlockGroup, leaving it 'empty'.

>**Returns**

 >- `None`

- - -

###starmade.BlockGroup.get_connection_groups()
Connections are stored in memory as pairs, but are serialized as a group of connections (master, slave, slave, slave, slave). This method is used in the serialization process to get back these groups.

>**Returns**

 >- `2D List` of `Blocks` as connection groups. `[[master, slave], [master,slave,slave]]`

- - -

###starmade.BlockGroup.num_blocks()
Returns the number of blocks in this group (the length of the blocks list)

>**Returns**

 >- `integer` number of blocks in this group

- - -

###starmade.BlockGroup.num_connections()
Gets the number of connection pairs (blocks linked with C + V) that are stored in this BlockGroup.

>**Returns**

 >- `integer` number of pairs of connected, or linked, blocks

- - -

###starmade.BlockGroup.box_dimensions()
Returns the size of this group (in blocks) as a cube that contains the entire group. (The min and max of every axis)

>**Returns**

 >- `Tuple` of the form (x,y,z)

- - -

###starmade.BlockGroup.count_by_block()
Helpful method to get a count of block types contained in this group.

>**Returns**

 >- `Dictionary` of block counts ex: `{'Activation Module': 13}`

- - -

###starmade.BlockGroup.add(block)
Adds a `Block` instance to this group.

>**Parameters**

 >- **block** - `Block` - Block instance to be added to the group

>**Returns**

 >- `None`

- - -

###starmade.BlockGroup.replace(source_query, changes)
Match all the blocks belonging to this group that meet the `source_query`, and then apply the following `changes` to those blocks. Used to select a group of blocks and then transform them in a batch. Convenience method wrapping both `BlockGroup.get_all_blocks()` and `Block.change()`.

>**Parameters**

 >- **source_query** - `Dictionary` - Block properties being queried for in the group.
 >- **changes** - `Dictionary` - Block property modifications that will be applied to blocks matching the source query.

>**Returns**

 >- `None`

**Example**

```
# Replace Grey Blocks with Orange Blocks
template = Starmade.Template.fromSMTPL('sometemplate.smtpl')
template.replace({'color': 'grey'}, {'color': 'orange'})
```

- - -

###starmade.BlockGroup.get_all_blocks(**block_properties)
Gets all the blocks in the current group that match the properties specified.

>**Parameters**

 >- **block_properties** - Named parameters equivalent to `Block` Properties you wish to match.

>**Returns**

 >- `List` of `Blocks`, or an empty list if none are found

**Example**

```
special_blocks = template.get_all_blocks(color="orange", shape=2)
```

- - -

###starmade.BlockGroup.get_block_at(x, y, z)
Gets a `Block` located at the position provided.

>**Parameters**

 >- **x** - `integer` - Block's x coordinate.
 >- **y** - `integer` - Block's y coordinate.
 >- **z** - `integer` - Block's z coordinate.

>**Returns**

 >- `Block` if block exists, else `None`

- - -

###starmade.BlockGroup.connect_blocks(master, slave)
Creates a new connection pair between the master and slave blocks provided.  
**Important:** Starmade stores these connections backwards, where the purple ('V' selection) is the master, and the orange the slave.

>**Parameters**

 >- **master** - `Block` - Block selected with 'C'
 >- **slave** - `Block` - Block selected with 'V' after a master is selected

>**Returns**

 >- `None`

- - -

###starmade.BlockGroup.connect_blocks_at(master_pos, slave_pos)
Connects two `Blocks` by providing their positions. This method is really just a convenience method for deserializing as the connection groups are stored by their positions (blocks have no guid). Refer to `BlockGroup.connect_blocks()` for difference between master and slave.

>**Parameters**

 >- **master_pos** - `Tuple` - (x, y, z)
 >- **slave_pos** - `Tuple` - (x, y, z)

>**Returns**

 >- `None`

- - -


## `Template` Class
###  extends `BlockGroup`

Template deserialized from a `.smtpl` file or generated through code composed of blocks and connections.

### **Methods**

- - -

###starmade.Template()
Creates an empty Template. Generally only used for programmatically generated Templates. Use `Template.fromSMTPL` to load templates instead.

>**Returns**

 >- Empty `Template` 

- - -

###starmade.Template.fromSMTPL(smtpl_file_path)
**@classmethod**
Deserializes a .smtpl file and creates a Template from it. If you want to create an empty template without a .smtpl file use the `Template()` constructor.

>**Parameters**

 >- **smtpl_file_path** - `string` - Path to the .smtpl file

>**Returns**

 >- `Template`

**Example**
```
template = starmade.Template.fromSMTPL('path/to/template.smtpl')
```

- - -

###starmade.Template.save(save_file_path)
Saves this template to a .smtpl file. If the same file path is used for loading and saving this will overwrite the old .smtpl file.

>**Parameters**

 >- **save_file_path** - `string` - File path where this .smtpl should be saved

>**Returns**

 >- `None`

**Example**
```
template = starmade.Template.fromSMTPL('path/to/template.smtpl')
...
template.save('path/to/template(out).smtpl')
```

- - -



## `Blueprint` Class
###  extends `BlockGroup`


unfinished

- - -
