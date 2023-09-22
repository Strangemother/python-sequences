from collections import defaultdict


mapped = {}

g = defaultdict(set)
hots = defaultdict(set)

keys = ('apples',
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
    'horse',
    'house',
    'wind',
    'windy',
    'w',
    'ww',
    'd' * 5,)


def main():
    for s in keys:
        add(s)
    ask()


import sys


def ask():
    while 1:
        try:
            v = input('V:')
        except EOFError:
            sys.exit(0)

        print(f'Reading: {len(v)}')
        for k in v:
            matches = step(k)
            print(k, table, ', '.join(matches))


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


table = {}
UNUSED = -1


def insert_seq(id_s):
    """Inject a sequence id, ready for stepping
    """

    table[id_s] = UNUSED


def insert_keys(*chars):
    matches = ()

    for c in chars:
        matches += insert_key(c)
    return matches


def insert_key(char, reset_on_fail=True):
    """

    `reset_on_fail` resets the index of a sequence positon, if the
                    sequence fails the given step char.
                    If False, the sequence position is not reset, allowing
                    the contiuation of a key through misses.
    """
    res = ()

    if char in hots:
        set_next_hots(char)

    print(table)

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
            print('match', seq)
            # Update the table; If a match, the index will update.
            table[id_s] += int(index_match)

            # A sequence match == the position of the stepper.
            len_match = len(seq) == table[id_s] #+ 1

            if len_match:
                res += (id_s,)
                # table[id_s] = 0
                # table[id_s] = -1
                table[id_s] = int(seq[0] == char)

            continue

        # If not "avoiding hot-start", this will reset all unchanged keys to 0.
        # With 'hot-start' the integer is left untouched as -1 for unused keys.
        if reset_on_fail:
            print('Reset',id_s, index_match)
            table[id_s] = -1#int(seq[0] == char)


    return res


def set_next_hots(char):
    """Given a char, step the val if it exists in the 'hot start'
    """
    keys = hots.get(char)
    for id_s in keys:
        if table[id_s] >= 1:
            # Already in process.
            # if int(mapped[id_s][table[id_s]] == char)
            try:
                if mapped[id_s][table[id_s]] == char:
                    continue
            except IndexError:
                pass

        print('hot', id_s)
        table[id_s] = 0
        # table[id_s] = int(mapped[id_s][0] == char)

add = input_sequence
step = insert_keys

if __name__ == '__main__':
    main()
