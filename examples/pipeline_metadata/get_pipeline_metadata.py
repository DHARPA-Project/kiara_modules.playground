from orjson import dumps, OPT_INDENT_2
from dataclasses import dataclass
from logging import getLogger
from typing import Iterable, List, Optional, Tuple

from kiara import Kiara
from kiara.data.values import ValueSchema, ValueSet
from kiara.pipeline.pipeline import Pipeline
from pydantic.main import BaseModel


def get_pipeline_name_from_io_name(io_name: str) -> Optional[str]:
    parts = io_name.split('__')
    if len(parts) > 2:
        return None
    else:
        return parts[1]


def get_pipeline_io(values: ValueSet) -> Iterable[Tuple[str, str]]:
    for v in values:
        name = get_pipeline_name_from_io_name(v)
        if name is not None:
            yield (name, v)


def get_io_info(values: ValueSet) -> str:
    res = '\n'
    for name, full_name in get_pipeline_io(values):
        o = values.get_value_obj(full_name, ensure_metadata=False)
        s = o.value_schema
        r = '*' if s.is_required else '' 
        res += f' {name}{r} [{s.type}] {s.doc}\n'
    return res


@dataclass
class IoMetadata:
    name: str
    schema: ValueSchema


@dataclass
class PipelineViewStructure:
    inputs: List[IoMetadata]
    outputs: List[IoMetadata]


def get_io_meta_list(values: ValueSet) -> Iterable[IoMetadata]:
    for name, full_name in get_pipeline_io(values):
        o = values.get_value_obj(full_name, ensure_metadata=False)
        s = o.value_schema
        yield IoMetadata(name=name, schema=s)


def get_pipeline_view_structure(pipeline: Pipeline) -> PipelineViewStructure:
    return PipelineViewStructure(
        inputs=list(get_io_meta_list(pipeline.inputs)),
        outputs=list(get_io_meta_list(pipeline.outputs))
    )


def orjson_pydantic_helper(obj):
    if isinstance(obj, BaseModel):
        return dict(obj)
    return obj


log = getLogger(__name__)


kiara = Kiara.instance()
pl = kiara.create_pipeline('playground_rk.network_analysis')

# log.info('Inputs:')
# log.info(get_io_info(pl.inputs))

# log.info('Outputs:')
# log.info(get_io_info(pl.outputs))

s = get_pipeline_view_structure(pl)

j = dumps(
    s,
    default=orjson_pydantic_helper,
    option=OPT_INDENT_2
)
log.info(j.decode("utf-8"))
