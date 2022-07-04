# Code for structuring NCC data
The target format is jsonlines. Commonly used for other coreference-datasets available. Each data point (document) is organized in an object as follows:

`doc_key`: id of the document
`tokens`: space-separated tokens
`sentences`: lists of tokens for each sentence
`clusters`: list of lists for each entity, consisting of a [start, stop] range. Single-token mentions have the same value for start/stop (e.g. "Det": [12, 12])

The two main parts of the code serve two purposes:
1: `gather_annotations.py`
    - extracts all annotations marked under as finished into a single directory, with the respective .ann and .txt file endings
    - supports arguments for bokmål or nynorsk
        - `--variation nynorsk` where bokmål is default
2: `batch_ann2jsonlines.py`
    - uses the .ann and .txt files to build the jsonlines formatted files
    - supports arguments:
        - `--folder` which defaults to `annotations`. This is the source folder for extracted files.
        - `--verbose` 0, 1 or 2 to indicate the verbosity levels


The converted files are stored in `annotations_jsonlines` or `annotations_conll`. The latter requires the `batch_jsonlines2conll.py` to be run, which is borrowed from the [corefconversion](https://github.com/boberle/corefconversion) library.