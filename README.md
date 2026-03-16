# Data Contracts and Quality Engine

This repository provides a framework for defining data contracts and validating data
against them.  Data contracts specify the expected structure and semantics of data
produced by one system and consumed by another.  The framework includes a simple CLI
for validating JSON files against a contract and basic drift detection.

## Features

* Define data contracts using Pydantic models or JSON Schema.
* Validate data files (JSON) against a contract and report errors.
* Detect basic drift by comparing field presence and types between two samples.
* Command‑line interface for validation and drift detection.

## Usage

Install dependencies:

```bash
pip install -r requirements.txt
```

Define your contract by subclassing `BaseContract` in `contract.py`.  Then validate a
JSON file against it:

```bash
python cli.py validate --contract SampleContract --file data.json
```

You can also compare two JSON files for drift:

```bash
python cli.py drift --contract SampleContract --file1 baseline.json --file2 new.json
```

## Extending

The current implementation focuses on structural validation.  You can extend it to
include semantic rules, value ranges, and cross‑field constraints by overriding the
`validate` method on your contract class.