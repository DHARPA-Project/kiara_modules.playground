import typing

from pandas import Series

from kiara import KiaraModule
from kiara.data.values import ValueSchema, ValueSet
from kiara.exceptions import KiaraProcessingException


class TokenizeModule(KiaraModule):

    def create_input_schema(
        self,
    ) -> typing.Mapping[
        str, typing.Union[ValueSchema, typing.Mapping[str, typing.Any]]
    ]:

        return {
            "table": {
                "type": "table",
                "doc": "The table that contains the column to tokenize.",
            },
            "column_name": {
                "type": "string",
                "doc": "The name of the column that contains the content to tokenize.",
                "default": "content"
            },
            "tokenize_by_word": {
                "type": "boolean",
                "doc": "Whether to tokenize by word (default), or character."
            }
        }

    def create_output_schema(
        self,
    ) -> typing.Mapping[
        str, typing.Union[ValueSchema, typing.Mapping[str, typing.Any]]
    ]:

        return {
            "tokens_array": {
                "type": "array",
                "doc": "The tokenized content, as an array of lists of strings."
            }
        }

    def process(self, inputs: ValueSet, outputs: ValueSet):

        import pyarrow as pa

        table: pa.Table = inputs.get_value_data("table")
        column_name: str = inputs.get_value_data("column_name")
        tokenize_by_word: bool = inputs.get_value_data("tokenize_by_word")

        if column_name not in table.column_names:
            raise KiaraProcessingException(f"Can't tokenize table: input table does not have a column named '{column_name}'.")

        column: pa.Array = table.column(column_name)

        # this is how you can get a Pandas Series from the column
        print("=========================================")
        pandas_series: Series = column.to_pandas()
        print(pandas_series)
        print("=========================================")

        # do your stuff here

        # then convert your result into an Arrow Array again
        # below is just a fake result, but should give you an idea how to do it
        fake_result = [['x', 'y'], ['a', 'b']]
        fake_result_series = Series(fake_result)
        result_array = pa.Array.from_pandas(fake_result_series)

        outputs.set_values(tokens_array=result_array)

