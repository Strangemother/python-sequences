from src.sequence import Sequence, Path
import unittest

def assertTupleTupleEqual(tta, ttb):
    for x,y in zip(tta,ttb):
        unittest.TestCase().assertTupleEqual(tuple(sorted(x)),tuple(sorted(y)))


def assert_sequence(s):
    # print('name', s.name)
    # print('path', s.path)
    # print('---')
    assert s.name == 'window'
    assertTupleTupleEqual(s.path, tuple('window'))


s1 = Sequence('window') # only args
assert_sequence(s1)

s2 = Sequence(path='window') # only kwarg path
assert_sequence(s2)

s3 = Sequence('window', Path('w', 'i', 'n', 'd', 'o', 'w')) # Args
assert_sequence(s3)

s4 = Sequence(name='window', path=('w', 'i', 'n', 'd', 'o', 'w')) # kwrgs
assert_sequence(s4)


s5 = Sequence('w', 'i', 'n', 'd', 'o', 'w', name='window') # Args
assert_sequence(s5)
