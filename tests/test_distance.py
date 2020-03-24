import pytest

from utils.distance import barcode_distance

testdata = [
    # target, other -> distance  (i.e. sample index vs. sequenced index)
    ('AAAA', 'AAAA', 0),
    ('AAAA', 'AAAT', 1),
    ('AAAA', 'AAAAT', 0),
    # ('AAAAT', 'AAAA', 1),
    ('AAAAT', 'AAAA', 0),
    ('ATCGT', 'TATCG', 5),
    ('TATCG', 'ATCGT', 5),
    ('ATCGT', 'TATCGG', 5),
    # ('TATCGG', 'ATCGT', 6),
    ('TATCGG', 'ATCGT', 5),
    ('ATCGT-AAAAA', 'TATCGG-AAAAA', 5),
    # ('TATCGG-AAAAA', 'ATCGT-AAAAA', 6),
    ('TATCGG-AAAAA', 'ATCGT-AAAAA', 5),
    ('AAAAA-ATCGT', 'AAAAA-TATCGG', 5),
    # ('AAAAA-TATCGG', 'AAAAA-ATCGT', 6),
    ('AAAAA-TATCGG', 'AAAAA-ATCGT', 5),
    ('AAAA', 'AAAA-TTTT', 0),
    # ('AAAA-TTTT', 'AAAA', 4),
    ('AAAA-TTTT', 'AAAA', 0),
    ('AAAA-TTTT', 'AAAA-TTTT', 0),
    ('AAA-TTT', 'AAAA-TTTT', 0),
    # ('AAAA-TTTT', 'AAA-TTT', 2),
    ('AAAA-TTTT', 'AAA-TTT', 0),
    ('AA-TTTT', 'AAAA-TTTT', 0),
    # ('AAAA-TTTT', 'AA-TTTT', 2),
    ('AAAA-TTTT', 'AA-TTTT', 0),
    ('A-TTTT', 'AAAA-TTTT', 0),
    # ('AAAA-TTTT', 'A-TTTT', 3),
    ('AAAA-TTTT', 'A-TTTT', 0),
    ('TTTT', 'AAAA-TTTT', 4),
    # ('AAAA-TTTT', 'TTTT', 8),
    ('AAAA-TTTT', 'TTTT', 4),
    ('AAAT-TTTA', 'AAAA-TTTT', 2),
    ('AAAA-TTTT', 'AAAT-TTTA', 2)
]


@pytest.mark.parametrize("target,other,expected", testdata)
def test_barcode_distance(target, other, expected):
    assert barcode_distance(target, other) == expected


