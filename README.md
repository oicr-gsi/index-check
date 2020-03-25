# index-check

Collection of index checking utilities

# Requirements
- Python 3.7+
- virtualenv

# Installation
```
# initialize virtualenv (python 3.7+ is required)
/usr/bin/python3 -m venv venv

# activate virtualenv
source venv/bin/activate

# install dependencies
pip install -r requirements.txt

# run tests
python -m pytest
```

# General usage

## check_controls.py

```
usage: check_controls.py [-h] --index-counts INDEX_COUNTS --control-samples
                         CONTROL_SAMPLES
                         [--read-count-positive-control-threshold READ_COUNT_POSITIVE_CONTROL_THRESHOLD]
                         [--read-count-negative-control-threshold READ_COUNT_NEGATIVE_CONTROL_THRESHOLD]
                         [--json-report-file JSON_REPORT_FILE]
                         [--exit-with-failure-if-any-control-status-failed]

optional arguments:
  -h, --help            show this help message and exit
  --index-counts INDEX_COUNTS
                        Path to index counts (gzip) (default: None)
  --control-samples CONTROL_SAMPLES
                        Path to control samples json (default: None)
  --read-count-positive-control-threshold READ_COUNT_POSITIVE_CONTROL_THRESHOLD
                        Fail if positive control if read count is less than or
                        equal (<=) to this threshold (default: 0)
  --read-count-negative-control-threshold READ_COUNT_NEGATIVE_CONTROL_THRESHOLD
                        Fail if negative control if read count is greater than
                        (>) to this threshold (default: 0)
  --json-report-file JSON_REPORT_FILE
                        Write report out to json file (or to stdout if not
                        specified) (default: None)
  --exit-with-failure-if-any-control-status-failed
                        If any control samples fail, exit with failure
                        (default: False)
```

For example:
```
source venv/bin/activate

python check_controls.py --index-counts /path/to/counts.gz --control-samples /path/to/control_samples.json
```

Where `counts.gz` is a csv file of `count,index`:
```
92221398,AAAAAAAA
88976066,TTTTTTTT
84342713,CCCCCCCC

...
```

And `control_samples.json` is a json file with an array of objects `name, type, index` objects, for example:
```
[
  {
    "name": "TEST0001",
    "type": "negative",
    "index": "ATATATAT"
  },
  {
    "name":"TEST0002",
    "type":"positive",
    "index":"TTTTTTTT"
  }
]
```

Example output:
```
{
    "TEST0001": {
        "status": "pass",
        "reason": "Negative control read count <= threshold (0 <= 0)"
    },
    "TEST0002": {
        "status": "pass",
        "reason": "Positive control read count > threshold (88976066 > 0)"
    }
}
```


# Development

Don't forget to update requirements.txt
```
source venv/bin/activate

pip freeze > requirements.txt
```
