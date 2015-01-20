import pytest
from starmade import Block, shape, tier

class TestBlock:
  def test_init(self):
    block1 = Block.from_itemname('Grey Standard Armor')
    block2 = Block(5)
    assert block1.name == block2.name
    assert block1.id == block2.id

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
