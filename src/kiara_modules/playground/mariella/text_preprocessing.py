import typing

from pandas import Series

from kiara import KiaraModule
from kiara.data.values import ValueSchema, ValueSet
from kiara.exceptions import KiaraProcessingException


class PreprocessModule(KiaraModule):

    def create_input_schema(
        self,
    ) -> typing.Mapping[
        str, typing.Union[ValueSchema, typing.Mapping[str, typing.Any]]
    ]:

        return {
            "table": {
                "type": "table",
                "doc": "The table that contains the column to pre-process.",
            },
            "column_name": {
                "type": "string",
                "doc": "The name of the column that contains the content to pre-process.",
                "default": "content"
            },
            "lowercase": {
                "type": "boolean",
                "doc": "Apply lowercasing to the text.",
                "default": False
            },
            "preprocess_method": {
                "type": "integer",
                "doc": "Pre-processing methodology",
                "default": 0
            },
            "remove_short_tokens": {
                "type": "string",
                "doc": "Remove tokens shorter than a certain length"
            }
        }

    def create_output_schema(
        self,
    ) -> typing.Mapping[
        str, typing.Union[ValueSchema, typing.Mapping[str, typing.Any]]
    ]:

        return {
            "preprocessed_array": {
                "type": "array",
                "doc": "The pre-processed content, as an array of lists of strings."
            }
        }

    def process(self, inputs: ValueSet, outputs: ValueSet):

        import pyarrow as pa

        table: pa.Table = inputs.get_value_data("table")
        column_name: str = inputs.get_value_data("column_name")
        lowercase: bool = inputs.get_value_data("lowercase")
        preprocess_method: int = inputs.get_value_data("preprocess_method")
        remove_short_tokens: str = inputs.get_value_data("remove_short_tokens")

        if column_name not in table.column_names:
            raise KiaraProcessingException(f"Can't pre-process table: input table does not have a column named '{column_name}'.")

        column: pa.Array = table.column(column_name)

        pandas_series: Series = column.to_pandas()

        if lowercase == True:
            pandas_series = pandas_series.apply(lambda x: [w.lower() for w in x])

        #0 none, 1 isalnum, 2 isalpha, 3 isdigit
        
        if preprocess_method != 0:
            
            if preprocess_method == 1:
                pandas_series = pandas_series.apply(lambda x: [w for w in x if w.isalnum()])
            elif preprocess_method == 2:
                pandas_series = pandas_series.apply(lambda x: [w for w in x if w.isalpha()])
            elif preprocess_method == 3:
                pandas_series = pandas_series.apply(lambda x: [w for w in x if not w.isdigit()])
        
        
        if remove_short_tokens != 0:
            pandas_series = pandas_series.apply(lambda x: [w for w in x if len(w) > remove_short_tokens])
            
        
        result_array = pa.Array.from_pandas(pandas_series)

        outputs.set_values(preprocessed_array=result_array)

