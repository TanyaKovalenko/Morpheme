# Morpheme
This repository contains dictionaries of prefixies and suffixies meanings; python scripts for compiling a new vector model of Russian corps, that is based on morpheme words decomposition

TODO:
1. Make splitting on morphemes requires at least on root
2. How to split "случайный", "кофейный", "филейный", "прощай", "релейный", "зазнайка", "водогрейный", "водогрейня", "попрошайка", "сотейник", "желейный", "поезжай" - "й" - suffix?
3. "гулянье", "кривлянье": "ь" - suffix? We have not found this suffix in dicts
4. Need to find accent dictionary, it affects sometimes on the suffix decision.
For example:
https://drive.google.com/file/d/0B19_r4ZqIbD5ZXU2V3ZTU3psX1U/view
5. Add small Epsilon (Probability of splitting into morphemes)
6. Try Markov model p->r->s->e ...
7. The accuracy of parsing (91%) can be improved by increasing the data
8. Part of the paper with splitting into morphemes algorithm can be a separate article!
9. Parametric model will be better (formula)
10. We can teach word2vec with morphemes, not with words
11. Test the model on more tasks
