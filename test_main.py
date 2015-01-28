import pytest
from starmade import Block, Template, shape, tier

class TestBlock:
  def test_init(self):
    block1 = Block.from_itemname('Grey Standard Armor')
    block2 = Block(5)
    assert block1.name == block2.name
    assert block1.id == block2.id
    block3 = Block(5, posy=3)
    assert block3.posy == 3

  def test_change_color(self):
    block = Block.from_itemname('Grey Standard Armor')
    assert block.color == 'grey'
    block.change_color('blue')
    assert block.color != 'grey'
    assert block.color == 'blue'

  def test_move(self):
    block = Block(5)
    assert block.posx == 0
    block.move_to(3,5,1)
    assert block.posx == 3
    assert block.posy == 5
    assert block.posz == 1

  def test_change_tier(self):
    block = Block(5)
    assert block.tier == 2
    block.change_tier(3)
    assert block.tier == 3
    block.change_tier_word('basic')
    assert block.tier == 1
    block.change_tier_word('ADVANCED')
    assert block.tier == 3

  def test_change_shape(self):
    block = Block(5)
    assert block.shape == shape('block')
    block.change_shape(shape('wedge'))
    assert block.shape == shape('wedge')

  def test_maintain_unchanged(self):
    block = Block(5, posz=3, posx=2, posy=2)
    block.change_color('blue')
    assert block.posx == 2
    assert block.posy == 2
    assert block.posz == 3


class TestTemplate:
  def test_init(self):
    t = Template()
    t.add(Block(5))
    t.add(Block(5, posy=1))
    assert t.num_blocks() == 2

  def test_box_dims(self):
    t = Template()
    t.add(Block(5))
    t.add(Block(5, posy=1))
    t.add(Block(5, posy=2))
    assert t.box_dimensions() == (1,3,1)
    t.add(Block(5, posz=1))
    assert t.box_dimensions() == (1,3,2)
    t2 = Template()
    t2.add(Block(5, posx=-5))
    t2.add(Block(5, posx=-4))
    assert t2.box_dimensions() == (2,1,1)

  def test_block_count(self):
    t = Template()
    t.add(Block(1))
    t.add(Block(2))
    t.add(Block(5))
    block_count = t.count_by_block()
    assert len(block_count.keys()) == 3

  def test_block_query(self):
    t = Template()
    for x in xrange(10):
      t.add(Block(5, posx=x))
      t.add(Block(431, posy=x))
    t.add(Block(432, posx=3,posy=3,posz=3))
    assert t.num_blocks() == 21
    orange_blocks = t.get_all_blocks(color='orange')
    assert len(orange_blocks) == 11
    orange_hulls = t.get_all_blocks(color='orange', shape=shape('block'))
    print [b.shape for b in orange_hulls]
    assert len(orange_hulls) == 10
    orange_wedges = t.get_all_blocks(color='orange', shape=shape('wedge'))
    assert len(orange_wedges) == 1

  def test_block_batch_replace(self):
    t = Template()
    for x in xrange(10):
      t.add(Block(5, posx=x))
      t.add(Block(431, posy=x))
    t.add(Block(432, posx=3,posy=3,posz=3))
    assert t.num_blocks() == 21
    oranges = len(t.get_all_blocks(color='orange'))
    t.replace({'color':'orange'}, {'color': 'blue'})
    blues = t.get_all_blocks(color='blue')
    assert oranges == len(blues)

  def test_empty(self):
    t = Template()
    d = t.box_dimensions()
    b = t.count_by_block()


class TestTemplateLoading:
  def test_small_armors(self):
    t1 = Template.fromSMTPL('data/test-templates/AAAstandardgrey.smtpl')
    assert len(t1.blocks) == 1
    assert t1.blocks[0].id == 5
    t2 = Template.fromSMTPL('data/test-templates/AAAbasicgrey.smtpl')
    assert t2.blocks[0].id == 598
    t3 = Template.fromSMTPL('data/test-templates/AAApossiblesalvage.smtpl')
    assert t3.blocks[0].id == 4