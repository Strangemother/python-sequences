# Sequences

match a sequence of chars within a larger set, using a table of integers. Each 'word' has a position index to yield matches

For example, consider you have a very long string containing your sequence `fragil` - such as "supercalifragilisticexpialidocious". or other button bashed stream of bits.

Here we build a table of positions for the possible words.

For example we have a list of words and input `window`

    ?: window
    # ... 5 more frames.

    WORD    POS  | NEXT | STRT | OPEN | HIT  | DROP
    apples       |      |      |      |      |
    window   1   |  i   |      |  #   |  #   |
    ape          |      |      |      |      |
    apex         |      |      |      |      |
    extra        |      |      |      |      |
    tracks       |      |      |      |      |
    stack        |      |      |      |      |
    yes          |      |      |      |      |
    cape         |      |      |      |      |
    cake         |      |      |      |      |
    echo         |      |      |      |      |
    win      1   |  i   |  #   |  #   |      |
    wind     1   |  i   |  #   |  #   |      |
    windy    1   |  i   |  #   |  #   |      |
    w        1   |      |  #   |  #   |  #   |
    ww       1   |  w   |  #   |  #   |      |
    ddddd        |      |      |      |      |

The library can detect overlaps and repeat letters. Therefore when _ending_ a sequence, you can _start_ another.

For example the word `window` can also be a potential start of another `w...` sequence - such as the single char `w`.

Therefore we have `window`, and has a range of things _started_  and _matched_

      (
        ('win', 'ww', 'wind', 'w', 'windy'), #started
        ('window', 'w'), # match
        ()
      )

Upon each step of the input sequence (processing bits) we match the table.

---

Although cheap The sequences input machine is versatile:

+ Game 'cheat' input
+ Sequence testing


Input sequences are checked (after applied to the sequence machine) - processing internal steps until success. If a key fails during startup - the associated units react though events from the sequence machine. Essentially graph-based step-testing.

As input sequences may overlap, unique sub-sequences may be captured whilst capturing large sequences: considering the keys for an example game:

    load
    systemlive
    systemliveload
    live
    loadpass
    loadfail
    fail
    pass

A 5 key even stream may activate all:

    start system live load pass

We load those keys, and as the user inputs, the sequence table will detect when a a match occurs.
