

class Scratch:

    def old_insert_key(self, char, reset_on_fail=True):
        """Insert an item to process against all table sequences.
        This will _push_ or _reset_ the sequence matches when validating.

        `reset_on_fail` resets the index of a sequence positon, if the
                        sequence fails the given step char.
                        If False, the sequence position is not reset, allowing
                        the contiuation of a key through misses.

        Return hot, matches, and drops.
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
                table_position = seq[pos]
                index_match = int(table_position == char)
                if isfunction(table_position):
                    index_match = int(table_position(char))
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

    def old_set_next_hots(self, char):
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

        for table_id in hot_keys:
            pos = self.get_position(table_id)
            sequence = self.get_sequence(table_id)
            if pos >= 1:
                # This position is already open but the start char (table_id)
                # matches the given (char). This may occur for dup index words
                # such as "window" or "ddddddd"
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
            self.set_position(table_id, 0)
            hot_starts += (table_id, )

        return hot_starts

    def old_set_next_hots(self, char):
        hot_starts = ()
        hot_keys = self.hots.get(char, None) or ()

        # Iterale all table ids found in the hot start table,
        # where the hot-start key is the given char.
        for table_id in hot_keys:

            # Find the current position of the sequence running index.
            pos = self.get_position(table_id)
            sequence = self.get_sequence(table_id)

            if self._is_gt_1_position_match(sequence, pos, char):
                # If the current char is a match within the sequence (where pos > 1)
                # then is not a hot-start, as the sequence is already running.
                continue

            # Reset to zero - applying the new position as open.
            self.set_position(table_id, 0)
            # an event response to the insert function.
            hot_starts += (table_id, )

        return hot_starts

