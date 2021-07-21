# Examples

## Command-line

### Import ('onboard') a file

The ``import.local_file`` module can be used to import any file. Internally, it will extract some metadata (file size, hash, original name, ...)
and copy the file into the internal kiara data store, where it should be safe from external (or any, really) modification.

```
kiara run import.local_file path=examples/data/misc/photo_with_gps_metadata_1.jpg aliases=photo1
```

Check whether the file is imported using one of those commands:

```
kiara data list
kiara data explain photo1
```

### Import ('onboard') a csv file as a table

```
kiara run table.import.from_local_file path=examples/data/journals/JournalNodes1902.csv aliases=journal_1902_nodes
```

You should see two now data items when doing ``kiara data list``: one for the file (this one won't have an alias because we didn't give it any), and one for the table itself.

### Run a sql query against the newly imported table:

```
kiara run table.query.sql table=value:journal_1902_nodes query="select * from data where City='Berlin'"
```

We could also save the query result into the *kiara* data store:

```
kiara run table.query.sql table=value:journal_1902_nodes query="select * from data where City='Berlin'" --save --alias query_result=berlin_journals
```

Now check the metadata of the saved result via the ``explain`` command:

```
kiara data explain berlin_journals
```

## Python

To be done
