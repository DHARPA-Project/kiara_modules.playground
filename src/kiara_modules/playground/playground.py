# -*- coding: utf-8 -*-
import typing
import networkx as nx

from kiara import KiaraModule
from kiara.data.values import ValueSchema, ValueSet
from kiara.module_config import KiaraModuleConfig
from pydantic import Field
from networkx import Graph


class ExampleModuleConfig(KiaraModuleConfig):

    separator: str = Field(
        description="The seperator between the two strings.", default=" - "
    )


class ExampleModule(KiaraModule):
    """A very simple example module; concatenate two strings.

    The purpose of this module is to show the main elements of a ``KiaraModule``:

    the (optional) configuration
    :    must inherit from ``KiaraModuleConfig``, and the config class must be set as the "_config_cls" attribute
         on the ``KiaraModule`` class. Configuration values can be retrieved via the ``self.get_config_value(key)``
         method

    the inputs description
    :    must return a dictionary, containing the input name(s) as keys, and another dictionary containing type information
         and documentation about the input data as value

    the outputs description
    :    must return a dictionary, containing the output name(s) as keys, and another dictionary containing type information
         and documentation about the output data as value

    the ``process`` method
    :    this is where the actual work gets done. Input data can be accessed via ``inputs.get_value_data(key)``, results
         can be set with the ``outputs.set_value(key, value)`` method

    Examples:

        This example module can be tested on the commandline with one of the relevant ``kiara`` commands:

            kiara module explain-type playground.playground.example
            kiara module explain-instance playground.playground.example
            kiara run playground.playground.example text_1="xxx" text_2="yyy"

        To set a different separator in the config for this module, and use that via the cli, you could do:

            kiara run playground.playground.example --module-config separator="." text_1="xxx" text_2="yyy"

    """

    _config_cls = ExampleModuleConfig
    _module_type_name = "example"

    def create_input_schema(
        self,
    ) -> typing.Mapping[
        str, typing.Union[ValueSchema, typing.Mapping[str, typing.Any]]
    ]:

        inputs = {
            "text_1": {"type": "string", "doc": "The first text."},
            "text_2": {"type": "string", "doc": "The second text."},
        }

        return inputs

    def create_output_schema(
        self,
    ) -> typing.Mapping[
        str, typing.Union[ValueSchema, typing.Mapping[str, typing.Any]]
    ]:

        outputs = {
            "text": {
                "type": "string",
                "doc": "The concatenated text.",
            }
        }
        return outputs

    def process(self, inputs: ValueSet, outputs: ValueSet) -> None:

        separator = self.get_config_value("separator")

        text_1 = inputs.get_value_data("text_1")
        text_2 = inputs.get_value_data("text_2")

        result = text_1 + separator + text_2
        outputs.set_value("text", result)

#Here comes my attempt at building a find largest component module. Maybe need to add config for setting graph type as in CreateGraphFromEdgesTableModule

class FindLargestComponentsModuleConfig(KiaraModuleConfig):

    find_largest_component: bool = Field(
        description="Find the largest component of a graph.", default=True
        )

    number_of_components: bool = Field(
        description="Count the number of components.", default=True
    )

class FindLargestComponentsModule(KiaraModule):

    _config_cls = FindLargestComponentsModuleConfig
    _module_type_name = "find_largest_component"

    def create_input_schema(
        self,
    ) -> typing.Mapping[
        str, typing.Union[ValueSchema, typing.Mapping[str, typing.Any]]
    ]:

        return {
            "graph": {
                "type": "network_graph",
                "doc": "The network graph."
            }
        }

    def create_output_schema(
        self,
    ) -> typing.Mapping[
        str, typing.Union[ValueSchema, typing.Mapping[str, typing.Any]]
    ]:

        result = {}
        if self.get_config_value("find_largest_component"):
            result["largest_component"] = {
                "type": "network_graph",
                "doc": "A sub-graph of the largest component of the graph.",
            }

        if self.get_config_value("number_of_components"):
            result["number_of_components"] = {
                "type": "integer",
                "doc": "The number of components in the graph.",
            }

        return result

    def process(self, inputs: ValueSet, outputs: ValueSet) -> None:

        if self.get_config_value("find_largest_component"):
            input_graph: Graph = inputs.get_value_data("graph")
            undir_graph = nx.to_undirected(input_graph)
            undir_components = nx.connected_components(undir_graph)
            lg_component = max(undir_components, key=len)
            subgraph = input_graph.subgraph(lg_component)

            outputs.set_values(largest_component=subgraph)

        if self.get_config_value("number_of_components"):
            input_graph: Graph = inputs.get_value_data("graph")
            undir_graph = nx.to_undirected(input_graph)
            number_of_components = nx.number_connected_components(undir_graph)

            outputs.set_values(number_of_components=number_of_components)

#hmm.. how do I run this? kiara run playground.playground.find_largest_component
