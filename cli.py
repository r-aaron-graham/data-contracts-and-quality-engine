"""CLI for validating data against contracts and detecting drift."""

from __future__ import annotations

import click
import importlib
import json
from typing import Any, Dict

from contract import BaseContract


def load_contract_class(name: str):
    """Dynamically load a contract class by name from the contract module."""
    module = importlib.import_module("contract")
    cls = getattr(module, name, None)
    if cls is None or not issubclass(cls, BaseContract):
        raise click.BadParameter(
            f"Contract class '{name}' not found or not a subclass of BaseContract"
        )
    return cls


@click.group()
def cli() -> None:
    """Data contract CLI."""
    pass


@cli.command(help="Validate a JSON file against a contract")
@click.option("--contract", "contract_name", required=True, help="Name of the contract class")
@click.option("--file", "file_path", required=True, type=click.Path(exists=True))
def validate(contract_name: str, file_path: str) -> None:
    contract_cls = load_contract_class(contract_name)
    with open(file_path, "r", encoding="utf-8") as f:
        data: Dict[str, Any] = json.load(f)
    try:
        contract_cls.validate_data(data)
        click.echo("Validation succeeded")
    except Exception as exc:  # noqa: BLE001
        click.echo(f"Validation failed: {exc}")


@cli.command(help="Compare two JSON files for drift against a contract")
@click.option("--contract", "contract_name", required=True, help="Name of the contract class")
@click.option("--file1", "file1_path", required=True, type=click.Path(exists=True))
@click.option("--file2", "file2_path", required=True, type=click.Path(exists=True))
def drift(contract_name: str, file1_path: str, file2_path: str) -> None:
    contract_cls = load_contract_class(contract_name)
    with open(file1_path, "r", encoding="utf-8") as f:
        data1: Dict[str, Any] = json.load(f)
    with open(file2_path, "r", encoding="utf-8") as f:
        data2: Dict[str, Any] = json.load(f)
    diffs = contract_cls.compare_samples(data1, data2)
    if not diffs:
        click.echo("No drift detected")
    else:
        click.echo("Drift detected in fields:")
        for field, (v1, v2) in diffs.items():
            click.echo(f"  {field}: {v1} -> {v2}")


if __name__ == "__main__":
    cli()