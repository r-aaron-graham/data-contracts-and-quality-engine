import unittest
from click.testing import CliRunner
from cli import cli, load_contract_class
from contract import SampleContract

class ContractTests(unittest.TestCase):
    def test_presence_change_including_null(self):
        self.assertIn("optional", SampleContract.compare_samples({}, {"optional": None}))

    def test_invalid_class_is_reported_as_parameter_error(self):
        from click import BadParameter
        with self.assertRaises(BadParameter):
            load_contract_class("__name__")

    def test_documented_examples_and_exit_codes(self):
        runner = CliRunner()
        self.assertEqual(runner.invoke(cli, ["validate", "--contract", "SampleContract",
                                            "--file", "examples/valid.json"]).exit_code, 0)
        result = runner.invoke(cli, ["validate", "--contract", "SampleContract",
                                    "--file", "examples/invalid.json"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Validation failed", result.output)
