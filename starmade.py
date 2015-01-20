import json
from bisect import bisect_left
"""
Starmade.py is a collection of various helpers for manipulating Starmade data
"""

# items-complete.json has the expanded meta data needed for items
# including things like: shape, armor tier, and color
item_data_path = 'data/items-complete.json'
fh = open(item_data_path, 'r')
item_data = json.load(fh)
items = item_data['items']
fh.close()
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
  def __init__(self, item_id):
    # Creates a block from a supported item id
    data_index = id_map[item_id]
    data = items[data_index]
    self.name = data['name']
    self.id = data['id']
    self.color = data['color']
    self.tier = data['tier']
    self.shape = data['shape']
    self.posx = 0
    self.posy = 0
    self.posz = 0

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
    # Searches the prototypes of all blocks for parameters matching those
    # supplied. Does not search any active blocks, this is just the class here
    # Querying actual instances of blocks will be handled in the sections
    # that contain Blocks, like Templates and Blueprints
    def match(item):
      return all( [ (item[k] == v) for k,v in kwargs.iteritems() ] )
    return filter(match , items)
    return None

  @classmethod
  def search_first(cls, **kwargs):
    return cls.search(**kwargs)[0]

  def change_block_data(self, new_block):
    for k,v in new_block.iteritems():
      setattr(self, k, v)

  # @expects(['grey', 'white', 'black', 'purple', 'blue', 'red', 'green', 'orange', 'yellow'])
  def change_color(self, new_color):
    # find appropriate block of the new color provided
    if new_color != self.color:
      new_block = Block.search_first(color=new_color,tier=self.tier,shape=self.shape)
      self.change_block_data(new_block)

  def change_tier_word(self, new_tier):
    # Takes a tier, as a string, and changes the block to match that new tier
    self.change_tier(tier(new_tier))

  def change_tier(self, new_tier):
    # Takes a tier, as an int, and changes the block to match that new tier
    if new_tier != self.tier:
      new_block = Block.search_first(tier=new_tier,color=self.color,shape=self.shape)
      self.change_block_data(new_block)

  def change_shape(self, new_shape):
    if new_shape != self.shape:
      new_block = Block.search_first(shape=new_shape,tier=self.tier,color=self.color)
      self.change_block_data(new_block)

  def change(self, **kwargs):
    # TODO: Modify kwargs after it comes through to include the things its missing
    # so that which isnt included, isn't altered
    self.change_block_data(Block.search_first(**kwargs))

  def move_to(self,nx=0,ny=0,nz=0):
    # Should be used to change a blocks position to a new one
    self.posx = nx
    self.posy = ny
    self.posz = nz

  def move(self, *args):
    # Placeholder for the moment
    # Should be used to move a block in relation to its current position
    self.move_to(*args)

  def info(self):
    print "Item Name: %s" % self.name
    print "Item ID: %s" % self.id
    print "Position: %s, %s, %s" % (self.posx, self.posy, self.posz)
    print "Item Color: %s" % self.color
    print "Item Shape: %s" % self.shape
    print "Armor Tier: %s" % self.tier








class Template:
  """Template deserialized from a .smtpl file or generated through code
  composed of blocks and connections
  """
  def __init__(self):
    # Creates an empty template from a supplied data source
    self.name = None

  @classmethod
  def fromSMTPL(cls, smtpl_filename):
    # Creates a template from a .smtpl file
    return None

  @classmethod
  def fromJSON(cls, json):
    # Creates a template from a correctly formatted json file
    return None




def test():
  b = Block.from_itemname('Grey Standard Armor')
  b.move(2,2,2)
  b.info()
  # print Block.map_id_to_name(312)
  # print [ block['name'] for block in Block.search(color='yellow',shape=2) ]
  b.change_color('blue')
  b.info()
  # print Block.map_name_to_id('AND-Signal')


if __name__ == '__main__':
  test()