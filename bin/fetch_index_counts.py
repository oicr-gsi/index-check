#!/usr/bin/env python3

import argparse
import json
import sys

import pandas

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--input-json",
                    help="Path to input json file",
                    required=False,
                    type=argparse.FileType('r'),
                    default=sys.stdin)
args = parser.parse_args()

input_data = json.load(args.input_json)

indices_sequenced = pandas.read_csv(input_data[0], names=["count", "index"])

index_read_counts = {}
for input_index in input_data[1]:
    read_count = indices_sequenced[indices_sequenced["index"] == input_index]["count"].sum()
    index_read_counts[input_index] = int(read_count)

print(json.dumps(index_read_counts, indent=4))
