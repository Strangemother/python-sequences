from collections import defaultdict
from inspect import isfunction

from .printing import PrintTableMixin
from .insert import InsertMixin
from .hot import HotMixin

UNUSED = -1

class Sequences(HotMixin, InsertMixin, PrintTableMixin):

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
        keys = ['hots', 'mapped', 'table', 'graph', 'id_func',]
        return {x:getattr(self,x) for x in keys}

    def set_data(self, *data):
        self.__dict__.update(*data)

    def stack(self, words):
        for w in words:
            self.input_sequence(w)

    def input_sequence(self, seq):
        """
        Add a sequence for matching
        """
        for index, item in enumerate(seq):
            next_item = seq[index]
            # Stack the _next_ of the walking tree into the set
            # of future siblings
            self.graph[item].add(next_item)

        table_id = self.generate_id(seq)
        # positional keep sequence
        self.mapped[table_id] = seq
        # First var hot-start
        self.hots[seq[0]].add(table_id)

        self.table[table_id] = UNUSED

    def generate_id(self, item):
        return self.id_func(item)

    def get_sequence(self, table_id):
        """Return the iterable sequence given the ID.
        """
        return self.mapped[table_id]

    def set_position(self, key, value):
        self.table[key] = value

    def get_position(self, table_id):
        return self.table[table_id]

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
