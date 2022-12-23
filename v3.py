from collections import defaultdict
import sys


mapped = {}

g = defaultdict(set)
hots = defaultdict(set)
table = {}
UNUSED = -1


WORDS = ('apples',
    'window',
    'ape',
    'apex',
    'extra',
    'tracks',
    'stack',
    'yes',
    'cape',
    'cake',
    'echo',
    'win',
    # 'horse',
    # 'house',
    'wind',
    'windy',
    'w',
    'ww',
    'd' * 5,)


def main():
    for s in WORDS:
        add(s) # input_sequence
    ask()


def ask():
    while 1:
        try:
            v = input('V:')
        except EOFError:
            sys.exit(0)

        #print(f'Reading: {len(v)}')

        for k in v:
            _hots, matches, drops = step(k) # insert_keys
            print(k, table, )
            print(', '.join(_hots), ' | ',
                ', '.join(matches), ' | ',
                ', '.join(drops))


def input_sequence(seq):
    """
    Add a sequence for matching
    """

    for index, item in enumerate(seq):
        next_item = seq[index]
        # Stack the _next_ of the walking tree into the set
        # of future siblings
        g[item].add(next_item)

    id_s = str(seq) #id(seq)
    # positional keep sequence
    mapped[id_s] = seq
    # First var hot-start
    hots[seq[0]].add(id_s)

    insert_seq(id_s)


def insert_seq(id_s):
    """Inject a sequence id, ready for stepping
    """

    table[id_s] = UNUSED


def insert_keys(*chars):

    new_hots = ()
    matches = ()
    drops = ()

    #print('insert_keys', chars)
    for c in chars:
        _hots, _matches, _drops = insert_key(c)
        new_hots += _hots
        matches += _matches
        drops += _drops

    return new_hots, matches, drops


def insert_key(char, reset_on_fail=True):
    """

    `reset_on_fail` resets the index of a sequence positon, if the
                    sequence fails the given step char.
                    If False, the sequence position is not reset, allowing
                    the contiuation of a key through misses.
    """
    res = ()
    _hots = ()
    resets = ()

    # print('Reading char', char)
    if char in hots:
        _hots += set_next_hots(char)

    # print('Hots', _hots)
    # print(table)

    for id_s, p in table.items():
        # The passed positions.
        #
        # ditched unused for speed (dependent upon the _hot start_.)
        if p == -1: continue

        seq = mapped[id_s]

        try:
            # Check if the given value matches the step position.
            index_match = seq[p] == char
            # print('Index', p, char, seq)
        except IndexError:
            # failed through the _top_; a forced finish.
            print('IndexError for', p, 'on', id_s)

            index_match = int(seq[0] == char)

        if index_match:
            # print('match', seq)
            # Update the table; If a match, the index will update.
            table[id_s] += int(index_match)

            # A sequence match == the position of the stepper.
            len_match = table[id_s] >= len(seq) #+ 1

            if len_match:
                # Append to the matches set.
                res += (id_s,)

                """
                Reset the index position within the table.
                the step index may be the first char of this key, e.g "window"
                Thus we capture the `1` for the next expected char `i`
                or `0` for char `w`. If 0 the value is eventually reset to -1.
                on the next fail.

                # table[id_s] = 0
                # table[id_s] = -1
                """
                table[id_s] = int(seq[0] == char)

            continue

        # If not "avoiding hot-start", this will reset all unchanged keys to 0.
        # With 'hot-start' the integer is left untouched as -1 for unused keys.
        if reset_on_fail:
            # stash to outputs.
            resets += (id_s, )

            """
            Reset the table index to the inactive position, allowing _skips_
            later.

            #int(seq[0] == char)
            """
            table[id_s] = -1

    return _hots, res, resets


def set_next_hots(char):
    """Given a char, step the val if it exists in the 'hot start'"""
    res = ()
    _keys = hots.get(char)
    # print('Reading', char, _keys)
    for id_s in _keys:

        if table[id_s] >= 1:
            # Already in process, so don't reset to zero as this
            # char may be part of the existing key: "apples", "ddddddd"
            try:
                # If the given char == current index position char, then continue.
                # "mystring"[3] == 't'
                if mapped[id_s][table[id_s]] == char:
                    continue
            except IndexError:
                pass

        res += (id_s, )
        """
        The given char exists as a first key - or 'hot start',
        enumerate all keys into the active table, setting the 'current' index
        to 0,
        Thus when tested the current char will by valid, and the index
        position will step to the next wait: `1`
        """
        table[id_s] = 0

    return res

add = input_sequence
step = insert_keys

if __name__ == '__main__':
    main()
