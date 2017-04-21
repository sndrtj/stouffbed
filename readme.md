Stouff-bed
==========

Calculate Stouffer's zscores given 4-column bed files containing z-scores.

### Horizontal mode

Calculates Stouffer's zscores for every region across several files

### Vertical mode

Calculates Stouffer's zscores across several regions within the same file

## Requirements

* Python 3.4+
* Click 
* Numpy
 
## Installation

`pip install -r requirements.txt && python setup.py install` 

## Usage

```
Usage: stouffbed [OPTIONS] COMMAND [ARGS]...

  Calculate Stouffer's z scores across or within 4-column bed files



  Two sub-commands are currently supported:

    - horizontal: Calculate Stouffer's z-scores across bed files
    - vertical: Calculate Stouffer's z-scores within bed files

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  horizontal  Across bed files
  vertical    Within bed files
```


