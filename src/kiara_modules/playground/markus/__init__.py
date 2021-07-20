# -*- coding: utf-8 -*-
import typing

from kiara import KiaraModule
from kiara.data.values import ValueSchema, ValueSet
from kiara_modules.core.metadata_schemas import FileMetadata
from pyarrow import csv


class CreateGraphFromFileModule(KiaraModule):
    """Load table-like data from a *kiara* file object (not a path!)."""

    _module_type_name = "from_file"

    def create_input_schema(
        self,
    ) -> typing.Mapping[
        str, typing.Union[ValueSchema, typing.Mapping[str, typing.Any]]
    ]:

        inputs = {
            "file": {
                "type": "file",
                "doc": "The file that contains table data.",
                "optional": False,
            }
        }

        if self.get_config_value("allow_column_filter"):

            inputs["columns"] = {
                "type": "array",
                "doc": "If provided, only import the columns that match items in this list.",
                "optional": False,
            }

        return inputs

    def create_output_schema(
        self,
    ) -> typing.Mapping[
        str, typing.Union[ValueSchema, typing.Mapping[str, typing.Any]]
    ]:
        return {"table": {"type": "table", "doc": "the imported table"}}

    def process(self, inputs: ValueSet, outputs: ValueSet) -> None:

        input_file: FileMetadata = inputs.get_value_data("file")
        imported_data = csv.read_csv(input_file.path)

        if self.get_config_value("allow_column_filter"):
            if self.get_config_value("columns"):
                imported_data = imported_data.select(
                    self.get_config_value("only_columns")
                )

        outputs.set_value("table", imported_data)
