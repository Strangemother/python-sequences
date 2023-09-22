from src.sequences import Sequences
from src.frames import mass_frame, single_frames
import unittest

def hash_val(text:str):
    res = 0
    for ch in text:
        res = ( res*281  ^ ord(ch)*997) & 0xFFFFFFFF
    return res


def run_test(words):
    test_hit_all(words)
    test_window(words)
    test_clone(words)


def test_clone(words):
    s = Sequences(words, id_func=hash_val)
    c = s.clone()

    assert s.id_func == c.id_func


def test_hit_all(words):
    v = 'apextrackstackcapechoappleswwindowwindyyescakedddddf'
    s = Sequences(words)#, id_func=hash_val)
    r = mass_frame(s, v)
    e = (('ddddd', 'ww', 'yes', 'stack', 'cake', 'wind', 'w', 'windy', 'win',
        'window', 'ape', 'apex', 'extra', 'tracks', 'apples', 'cape', 'echo'),
         ('cake', 'wind', 'ddddd', 'yes', 'w', 'windy', 'win', 'window',
            'ape', 'apex', 'extra', 'tracks', 'apples', 'ww', 'stack',
            'cape', 'echo'),
         ('tracks', 'yes', 'ww', 'stack', 'cake', 'wind', 'w', 'windy',
            'win', 'window', 'ape', 'apex', 'extra', 'ddddd', 'apples',
            'cape', 'echo'))
    assertTupleTupleEqual(r, e)


def test_window(words):
    v = 'window'
    e = (('ww', 'ddddd', 'w', 'win', 'wind', 'windy', 'window'),
         ('w', 'window', 'win', 'wind'),
         ('ww', 'ddddd', 'w', 'windy', 'win', 'wind'))
    se = (('ww', 'w', 'wind', 'windy', 'win'), ('w', 'window'), ())

    s = Sequences(words)#, id_func=hash_val)
    r = mass_frame(s, v)
    sr = single_frames(s, v)

    assertTupleTupleEqual(r, e)
    assertTupleTupleEqual(sr, se)
    return r


def assertTupleTupleEqual(tta, ttb):
    for x,y in zip(tta,ttb):
        unittest.TestCase().assertTupleEqual(tuple(sorted(x)),tuple(sorted(y)))
