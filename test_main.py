import pytest
import os
import pep8
from starmadepy.starmade import Block, Template, Blueprint, shape, tier



""" To run these tests simply run the command 'py.test' from the root directory.
This will run all the tests so it is recommended that if you are running the tests
automatically upon filechanges that you run the command "py.test -m 'not filewrite'".
This will exclude tests that make sure writing of files is working, which will also
cause the tests to be rerun infinitely when using something like 'rerun' to
automatically rerun those tests.
"""

tpl_dir = 'starmadepy/data/test-templates/'
# tpl_dir = 'data/test-templates/'


class TestBlock:
  def test_init(self):
    block1 = Block.from_itemname('Grey Standard Armor')
    block2 = Block(5)
    assert block1.name == block2.name
    assert block1.id == block2.id
    block3 = Block(5, posy=3)
    assert block3.posy == 3

  def test_failed_init(self):
    with pytest.raises(Exception):
        block1 = Block('Something')

  def test_init_active_state(self):
    # Blocks should always start out as off or closed (visible)
    b = Block.from_itemname('Activation Module')
    b2 = Block.from_itemname('Plex Door')
    assert b.active == False
    assert b2.active == False
    b.toggle()
    assert b.active == True
    b.on()
    assert b.active == True
    b.off()
    assert b.active == False

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

  def test_block_pos_query(self):
    t = Template()
    block1 = Block(5)
    block1.move_to(4,7,3)
    block2 = Block(5)
    block2.move_to(3,3,3)
    t.add(block1)
    t.add(block2)
    compare_block = t.get_block_at(3,3,3)
    assert compare_block == block2

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
    assert True


class TestTemplateConnections:
  def test_read_connections(self):
    # TODO: Need to create some template test-cases
    # of varying size and complexity
    # t1 = Template.fromSMTPL(tpl_dir + 'XOR Gate.smtpl')
    # assert t1.num_connections() == 6
    pass

  def test_make_connections(self):
    t = Template()
    t.add(Block(5))
    t.add(Block(5, posy=1))
    t.connect_blocks_at((0,0,0), (0,1,0))
    assert t.num_connections() == 1


class TestTemplateLoading:
  def test_small_armors(self):
    t1 = Template.fromSMTPL(tpl_dir + 'AAAstandardgrey.smtpl')
    assert len(t1.blocks) == 1
    assert t1.blocks[0].id == 5
    t2 = Template.fromSMTPL(tpl_dir + 'AAAbasicgrey.smtpl')
    assert t2.blocks[0].id == 598
    t3 = Template.fromSMTPL(tpl_dir + 'AAApossiblesalvage.smtpl')
    assert t3.blocks[0].id == 4

  def test_logic_blocks(self):
    t1 = Template.fromSMTPL(tpl_dir + 'XOR Gate.smtpl')
    assert t1.num_blocks() == 8

  def test_active_states(self):
    t1 = Template.fromSMTPL(tpl_dir + 'Pulse.smtpl')
    assert t1.get_all_blocks(name="NOT-Signal")[0].active == True
    assert len(t1.get_all_blocks(active=False)) == 3

  @pytest.mark.filewrite
  def test_save_data(self):
    saved_name = tpl_dir + 'connections/pulse test 5 (saved).smtpl'
    t1 = Template.fromSMTPL(tpl_dir + 'connections/pulse test 5.smtpl')
    t1.save(saved_name)
    t2 = Template.fromSMTPL(saved_name)
    t1not = t1.get_all_blocks(name="NOT-Signal")[0]
    t2not = t2.get_all_blocks(name="NOT-Signal")[0]
    os.remove(saved_name)
    # Make sure active states on blocks are being saved correctly
    assert t1not.active == t2not.active
    assert t1.num_blocks() == t2.num_blocks()
    # Make sure connections between blocks are saved
    assert t1.num_connections() == t2.num_connections()

  @pytest.mark.filewrite
  def test_save_orientation_data(self):
    fname = tpl_dir + 'tutorial1.smtpl'
    saved_name = tpl_dir + 'tutorial1-save.smtpl'
    t1 = Template.fromSMTPL(fname)
    t1.save(saved_name)
    t2 = Template.fromSMTPL(saved_name)
    os.remove(saved_name)
    # TODO:
    # Check to make sure all the wedges have the same orientation
    # as the original file
    pass

  @pytest.mark.filewrite
  def test_save_new_data(self):
    saved_name = tpl_dir + 'generate.smtpl'
    t1 = Template()
    b1 = Block.from_itemname('Activation Module')
    b2 = Block(409, posy=1)
    t1.connect_blocks(b1, b2)
    t1.add(b1)
    t1.add(b2)
    t1.save(saved_name)
    t2 = Template.fromSMTPL(saved_name)
    os.remove(saved_name)
    assert t1.num_blocks() == t2.num_blocks()
    assert t1.num_connections() == t2.num_connections()


class TestBlueprint:
    def test_load_header(self):
        bp_file = 'starmadepy/data/test-blueprints/bptest2'
        bp = Blueprint.fromFolder(bp_file)
        assert bp.info['body']['numElements'] == 3

    def test_load_logic(self):
        bp_file = 'starmadepy/data/test-blueprints/bptest4'
        bp = Blueprint.fromFolder(bp_file)
        logic = bp.logic
        assert logic.get('size') == 2
        


@pytest.mark.style
class TestStyle:
    def test_pep8(self):
        pep8style = pep8.StyleGuide()
        result = pep8style.check_files([
            'starmadepy/starmade.py',
            'starmadepy/binary.py',
            'starmadepy/utils.py'])
        assert result.total_errors == 0