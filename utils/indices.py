import pandas

from pandas.api.types import CategoricalDtype

bases = CategoricalDtype(categories=['A', 'T', 'C', 'G', 'N', '_'])


def split_index(df, index_column_name='index', index_separator='-', target_index_1_length=None,
                target_index_2_length=None):
    split_indices = df[index_column_name].str.split(index_separator, expand=True).add_prefix('I').fillna('_')

    s = pandas.DataFrame(index=df.index)
    if 'I0' in split_indices:
        index_1_bases = split_indices['I0'].str.split('(?!^)(?!$)', expand=True)
        if target_index_1_length is not None:
            index_1_bases = index_1_bases.reindex(columns=range(0, target_index_1_length))
        index_1_bases = index_1_bases.add_prefix('I1_').fillna('_').astype(bases)
        s = s.join(index_1_bases)
    else:
        raise Exception('Missing index 1')

    if 'I1' in split_indices:
        index_2_bases = split_indices['I1'].str.split('(?!^)(?!$)', expand=True)
        if target_index_2_length is not None:
            index_2_bases = index_2_bases.reindex(columns=range(0, target_index_2_length))
        if not index_2_bases.empty:
            index_2_bases = index_2_bases.add_prefix('I2_').fillna('_').astype(bases)
            s = s.join(index_2_bases)
    elif target_index_2_length:
        index_2_bases = pandas.DataFrame(index=df.index, columns=range(0, target_index_2_length))
        if not index_2_bases.empty:
            index_2_bases.add_prefix('I2_').fillna('_').astype(bases)
            s = s.join(index_2_bases)
    else:
        # no index_2
        pass

    return s


def calculate_distance(x, y, dtype='int8'):
    z = pandas.DataFrame(index=x.index, columns=y.index, dtype=dtype)
    for i in y.index:
        z[i] = (
                (y.iloc[i, :] != x.iloc[:, :])
                # do not count unknown bases in distance
                & (y.iloc[i, :] != "_")
                & (x.iloc[:, :] != "_")
        ).sum(axis=1).astype(dtype)

    return z
