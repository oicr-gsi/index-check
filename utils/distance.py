import operator

import numpy
import pandas as pd
from pandas import DataFrame, Series


def get_distance(df1: Series, threshold=2, op=operator.lt):
    z = pd.Series(dtype=object, index=df1.index)
    for i, v in df1.iteritems():
        z[i] = numpy.asarray(barcode_distance_dataframe(v, df1[~df1.index.isin([i])], threshold, op).index.tolist())
    return z


def get_distance2(df1: Series, df2: Series, threshold=1, op=operator.lt):
    return df1.apply(lambda target: numpy.asarray(barcode_distance_dataframe(target, df2, threshold, op).index.tolist()))


def barcode_distance_dataframe(target: str, others: Series, threshold: int, op: operator) -> DataFrame:
    barcode_distance_passes_threshold = others.apply(lambda other: op(barcode_distance(target, other), threshold))
    return barcode_distance_passes_threshold.loc[barcode_distance_passes_threshold == True]


def barcode_distance(target: str, other: str, barcode_separator='-') -> int:
    return sum([sum(1 for a, b in zip(*x) if a != b)
                for x in zip(target.split(barcode_separator), other.split(barcode_separator))])
