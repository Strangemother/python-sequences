

class HotMixin(object):

    def set_next_hots(self, char):
        """Given a char, step the val if it exists in the 'hot start'

        The hots dict, applied the first item of the sequence to each
        mapped key; speeding up initial steps into an open sequence
            {
                "w": {'w', 'win', 'window'}
                "c": {'cape'}
            }
        """
        hot_keys = self.hots.get(char, None) or ()

        hot_starts = ()
        # Iterate all table ids found in the hot start table,
        # where the hot-start key is the given char.
        for table_id in hot_keys:
            if self._apply_hot_position(table_id, char):
                # an event response to the insert function.
                hot_starts += (table_id, )

        return hot_starts

    def _apply_hot_position(self, table_id, char):
        # Find the current position of the sequence running index.
        pos = self.get_position(table_id)
        sequence = self.get_sequence(table_id)
        not_is_match = not self._is_gt_1_position_match(sequence, pos, char)

        if not_is_match:
            # Reset to zero - applying the new position as open.
            self.set_position(table_id, 0)

        # If the current char is a match within the sequence (where pos > 1)
        # then is not a hot-start, as the sequence is already running.
        return not_is_match

    def _is_gt_1_position_match(self, sequence, pos, char):
        """Given a sequence, an expected position within the sequence,
        and a matching `char`, test if the char matches the value at the
        seq[pos]. Only do this if pos is greater than 1.

        return bool - True for a match of the char to the seq[pos]
                      where `pos > 1`, else False.
        """
        if pos >= 1:
            # This position is already open but the start char (table_id)
            # matches the given (char). This may occur for dup index words
            # such as "window" or "ddddddd"
            try:
                # Don't reset to zero because this is already open.
                # and the key matches the current sequece (an open step.)
                return sequence[pos] == char
            except IndexError:
                # The key does not exist at this position,
                # thus the given (char), must be the first index.
                pass
        return False

