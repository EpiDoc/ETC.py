ETC.py
======

Python implementation of the old CHETC.js epigraphic Leiden to EpiDoc converter

# Install

## Via git

Install by cloning the repository and run 

```shell
python setup.py install
```

## Via pip

```shell
pip install chetc
```

# How to use

To use ETC.py, you need to create a converter instance and configure it with a ConverterModel (Currently, only a ConverterReplacementModel for http://manfredclauss.de/gb/index.html is available)

```python
from chetc import Converter
from chetc.configs import Clauss

# We initialize a converter and disable the word tagging and numbering
converter = Converter(replacement_model=Clauss(word_numbering=False))
# We run a single transformation and print it
print(converter.convert("Sittium a[e]d(ilem) [o(ro) v(os)] f(aciatis)"))
```

should print in a single line
```xml
<lb n="1"/>Sittium
<expan><abbr>a<supplied reason="lost">e</supplied>d</abbr><ex>ilem</ex></expan>
<supplied reason="lost"><expan><abbr>o</abbr><ex>ro</ex></expan></supplied>
<supplied reason="lost"><expan><abbr>v</abbr><ex>os</ex></expan></supplied>
<expan><abbr>f</abbr><ex>aciatis</ex></expan>
```

*Warning* : if you were to run another transformation that is not following this line, you should do a `converter.reset()` to reset the line numbering.

Alternatively, you can run a list of strings to convert and this will be done automatically.