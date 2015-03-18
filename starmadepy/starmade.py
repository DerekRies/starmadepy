import json
import binascii
import copy
import pkgutil
import os
import tags


from bisect import bisect_left
from utils import tuple_add, tuple_sub, plural, bits, split_every_nchars
from binary import BinaryStream, BitPacker

"""
Starmade.py is a collection of various helpers for manipulating Starmade data
"""

# items-complete.json has the expanded meta data needed for items
# including things like: shape, armor tier, and color
# item_data_path = 'starmadepy/data/items-complete.json'
# fh = open(item_data_path, 'r')
fh = pkgutil.get_data('starmadepy', 'data/items-complete.json')
item_data = json.loads(fh)
items = item_data['items']
# fh.close()
id_map = {}
name_map = {}
SHAPES = item_data['shapes']
ARMOR = item_data['armor_tiers']
for i, item in enumerate(item_data['items']):
    id_map[item['id']] = i
    name_map[item['name']] = i


def shape(s):
    return SHAPES[s.lower()]


def tier(t):
    return ARMOR[t.lower()]


def get_inventory(inv_list):
    """
    Helper function to read the inventory of a storage box or factory
    stored in a meta file for blueprints. (And possibily other files
    later)
    Inventory is stored in 3 separate lists, the first is a list of slot
    ids. The second is a list of block-ids indexed by slot_id. The third
    being the number of blocks of that type.0
    """
    print inv_list
    inventory = []
    for slot_id in inv_list[0]:
        block_id = inv_list[1][slot_id]
        block_count = inv_list[2][slot_id]
        item = {
            'name': Block.map_id_to_name(block_id),
            'id': block_id,
            'count': block_count,
            'slot': slot_id
        }
        inventory.append(item)
    return inventory


def get_filters(filter_list):
    """
    Helper function to read the filters attached to a storage box that
    are stored in a meta file for blueprints. (And possibly other files
    later)
    """
    filters = {}
    for block_count_pair in filter_list:
        block_id = block_count_pair[0]
        block_count = block_count_pair[1]
        block_name = Block.map_id_to_name(block_id)
        filters[block_name] = block_count
    return filters


class Block:

    """Block class serves two roles
        1. to provide an interface for the starmade block database
        2. to represent an actual block in a BlockGroup (template or bp)
    """

    def __init__(
            self,
            item_id,
            posx=0,
            posy=0,
            posz=0,
            orientation=0,
            active=False):
        # Creates a block from a supported item id
        if type(item_id) is not int:
            raise Exception("""Item ID is not an int. If you\'re using a block
                name then use the Block.from_itemname method.""")
        data_index = id_map[item_id]
        data = items[data_index]
        self.name = data['name']
        self.id = data['id']
        self.color = data['color']
        self.tier = data['tier']
        self.shape = data['shape']
        self.posx = posx
        self.posy = posy
        self.posz = posz
        self.orientation = orientation
        # For my purposes I'll be representing both ON and OPEN as a True state
        # OFF and Closed will be represented as a False state
        self.active = active
        self.door = data.get('door', False)
        self.hitpoints = 1

    def props(self):
        return ['color', 'tier', 'shape']

    @classmethod
    def from_stream(cls, stream):
        """
        Preferred method of parsing block data from a file, can be shared
        between templates and blueprints.
        Bit-packed in 3 bytes to represent block data

        - start with last 11 bits for the block id
        - if block has an active state, first 3 bits are orientation
            and 4th bit is active state
        - if block is a corner then first 5 bits are orientation, else 4
        - remainder of bits are block hitpoints value
        """
        total_bits = stream.readNBytesAsBits(3)
        block_id = int(total_bits[-11:], 2)
        block = cls(block_id)
        block.hitpoints = int(total_bits[5:-11], 2)
        if block.shape == shape('corner'):
            # corners require more bits to represent adequately
            block.orientation = int(total_bits[:5], 2)
        else:
            orient_bits = total_bits[:4]
            active_bit = total_bits[4]
            block.active = not bool(int(active_bit))
            block.orientation = int(orient_bits, 2)
            # I'm representing doors the other way around as it makes sense
            # to me.
            # OPEN = ON = 0, CLOSED = OFF = 1
            if block.door:
                block.active = not block.active
        return block

    def serialize_to_stream(self, stream):
        bitpacker = BitPacker()
        if self.shape == shape('corner'):
            bitpacker.pack(self.orientation, 5)
        else:
            bitpacker.pack(self.orientation, 4)
            if self.door:
                bitpacker.pack(self.active, 1)
            else:
                bitpacker.pack(not self.active, 1)
        bitpacker.pack(self.hitpoints, 8)
        bitpacker.pack(self.id, 11)
        bitpacker.write(stream)

    @classmethod
    def from_itemname(cls, name):
        # Creates a block from a item name (string)
        new_block = cls(cls.map_name_to_id(name))
        return new_block

    @classmethod
    def map_name_to_id(cls, name):
        return items[name_map[name]]['id']

    @classmethod
    def map_id_to_name(cls, id):
        return items[id_map[id]]['name']

    @classmethod
    def search(cls, **kwargs):
        """
        Searches the prototypes of all blocks for parameters matching those
        supplied. Does not search any active blocks, this is just the class
        here.

        Querying actual instances of blocks will be handled in BlockGroup
        classes like Templates and Blueprints.
        """
        def match(item):
            return all([(item[k] == v) for k, v in kwargs.iteritems()])
        return filter(match, items)
        return None

    @classmethod
    def search_first(cls, **kwargs):
        return cls.search(**kwargs)[0]

    # Active State Methods
    # Opening and Closing are really just aliases that might throw an
    # exception later if used by Blocks that can't be made invisible
    # by opening them
    def on(self):
        self.active = True

    def open(self):
        self.on()

    def off(self):
        self.active = False

    def close(self):
        self.off()

    def toggle(self):
        self.active = not self.active

    def copy(self, n_copies=1):
        return copy.deepcopy(self)

    def change_block_data(self, new_block):
        for k, v in new_block.iteritems():
            setattr(self, k, v)

    def change_color(self, new_color):
        """
        Expects a string of equal to:
        'grey', 'white', 'black', 'purple', 'blue', 'red', 'green', 'orange',
        'yellow', 'yellow hazard', or 'green hazard'.
        """
        # find appropriate block of the new color provided
        if new_color != self.color:
            new_block = Block.search_first(
                color=new_color, tier=self.tier, shape=self.shape)
            self.change_block_data(new_block)

    def change_tier_word(self, new_tier):
        # Takes a tier, as a string, and changes the block to match that new
        # tier
        self.change_tier(tier(new_tier))

    def change_tier(self, new_tier):
        # Takes a tier, as an int, and changes the block to match that new tier
        if new_tier != self.tier:
            new_block = Block.search_first(
                tier=new_tier, color=self.color, shape=self.shape)
            self.change_block_data(new_block)

    def change_shape(self, new_shape):
        if new_shape != self.shape:
            new_block = Block.search_first(
                shape=new_shape, tier=self.tier, color=self.color)
            self.change_block_data(new_block)

    def change(self, **kwargs):
        # TODO: Needs more tests to make sure this is working properly
        for prop in self.props():
            if prop not in kwargs:
                kwargs[prop] = getattr(self, prop)
        self.change_block_data(Block.search_first(**kwargs))

    def move_to(self, nx=0, ny=0, nz=0):
        # Should be used to change a blocks position to a new one
        self.posx = nx
        self.posy = ny
        self.posz = nz

    def move(self, *args):
        # Placeholder for the moment
        # Should be used to move a block in relation to its current position
        self.move_to(*args)

    def set_position(self, x=0, y=0, z=0):
        self.posx = x
        self.posy = y
        self.posz = z

    def get_position(self):
        return (self.posx, self.posy, self.posz)

    def info(self):
        print "Item Name: %s" % self.name
        print "Item ID: %s" % self.id
        print "Position: %s, %s, %s" % (self.posx, self.posy, self.posz)
        print "Item Color: %s" % self.color
        print "Item Shape: %s" % self.shape
        print "Armor Tier: %s" % self.tier
        print "Door: %s" % self.door


class BlockGroup:

    """Used to share functionality and a common interface between Templates
    and Blueprints
    """

    def __init__(self):
        # Creates an empty block group
        self.name = None
        self.header = None
        self.blocks = []
        # Connections will be tuples with the master first and the slave second
        self.connections = []
        # Header Info
        self.version = 1
        self.bound_lower = None
        self.bound_upper = None

    def empty(self):
        self.blocks = []
        self.connections = []

    def get_connection_groups(self):
        connection_groups = []
        last_master = None
        cur_pos = -1
        for pair in sorted(
                self.connections, key=lambda p: p[1].get_position()):
            master = pair[1]
            slave = pair[0]
            if master != last_master:
                cur_pos += 1
                group = [master, slave]
                connection_groups.append(group)
                last_master = master
            else:
                connection_groups[cur_pos].append(slave)
        return connection_groups

    def num_blocks(self):
        return len(self.blocks)

    def num_connections(self):
        return len(self.connections)

    def box_dimensions(self):
        # Get min values for each axis
        if self.num_blocks() == 0:
            return (0, 0, 0)
        minx = min(block.posx for block in self.blocks)
        miny = min(block.posy for block in self.blocks)
        minz = min(block.posz for block in self.blocks)
        mins = (minx, miny, minz)
        # Get max values for each axis
        maxx = max(block.posx for block in self.blocks)
        maxy = max(block.posy for block in self.blocks)
        maxz = max(block.posz for block in self.blocks)
        maxs = (maxx, maxy, maxz)
        dif = tuple_sub(maxs, mins)
        return tuple_add(dif, (1, 1, 1))

    def count_by_block(self):
        b_count = {}
        if self.num_blocks() != 0:
            for block in self.blocks:
                count = b_count.get(block.name, 0) + 1
                b_count[block.name] = count
        return b_count

    def add(self, block):
        self.blocks.append(block)

    def replace(self, source_query, changes):
        """
        Match all blocks belonging to this template that meet
        the source query, and apply the following changes to them.

        ex: Get all the orange blocks, and make them blue
        t = Template()...
        t.replace({color: 'orange'}, {color: 'blue'})

        ex: Get all the orange wedges and turn them into blocks
        t.replace({color: 'orange', shape: 'wedge'}, {shape: 'block'})
        """
        blocks = self.get_all_blocks(**source_query)
        for block in blocks:
            block.change(**changes)

    def get_all_blocks(self, **kwargs):
        """
        Returns all blocks that match the query provided
        TODO: Allow for more complex filters, like ranges, or multiple options
        for specific block properties
        """
        queried_blocks = []
        for block in self.blocks:
            filters = [bool(getattr(block, key) == val)
                       for key, val in kwargs.iteritems()]
            if all(filters):
                queried_blocks.append(block)
        return queried_blocks

    def get_block_at(self, x, y, z):
        pos_args = {'posx': x, 'posy': y, 'posz': z}
        blocks = self.get_all_blocks(**pos_args)
        if len(blocks):
            return blocks[0]
        return None

    def connect_blocks(self, master, slave):
        """
        Creates a connection pair in the template between two blocks, a master
        and a slave. These are actual Block instances.
        """
        self.connections.append((master, slave))

    def connect_blocks_at(self, master_pos, slave_pos):
        """
        Creates a connection pair in the template between two blocks that are
        specified by their coordinates. master_pos and slave_pos should be a
        tuple like (x,y,z)
        """
        master = self.get_block_at(*master_pos)
        slave = self.get_block_at(*slave_pos)
        self.connect_blocks(master, slave)
        self._print_connection(master_pos, slave_pos)

    def _print_connection(self, pos_a, pos_b):
        print str(pos_a) + ' --> ' + str(pos_b)

    def _print_connections(self):
        """Debugging method to make seeing the connections between blocks
        visual and easy
        """
        for pair in self.connections:
            if pair[0] is None:
                bpos = str(pair[1].get_position())
                print "None --> %s (%s)" % (pair[1].name, bpos)
            elif pair[1] is None:
                apos = str(pair[0].get_position())
                print "%s (%s) --> None" % (pair[0].name, apos)
            else:
                apos = str(pair[0].get_position())
                bpos = str(pair[1].get_position())
                print "%s (%s) --> %s (%s)" % (
                    pair[0].name, apos, pair[1].name, bpos)

    def _print_block_states(self):
        """Debugging method to make seeing which blocks are currently active
        or open, easier"""
        for block in self.blocks:
            print '{0}: {1}'.format(block.name, block.active)

    def _print_block_orientations(self):
        for block in self.blocks:
            print '{0} ({1}): {2}'.format(
                block.name, str(block.get_position()), block.orientation)


class Template(BlockGroup):

    """Template deserialized from a .smtpl file or generated through code
    composed of blocks and connections.
    """

    def save(self, filepath):
        with open(filepath, 'wb') as ofile:
            stream = BinaryStream(ofile)
            stream.writeUChar(self.version)

            if self.bound_lower is None or self.bound_upper is None:
                # create the bounds
                self.bound_lower = (0, 0, 0)
                self.bound_upper = self.box_dimensions()
            stream.writeVec3Int32(self.bound_lower)
            stream.writeVec3Int32(self.bound_upper)

            stream.writeInt32(self.num_blocks())
            for block in self.blocks:
                stream.writeVec3Int32(block.get_position())
                block.serialize_to_stream(stream)
            # stream.writeInt32(0)
            # Writing the Connections portion of the file
            # Connections not supported yet so just writing 4 blank bytes
            connection_groups = self.get_connection_groups()
            stream.writeInt32(len(connection_groups))
            for group in connection_groups:
                master = group[0]
                slaves = group[1:]
                stream.writeInt16(0)
                # Need to save coordinates backwards
                stream.writeVec3Int16(master.get_position()[::-1])
                stream.writeInt32(len(slaves))
                for slave in slaves:
                    stream.writeInt16(0)
                    stream.writeVec3Int16(slave.get_position()[::-1])

    @classmethod
    def fromSMTPL(cls, smtpl_filepath, debug=False):
        # Creates a template from a .smtpl file
        t = cls()
        t.name = smtpl_filepath
        with open(smtpl_filepath, 'rb') as ifile:
            stream = BinaryStream(ifile)
            # t.header = stream.readBytes(25)
            t.version = stream.readUChar()
            t.bound_lower = stream.readVec3Int32()
            t.bound_upper = stream.readVec3Int32()
            n_blocks = stream.readInt32()
            # Template Blocks
            for i in xrange(n_blocks):
                x, y, z = stream.readVec3Int32()
                block = Block.from_stream(stream)
                block.move_to(x, y, z)
                t.add(block)
            n_connection_groups = stream.readInt32()

            # Template Connections
            for j in xrange(n_connection_groups):
                unknown_filler = stream.readInt16()
                # Coordinates are saved as z,y,x so we need to reverse them
                master_pos = stream.readVec3Int16()[::-1]
                n_connections = stream.readInt32()
                for x in xrange(n_connections):
                    unknown_filler3 = stream.readInt16()
                    # Saved backwards again
                    slave_pos = stream.readVec3Int16()[::-1]
                    t.connect_blocks_at(slave_pos, master_pos)
        return t

    @classmethod
    def fromJSON(cls, json_filepath):
        # Creates a template from a correctly formatted json file
        return None


class Blueprint(BlockGroup):

    """
    Blueprint deserialized from a .sment file, blueprint folder, or generated
    through code.
    """

    def __init__(self):
        self.info = None
        self.logic = None
        self.meta = None

    @classmethod
    def read_header(cls, header_file_path, block_names=False):
        """
        Reads a header.smbph file and returns a dictionary of useful info about
        the blueprint.
        Entity Type: Indicates whether the blueprint is for a Ship, Shop, Space
        Station, Asteroid or Planet.
        Bouding Box: A pair of three-dimensional coordinates providing the min
        and max block coords for the blueprint relative to the BP origin(0,0,0)
        Element Map: An array of structures describing the number and types of
        each block in the blueprint.
        """
        header_info = {}
        with open(header_file_path, 'rb') as ifile:
            stream = BinaryStream(ifile)
            header_info['version'] = stream.readInt32()
            header_info['entityType'] = stream.readUInt32()
            header_info['bounds'] = {
                'min': stream.readVec3F(),
                'max': stream.readVec3F()
            }
            num_elements = stream.readInt32()
            elements = []
            for i in xrange(num_elements):
                element = {
                    'block': stream.readInt16(),
                    'count': stream.readInt32()
                }
                if block_names:
                    element['block'] = Block.map_id_to_name(element['block'])
                elements.append(element)
            header_info['body'] = {
                'numElements': num_elements,
                'elements': elements
            }
        return header_info

    @classmethod
    def read_meta(cls, meta_file_path):
        with open(meta_file_path, 'rb') as ifile:
            stream = BinaryStream(ifile)
            version = stream.readUInt32()
            docked_entries = []
            # tagtype = None
            tagtype = stream.readUChar()
            tagroot = None
            if tagtype == 3:
                dock_count = stream.readInt32()
                for i in xrange(dock_count):
                    name = stream.readString()
                    dock_pos = stream.readVec3Int32()
                    dock_size = stream.readVec3F()
                    dock_style = stream.readUInt16()
                    dock_orientation = stream.readUChar()
                    docked_entries.append({
                        'name': name,
                        'dockPos': dock_pos,
                        'dockSize': dock_size,
                        'dockStyle': dock_style,
                        'dockOrientation': dock_orientation,
                        })
                byte_b = stream.readByte()
                gzip = stream.readInt16()

                tagparser = tags.TagParser(stream)
                tagroot = tagparser.read()
                # format the tagroot into a nice data structure
                container = {}
                tag_container = tagroot[0].get('value')
                # print tag_container
                tag_map = {
                    'pw': 'power',
                    'sh': 'shield',
                }
                for item in tag_container:
                    if type(item) == dict:
                        name = item['name']
                        if name in tag_map:
                            name = tag_map[name]
                        container[name] = item['value']
                container['storages'] = []
                for inv in container['controllerStructure']:
                    inv = inv.get('value')
                    storage = {}
                    for pair in inv:
                        storage[pair['name']] = pair['value']
                    stash = storage['stash']
                    storage['inventory'] = get_inventory(stash[1].get('value'))
                    storage['filters'] = get_filters(stash[0][1])
                    # Older blueprints will only have 2 items in the
                    # stash portion (ex: [0, [filters]]) while newer
                    # blueprints allow storages to be named and will
                    # have 3 items
                    # ex: [0, [filters], 'name']
                    if len(stash[0]) < 3:
                        storage['name'] = ''
                    else:
                        storage['name'] = stash[0][2]
                    container['storages'].append(storage)
        return {
            'version': version,
            'dockEntries': docked_entries,
            'tagroot': tagroot,
            'container': container,
            }

    @classmethod
    def read_logic(cls, logic_file_path):
        with open(logic_file_path, 'rb') as ifile:
            stream = BinaryStream(ifile)
            version = stream.readInt32()
            num_controllers = stream.readInt32()
            controller_entities = []
            for i in xrange(num_controllers):
                pos = stream.readVec3Int16()
                ngroups = stream.readInt32()
                groups = []
                for j in xrange(ngroups):
                    blockid = stream.readInt16()
                    nblocks = stream.readInt32()
                    block_pos_list = []
                    for h in xrange(nblocks):
                        block_pos_list.append(stream.readVec3Int16())
                    groups.append({
                        'id': blockid,
                        'nblocks': nblocks,
                        'positions': block_pos_list
                        })
                controller_entities.append({
                    'pos': pos,
                    'ngroups': ngroups,
                    'groups': groups
                    })
        return {
            'v': version,
            'size': num_controllers,
            'entities': controller_entities
            }

    @classmethod
    def fromSMENT(cls, sment_filepath):
        pass

    @classmethod
    def fromFolder(cls, folder_path):
        header_file = folder_path + '/header.smbph'
        info = cls.read_header(header_file, True)
        meta_file = folder_path + '/meta.smbpm'
        meta = cls.read_meta(meta_file)
        logic_file = folder_path + '/logic.smbpl'
        logic = cls.read_logic(logic_file)
        # print info
        # print_logic(logic)
        # print meta
        # print folder_path
        blueprint = cls()
        blueprint.info = info
        blueprint.logic = logic
        blueprint.meta = meta
        return blueprint


if __name__ == '__main__':
    # fdata = pkgutil.get_data('', 'data/items-complete.json')
    pass
