"""Classes and helpers for defining data contracts and validating data."""

from __future__ import annotations

from typing import Any, Dict, Tuple, Type

from pydantic import BaseModel, ValidationError


class BaseContract:
    """Base class for data contracts.

    Subclasses should define a `model` attribute that is a Pydantic BaseModel.
    """

    model: Type[BaseModel]

    @classmethod
    def validate_data(cls, data: Dict[str, Any]) -> BaseModel:
        """Validate a data record against the contract's model.

        :param data: The data record as a dictionary
        :return: An instance of the model if validation succeeds
        :raises ValidationError: If validation fails
        """
        return cls.model(**data)

    @classmethod
    def compare_samples(cls, data1: Dict[str, Any], data2: Dict[str, Any]) -> Dict[str, Tuple[Any, Any]]:
        """Compare two data samples and return a mapping of fields that differ.

        This simple drift detector flags any fields present in one sample but not the
        other or fields whose types differ.
        """
        diffs: Dict[str, Tuple[Any, Any]] = {}
        keys = set(data1.keys()) | set(data2.keys())
        for key in keys:
            v1 = data1.get(key)
            v2 = data2.get(key)
            if type(v1) != type(v2):  # type: ignore[unreachable]
                diffs[key] = (v1, v2)
        return diffs