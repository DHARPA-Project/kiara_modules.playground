from kiara import KiaraEntryPointItem, find_pipeline_base_path_for_module

pipelines: KiaraEntryPointItem = (
    find_pipeline_base_path_for_module,
    ["kiara_modules.playground.rk"],
)
