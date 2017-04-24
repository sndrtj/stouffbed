"""
stouffbed.stouff
~~~~~~~~~~~~~~~~
:copyright: (c) 2017 Sander Bollen
:copyright: (c) 2017 Leiden University Medical Center
:license: MIT
"""

from collections import namedtuple
from math import sqrt, ceil
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
    Create a generator returning stouffer's z-scores
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


def get_nearest_at_idx(values, idx, window):
    """
    Get sublist of elements nearest to a certain index
    :param values: list
    :param idx: the index  
    :param window: the margin that constitutes "near"
    :return: sublist
    """
    e_dist = len(values) - idx
    # starting edge; if distance from start less
    # or equal to half the window size
    if idx == 0 or 0 < idx <= window // 2:
        vals = values[:window]
    # ending edge; if distance from end is less
    # or equal to half the window size
    elif e_dist <= window // 2:
        vals = values[-window:]
    else:
        vals = values[idx - (window // 2):idx + int(ceil((window / 2)))]
    return vals


def vertical_stouff(reader, window_size):
    """
    Create a generator returning stouffer's z-scores along a window
    within a reader
    :param reader: Bed reader
    :param window_size: window size
    :return: generator of bedLines
    """
    records = [x for x in reader]  # must hold in memory
    for i, r in enumerate(records):
        near_records = get_nearest_at_idx(records, i, window_size)
        st = stouff_score([float(x.value) for x in near_records])
        yield BedLine(r.chromosome, r.start, r.end, st)


def bed_to_string(bed_record):
    return "{0}\t{1}\t{2}\t{3}".format(
        bed_record.chromosome,
        bed_record.start,
        bed_record.end,
        bed_record.value
    )

