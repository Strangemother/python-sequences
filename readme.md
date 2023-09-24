# Sequences

> `Sequences` aims to simplify the _silently complex_ task of finding sequences in streams, such as typed characters or object event detection, without storing cached assets.

Utilizing graph-based step-testing `Sequences` is a Python library developed to identify and match sequences within data streams. It specializes in detecting patterns, overlaps, and recurring elements in various types of data, such as character strings or event sequences. The library is designed to handle real-time sequence detection without the need for stored assets, making it suitable for applications like game 'cheat' input detection and sequence testing.


## Example

In this example, we define the Konami Code sequence and input it into the `Sequences` object. We then simulate button presses and check for sequence matches. The Konami Code is successfully matched when the entire sequence of buttons is pressed.


```py
from src.sequences import Sequences

# Define the Konami Code sequence
KONAMI_CODE = ('up', 'up', 'down', 'down', 'left', 'right', 'left', 'right', 'b', 'a', 'start')
CODE_NAME = 'konami'

# Initialize the Sequences object
sq = Sequences()

# Input the Konami Code sequence into the Sequences object
sq.input_sequence(KONAMI_CODE, CODE_NAME)

# Simulate button presses and check for matches
## Using `table_insert_keys` rather than `insert_keys` for demo printing.
button_sequence = KONAMI_CODE[:-1]  # Simulate pressing all buttons except the last one
hots, matches, drops = sq.table_insert_keys(button_sequence)

# At this point, no complete matches are found
print("Complete", matches)  # Output: Complete ()

# Press the last button in the sequence
hots, matches, drops = sq.table_insert_keys(['start'])

# Now, the Konami Code sequence is successfully matched
print("Complete", matches)  # Output: Complete ('konami',)
```

## Understanding Hots, Matches, and Drops

When using the Sequences library, three key concepts are essential: hots (hot starts), matches, and drops. Here’s a brief overview and a demonstration of each:

+ **Hots**: Represent sequences that have started matching and are actively being tracked.
+ **Matches**: Denote sequences that have been successfully matched.
+ **Drops**: Indicate sequences that were being tracked but have been dropped due to a mismatch.

```py
from src.sequences import Sequences

# Define sequences
SEQUENCE_A = ('a', 'b', 'c')
SEQUENCE_B = ('x', 'y', 'z')

# Initialize the Sequences object
sq = Sequences()

# Input sequences into the Sequences object
sq.input_sequence(SEQUENCE_A, 'Sequence A')
sq.input_sequence(SEQUENCE_B, 'Sequence B')

# Simulate partial input and check the state
hots, matches, drops = sq.table_insert_keys(['a', 'b'])
print("Hots", hots)  # Output: Hots ('Sequence A',)
print("Matches", matches)  # Output: Matches ()
print("Drops", drops)  # Output: Drops ()

# Simulate a mismatch
hots, matches, drops = sq.table_insert_keys(['x'])
print("Hots", hots)  # Output: Hots ('Sequence B',)
print("Matches", matches)  # Output: Matches ()
print("Drops", drops)  # Output: Drops ('Sequence A',)

# Complete the matching for Sequence B
hots, matches, drops = sq.table_insert_keys(['y', 'z'])
print("Hots", hots)  # Output: Hots ()
print("Matches", matches)  # Output: Matches ('Sequence B',)
print("Drops", drops)  # Output: Drops ()
```


## Functional Positions in Sequences

> Apply functions as keys within a sequence. If the _sink_ function return `True`, the sequence will continue matching, If `False` the sequence is dropped.

With `Sequences` you can define a single sequence with functional positions. A functional position in a sequence is a position where a function is expected rather than a specific value. This function will be called with the actual value at that position, and the sequence will continue if the function returns `True`.

```py
from src.sequences import Sequences

def sink(v):
    return True

sequence_with_sink = ('a', sink, 'c') # Will match a => ? => c
sq = Sequences()
sq.input_sequence(sequence_with_sink)

hots, matches, drops = sq.table_insert_keys(['a', 'b', 'c'])

print("Matches", matches)  # Output: Matches ('a?c',)
```


For a more grounded example, here we detect if the second character is a vowel:

```py
from src.sequences import Sequences

# Define a function to check if a character is a vowel
def vowel(v):
    return v in 'aeiou'

# Define a sequence with a functional position and a key "p?t"
sequence_with_function = ('p', vowel, 't')
sequence_key = "p?t"

# Initialize the Sequences object and input the sequence
sq = Sequences()
sq.input_sequence(sequence_with_function, sequence_key)

# Simulate multiple inputs and check for matches
inputs = [
    ['p', 'a', 't'],  # This input matches the sequence
    ['p', 'u', 't'],  # This input also matches the sequence
    ['p', 'e', 't'],  # This input matches as well
]

for input_values in inputs:
    hots, matches, drops = sq.table_insert_keys(input_values)
    print(f"Input: {''.join(input_values)}")
    print("Matches", matches)  # Output: Matches ('p?t',)
    print("-----")
```

In this example we simulate three different inputs: "pat", "put", and "pet". All three inputs match the sequence as they all have a vowel in the middle position.


---

### Matches

In the context of the Sequences class, a "match" refers to a successful identification of a sequence within the provided iterable. When you insert a key (or character) into the sequence, the library checks if this key aligns with any of the predefined sequences. If it does, and the sequence is completed, it's considered a "match". For instance, if you've defined the sequence "win" and you sequentially insert the keys "w", "i", and "n", you'll get a match for the sequence "win".

### Misses (Drops)

The term "drops" in the code seems to be synonymous with what you referred to as "misses". A "miss" or "drop" occurs when a key is inserted that doesn't align with the next expected key in any of the active sequences. This means that the current path being traced doesn't match any of the predefined sequences. When this happens, the sequence's position is reset (if reset_on_fail is set to True), effectively dropping or missing the sequence.

For example, if you've defined the sequence "win" and you insert the keys "w" and "a", the sequence is dropped or missed because "a" doesn't follow "w" in the predefined sequence.

### Hots (Hot Starts)

The concept of "hots" or "hot starts" is a performance optimization in the Sequences class. Instead of checking every possible sequence every time a key is inserted, the library maintains a "hot start" list for sequences that are currently active or have a high likelihood of matching. This list contains the starting characters of all predefined sequences. When a key is inserted that matches one of these starting characters, the sequence is considered "hot" and is actively checked for matches as subsequent keys are inserted.

For instance, if you've defined sequences "win" and "wind", and you insert the key "w", both sequences become "hot" and are actively checked for matches as you continue to insert keys.

## More Example

```py
import src.sequences as sequences

def sink(v):
    # Any value given is acceptable.
    return True


def vowel(v):
    return v in 'aieou'

WORDS = (
    ('w', 'i', 'n', 'd', 'o', 'w',),
    'windy',
    ('q', sink, 'd'),
    ('c', vowel, 't',),
    )


sq = sequences.Sequences(WORDS)
trip = sq.insert_keys(*'window')

```


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

The library can detect overlaps and repeat letters. Therefore when _ending_ a sequence, you can _start_ another. For example the word `window` can also be a potential start of another `w...` sequence - such as the single char `w`.