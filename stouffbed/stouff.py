"""
stouffbed.stouff
~~~~~~~~~~~~~~~~
:copyright: (c) 2017 Sander Bollen
:copyright: (c) 2017 Leiden University Medical Center
:license: MIT
"""

from collections import namedtuple
from math import sqrt
from numpy import isnan, nan

BedLine = namedtuple("BedLine", ['chromosome', 'start', 'end', 'value'])


def stouff_score(zvalues):
    """
    Calculate stouffer's score for a given set of input values 
    :param zvalues: list or numpy array of zscores. May contain nans
    :return: stouffer's z-score or nan 
    """
    values = [x for x in zvalues if not isnan(x)]
    if len(values) == 0:
        return nan
    return sum(values)/sqrt(len(values))


def bed_reader(filename):
    """
    Generator for bed files
    :param filename: path to bed file
    :return: generator of BedLine records
    """
    with open(filename) as handle:
        for line in handle:
            yield BedLine(*line.strip().split()[:4])


def check_region_identical(records):
    """
    Check whether BedLine records are identical regions
    :param records: BedLine records
    :return: Boolean
    """
    chrom = set([x.chromosome for x in records])
    start = set([x.start for x in records])
    end = set([x.end for x in records])
    return all([len(x) == 1 for x in [chrom, start, end]])


def horizontal_stouff(readers):
    """
    Create a generator returnin stouffer's z-scores
    across readers
    :param readers: bed readers 
    :return: Generator of BedLine records
    """
    for i, lines in enumerate(zip(*readers)):
        if not check_region_identical(lines):
            raise ValueError("Readers do not have identical regions"
                             " at line {0}".format(i+1))
        values = [float(x.value) for x in lines]
        st = stouff_score(values)
        yield BedLine(lines[0].chromosome, lines[0].start, lines[0].end, st)
