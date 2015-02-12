import json
import binascii
import copy
import pkgutil


from bisect import bisect_left
from utils import tuple_add, tuple_sub, plural, bits
from binary import BinaryStream

"""
Starmade.py is a collection of various helpers for manipulating Starmade data
"""

# items-complete.json has the expanded meta data needed for items
# including things like: shape, armor tier, and color
# item_data_path = 'starmadepy/data/items-complete.json'
# fh = open(item_data_path, 'r')
fh = pkgutil.get_data('starmadepy', 'data/items-complete.json')
print type(fh)
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


class Block:

    """Block class, i don't know what to do just yet.
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

    def props(self):
        return ['color', 'tier', 'shape']

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
        or 'yellow'.
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
        # print kwargs
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

                # Need to take the orientation as 4 bits and the active state
                # as 4 bits, concatenate them, and then write that as a UChar
                active_bits = '1000'
                if block.active and not block.door:
                    # Block On
                    active_bits = '0000'
                elif block.active and block.door:
                    # Door Open
                    active_bits = '1001'
                elif not block.active and block.door:
                    # Door Closed
                    active_bits = '0001'
                orientation_bits = format(block.orientation, '#06b')[2:]
                state = int(orientation_bits + active_bits, 2)
                stream.writeUChar(state)
                # stream.writeUChar(block.orientation)

                id_remainder = block.id % 256
                offset = block.id / 256
                offset_bits = '0010' + '{0:04b}'.format(offset)
                stream.writeUChar(int(offset_bits, 2))
                stream.writeUChar(id_remainder)
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
            print 'Save Complete'

    @classmethod
    def fromSMTPL(cls, smtpl_filepath):
        # Creates a template from a .smtpl file
        t = cls()
        t.name = smtpl_filepath
        print 'Deserializing %s' % smtpl_filepath
        with open(smtpl_filepath, 'rb') as ifile:
            stream = BinaryStream(ifile)
            # t.header = stream.readBytes(25)
            t.version = stream.readUChar()
            t.bound_lower = stream.readVec3Int32()
            t.bound_upper = stream.readVec3Int32()
            n_blocks = stream.readInt32()
            print 'Found %s %s' % (n_blocks, plural(n_blocks, 'block'))
            # Template Blocks
            for i in xrange(n_blocks):
                x, y, z = stream.readVec3Int32()
                # Block ID Bytes
                # ex:
                # 0x09 0x92 0x56
                # First Byte is the Orientation
                # Second Byte is the offset, only the last 4 bits (OLD, now
                # know this is the last 2 bits) matters
                # Third Byte is the id remainder
                state_byte = stream.readChar()
                state_bits = bits(state_byte, 8)
                orientation = int(state_bits[0:4], 2)
                active = state_bits[4:]
                active = int(active, 2)
                active = False if active in [8, 1] else True
                offset = stream.readUChar()
                block_id_remainder = stream.readUChar()
                # Apparently after more trial and error, only the last 2 bits
                # are important. This needs a bit more testing though just to
                # make sure.
                # offset = bits(offset, 4)
                offset = bits(offset, 2)
                offset = int(offset, 2)
                offset = offset * 256
                block_id = block_id_remainder + offset
                block = Block(block_id, posx=x, posy=y, posz=z,
                              orientation=orientation, active=active)
                t.add(block)
            n_connection_groups = stream.readInt32()
            print "File says: %s connection groups" % n_connection_groups

            # Template Connections
            for j in xrange(n_connection_groups):
                unknown_filler = stream.readInt16()
                # Coordinates are saved as z,y,x so we need to reverse them
                master_pos = stream.readVec3Int16()[::-1]
                n_connections = stream.readInt32()
                print n_connections
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


if __name__ == '__main__':
    # fdata = pkgutil.get_data('', 'data/items-complete.json')
    pass
