#!/usr/bin/env python3

import argparse
import json

from utils.indices import *

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("--index-counts",
                    help="Path to index counts (gzip)",
                    required=True)
parser.add_argument("--control-samples",
                    help="Path to control samples json",
                    required=True)
parser.add_argument("--read-count-positive-control-threshold",
                    help="Fail if positive control if read count is less than or equal (<=) to this threshold",
                    default=0,
                    required=False)
parser.add_argument("--read-count-negative-control-threshold",
                    help="Fail if negative control if read count is greater than (>) to this threshold",
                    default=0,
                    required=False)
parser.add_argument("--json-report-file",
                    help="Write report out to json file (or to stdout if not specified)",
                    required=False)
parser.add_argument("--exit-with-failure-if-any-control-status-failed",
                    help="If any control samples fail, exit with failure",
                    action='store_true',
                    required=False)

args = parser.parse_args()

# load sequenced index counts
indices_sequenced = pandas.read_csv(args.index_counts, names=["count", "index"])

# load control samples
with open(args.control_samples) as f:
    control_samples = json.load(f)

# check control sample thresholds
control_sample_output = {}
for control_sample in control_samples:
    control_sample_index = control_sample["index"]
    control_sample_type = control_sample["type"]
    control_sample_name = control_sample["name"]

    # direct index match, assumes sequenced vs. sample index same length
    read_count = indices_sequenced[indices_sequenced["index"] == control_sample_index]["count"].sum()

    if control_sample_type == "positive":
        if read_count <= int(args.read_count_positive_control_threshold):
            control_sample_status = "fail"
            control_sample_status_reason = f"Positive control read count <= threshold ({read_count} <= {args.read_count_positive_control_threshold})"
        else:
            control_sample_status = "pass"
            control_sample_status_reason = f"Positive control read count > threshold ({read_count} > {args.read_count_positive_control_threshold})"
    elif control_sample_type == "negative":
        if read_count > int(args.read_count_negative_control_threshold):
            control_sample_status = "fail"
            control_sample_status_reason = f"Negative control read count > threshold ({read_count} > {args.read_count_negative_control_threshold})"
        else:
            control_sample_status = "pass"
            control_sample_status_reason = f"Negative control read count <= threshold ({read_count} <= {args.read_count_negative_control_threshold})"
    else:
        raise Exception(f"Unsupported control type = {control_sample_type}")

    control_sample_output[control_sample_name] = {"status": control_sample_status,
                                                  "reason": control_sample_status_reason}

if args.json_report_file:
    with open(args.json_report_file) as f:
        json.dump(control_sample_output, f)
else:
    print(json.dumps(control_sample_output, indent=4))

if args.exit_with_failure_if_any_control_status_failed:
    if all([v["status"] == "pass" for k, v in control_sample_output.items()]):
        # all status==pass
        pass
    else:
        raise Exception("Not all control samples have passed threshold")
