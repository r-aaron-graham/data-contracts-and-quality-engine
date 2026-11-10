# Data contracts and quality engine

Validate JSON records against a Pydantic contract and compare field presence
and Python value types between two samples. `SampleContract` is included
for a runnable first example, requiring a positive ID and a nonempty name.

## Run the example

```bash
python -m pip install -r requirements.txt
python cli.py validate --contract SampleContract --file examples/valid.json
python cli.py validate --contract SampleContract --file examples/invalid.json
```

The first command prints `Validation succeeded` and exits with status 0.
The second reports validation errors and exits with a nonzero status.
To compare samples:

```bash
python cli.py drift --contract SampleContract --file1 examples/valid.json --file2 examples/invalid.json
```

Both samples have the same field types, so this comparison reports no drift.
The validation command checks values against the contract. The drift command
checks structure, including the difference between a missing field and a
present null field. Statistical drift is a separate extension.

## Verify

```bash
python -m pytest -q
```

Create additional contracts by subclassing `BaseContract` and assigning a
Pydantic model to `model`.
