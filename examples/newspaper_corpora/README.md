# Newspaper corpora example workflows and visuatisation

## Steps

### Preparation
- activate the playground virtual env
- change into this folder: ``cd examples/newspaper_corpora``
- download and unzip the ``ChroniclItaly_3.0_original.zip`` file from: https://zenodo.org/record/4596345#.YPki35MzbvW (this part will be done by *kiara* at some stage too, just not right now)

### Create a table from a folder of csv files

```
kiara run table.import.from_local_folder path=[PATH_TO_YOUR_LOCAL_UNZIPPED]/CI_newspaper_subcorpora/ aliases=newspaper_subcorpora
```

After this, you should see 2 (new) data items when you do a ``kiara data list``: one file without alias, and a table with the alias '*newspaper_subcorpora*'. This is the 'raw' table. Also try the ``kiara data explain newspaper_subcorpora`` command, if you are interested in the metadata that was created.

### Augment the newspaper table with information we extract from the filename

For this, we'll use the ``augment_newspaper_corpora_table.json`` pipeline in this folder:

```
kiara run augment_newspaper_corpora_table.json value_id=newspaper_subcorpora --save --alias table=augmented_newspaper_subcorpora
```

Check the newly created table and its metadata via ``kiara data explain augmented_newspaper_subcorpora``.

### Test any of the query pipelines

This folder contains 3 query pipelines (``query_newspaper_corpora_*.json``), each one aggregating how many publications where published within a date range. Run any of them like:

```
kiara run query_newspaper_corpora_month.json value_id=augmented_newspaper_subcorpora
```
