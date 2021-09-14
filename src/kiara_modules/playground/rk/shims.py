import typing

from kiara import KiaraModule
from kiara.data import ValueSet
from kiara.data.values import ValueSchema
from kiara.module_config import ModuleTypeConfigSchema
from pydantic import Field


class CreateTableModuleConfig(ModuleTypeConfigSchema):

    allow_column_filter: bool = Field(
        description="Whether to add an input option to filter columns.", default=False
    )


# NOTE: This module disappeared from "kiara_modules.core".
# It is back in the development branch. Once it is released, this
# module can be removed.
class CreateTableFromFileModule(KiaraModule):
    """Load table-like data from a *kiara* file object (not a path!)."""

    _config_cls = CreateTableModuleConfig
    _module_type_name = "table_from_file"

    def create_input_schema(
        self,
    ) -> typing.Mapping[
        str, typing.Union[ValueSchema, typing.Mapping[str, typing.Any]]
    ]:

        inputs = {
            "file": {
                "type": "string",
                "doc": "Path of the file that contains table data.",
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
        return {"table": {"type": "table", "doc": "The imported table."}}

    def process(self, inputs: ValueSet, outputs: ValueSet) -> None:

        from pyarrow import csv

        input_file = inputs.get_value_data("file")
        imported_data = csv.read_csv(input_file)

        if self.get_config_value("allow_column_filter"):
            if self.get_config_value("columns"):
                imported_data = imported_data.select(
                    self.get_config_value("only_columns")
                )

        outputs.set_value("table", imported_data)
