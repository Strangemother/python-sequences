from collections import defaultdict


UNUSED = -1


def bool_pr(key, items, true='+'):
    # return ['', true][key in items]
    return str_bool(key in items, true)


def str_bool(val, true='+'):
    return ['', true][val]



def print_table(lines, ml):
    for l in lines:
        if l is None:
            print('')
            continue

        pr(f"  {l[0]:<{ml}} {l[1]:^4} | {l[2]:^4} | {l[3]:^4} | {l[4]:^4} | {l[5]:^4} | {l[6]:^4}")


def pr(*a):
    print(' '.join(a))


class Sequences(object):

    def __init__(self, words=None, data=None, id_func=None):

        if data is None:
            data = {
                'hots': defaultdict(set),
                'mapped': {},
                'table': {},
                'graph': defaultdict(set),
                'id_func': id_func or str,
            }

        self.set_data(data)
        if words is not None:
            self.stack(words)

        self.add = self.insert_keys

    def get_data(self):
        return {
            'hots': self.hots,
            'mapped': self.mapped,
            'table': self.table,
            'graph': self.graph,
            'id_func': self.id_func,
        }

    def set_data(self, *data):
        self.__dict__.update(*data)

    def stack(self, words):
        for w in words:
            self.input_sequence(w)

    def table_insert_keys(self, chars):
        res = None
        for k in chars:
            res = self.insert_keys(k) # _hots, matches, drops
            self.print_insert_table(k, *res)
        return res

    def input_sequence(self, seq):
        """
        Add a sequence for matching
        """
        for index, item in enumerate(seq):
            next_item = seq[index]
            # Stack the _next_ of the walking tree into the set
            # of future siblings
            self.graph[item].add(next_item)

        id_s = self.generate_id(seq) # str(seq) #id(seq)
        # positional keep sequence
        self.mapped[id_s] = seq
        # First var hot-start
        self.hots[seq[0]].add(id_s)

        self.table[id_s] = UNUSED
        # insert_seq(id_s)
        #

    def generate_id(self, item):
        return self.id_func(item)

    def insert_keys(self, *chars):

        new_hots = set()
        matches = set()
        drops = set()

        for c in chars:
            _hots, _matches, _drops = self.insert_key(c)
            new_hots.update(set(_hots))
            matches.update(set(_matches))
            drops.update(set(_drops))

        return tuple(new_hots), tuple(matches), tuple(drops)

    def insert_key(self, char, reset_on_fail=True):
        """

        `reset_on_fail` resets the index of a sequence positon, if the
                        sequence fails the given step char.
                        If False, the sequence position is not reset, allowing
                        the contiuation of a key through misses.
        """
        matches = ()
        _hots = ()
        resets = ()
        target = self.table

        _hots += self.set_next_hots(char)

        for id_s, pos in target.items():
            if pos == -1: continue

            seq = self.get_sequence(id_s)

            try:
                index_match = int(seq[pos] == char)
            except IndexError:
                # The position is past the edge of the given sequence
                # This occurs when a key completes (has matched)
                print('IndexError for', pos, 'on', id_s)
                index_match = int(seq[0] == char)

            if index_match:
                # The given char does match the current sequence position,
                # advance the index (usually by 1) and test for a completion
                # match.
                t_value = target[id_s] + int(index_match)
                len_match = t_value >= len(seq)
                if len_match:
                    # target[id_s] = int(seq[0] == char)
                    t_value = int(seq[0] == char)
                    # A sequence is complete, present a match,
                    matches += (id_s,)

                target[id_s] = t_value
                continue

            if reset_on_fail:
                resets += (id_s, )
                target[id_s] = -1

        return _hots, matches, resets

    def set_next_hots(self, char):
        """Given a char, step the val if it exists in the 'hot start'

        The hots dict, applied the first item of the sequence to each
        mapped key; speeding up initial steps into an open sequence
            {
                "w": {'w', 'win', 'window'}
                "c": {'cape'}
            }
        """
        hot_starts = ()
        hot_keys = self.hots.get(char, None) or ()

        for id_s in hot_keys:
            pos = self.get_position(id_s)
            sequence = self.get_sequence(id_s)
            if pos >= 1:
                # This position is already open but the start char (id_s)
                # matches the given (char). This may occur for dup index words
                # such as "window" or "ddddddd"
                #
                try:
                    is_match = sequence[pos] == char
                    if is_match:
                        # Don't reset to zero because this is already open.
                        # and the key matches the current sequece (an open step.)
                        continue
                except IndexError:
                    # The key does not exist at this position,
                    # thus the given (char), must be the first index.
                    pass

            # Reset to zero - applying the new position as open.
            self.set_position(id_s, 0)
            hot_starts += (id_s, )
        return hot_starts

    def get_sequence(self, id_s):
        """Return the iterable sequence given the ID.
        """
        return self.mapped[id_s]

    def set_position(self, key, value):
        self.table[key] = value

    def get_position(self, id_s):
        return self.table[id_s]

    def print_state_table(self, hots=None, matches=None, drops=None):
        """print a table of the current state, inject hots, matches or drops
        to highlight within the table.

            self.print_state_table('ape',('ww', 'echo','w', ), 'yeswno' )

        """
        hots = hots or ()
        matches = matches or ()
        drops = drops or ()

        return self.print_insert_table(None, hots, matches, drops)

    def print_insert_table(self, char, _hots, matches, drops):
        opens = ()
        lines = ()
        ml = 4
        spacer = None
        header = ('WORD', 'POS', 'NEXT', 'STRT', 'OPEN', 'HIT', 'DROP', )
        lines += ( spacer, header, )
        for tk, v in self.table.items():
            stk = str(tk)
            # if v < 0:
            #     continue
            ml = max(ml, len(stk)+1)
            opens += ( (stk,v,), )
            _next = '' # stk[0]
            if v > -1:
                try:
                    _next = stk[v]# if v > -1 else 0]
                except IndexError:
                    pass

            line = (
                    stk,
                    v if v > -1 else '',
                    _next,
                    bool_pr(stk, _hots, '#'),# 'started'),
                    str_bool(v > -1, '#'),# 'open'),
                    bool_pr(stk, matches, '#'),# 'match'),
                    bool_pr(stk, drops, '#'),# 'dropped'),
                )

            lines += ( line, )

        # print(k, sequences.table, )
        # print(', '.join(_hots), ' | ',
        #     ', '.join(matches), ' | ',
        #     ', '.join(drops))
        print_table(lines, ml)

    def add_to(self, entity, other):
        return entity.table_insert_keys(other)

    def clone(self):
        return self.__class__(data=self.get_data())

    def __iadd__(self, other):
        """Edit the sequences _in place_, mutating the current sequence.
        """
        self.add_to(self, other)
        return self

    def __add__(self, other):
        """Alter a new one (somehow.)
        """
        entity = self.clone()
        self.add_to(entity, other)
        return entity
