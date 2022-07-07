r"""
Convert conll format (2012 or U or X) into jsonlines format.

The jsonlines format stores data for
several texts (a corpus).  Each line is a valid json document, as follows:

    {
      "clusters": [],
      "doc_key": "nw:docname",
      "sentences": [["This", "is", "the", "first", "sentence", "."],
                    ["This", "is", "the", "second", "."]],
      "speakers":  [["spk1", "spk1", "spk1", "spk1", "spk1", "spk1"],
                    ["spk2", "spk2", "spk2", "spk2", "spk2"]]
    }

It is used for some coreference resolution systems, such as:

- https://github.com/kentonl/e2e-coref
- https://github.com/kkjawz/coref-ee
- https://github.com/boberle/cofr

To convert from the original CoNLL2012 format into jsonlines format:

python3 conll2jsonlines.py \
  --token-col 3 \
  --speaker-col 9 \
  INPUT_FILE \
  OUTPUT_FILE

To convert from the StanfordNLP format into jsonlines format:

python3 conll2jsonlines.py \
  --skip-singletons \
  --skip-empty-documents \
  --tab \
  --ignore-double-indices 0 \
  --token-col 1 \
  --speaker-col "_" \
  --no-coref \
  INPUT_FILE \
  OUTPUT_FILE

To convert from the Democrat corpus in CoNLL format (with a column for
paragraphs at position 11):

python3 conll2jsonlines.py \
  --tab \
  --ignore-double-indices 0 \
  --token-col 1 \
  --speaker-col "_" \
  --par-col 11 \
  testing/singe.conll \
  testing/singe.jsonlines

Note that you may have to change document keys in the CoNLL files before
running this script if you want to transform them.
"""

import json
import os
import argparse

from conversion.conll_transform import read_file, sentpos2textpos, compute_chains, read_files


def main(
        infpath, outfpath,
        sep=None, token_col=3, speaker_col="_", add_coref=True, par_col=0,
        ignore_double_indices=True,
        skip_empty_documents=True, skip_singletons=False):

    docs = read_files(
        infpath,
        sep=sep,
        ignore_double_indices=ignore_double_indices,
    )

    with open(outfpath, 'w') as fh:

        for doc_key, doc in docs.items():

            print("Doing %s" % doc_key)

            if add_coref:
                try:
                    clusters = compute_chains(doc)
                    clusters = [
                        [ list(mention) for mention in cluster]
                        for cluster in clusters
                    ]
                    for cluster in clusters:
                        sentpos2textpos(cluster, doc)
                    if skip_singletons:
                        clusters = list(filter(lambda c: len(c) > 1, clusters))
                    if skip_empty_documents and not clusters:
                        print("Skipping %s because no cluster" % doc_key)
                        continue
                except:
                    print(f"Skipping ${doc_key} because of an error")
                    continue
            else:
                clusters = []

            tokens = [t for sent in doc for t in sent]

            sentences = [
                [token[token_col] for token in sent] for sent in doc
            ]

            if par_col:
                start = 0
                length = 0
                current = -1
                paragraphs = []
                for sent in doc:
                    length += len(sent)
                    if int(sent[0][par_col]) != current:
                        current = int(sent[0][par_col])
                        paragraphs.append([start, start+length-1])
                        start += length
                        length = 0
            else:
                #paragraphs = [[0, len(tokens)]]
                paragraphs = None

            if speaker_col.isdigit():
                speakers = [
                    [token[int(speaker_col)] for token in sent] for sent in doc
                ]
            else:
                speakers = [
                    [speaker_col for token in sent] for sent in sentences
                ]


            dic = dict(
                doc_key=doc_key,
                clusters=clusters,
                sentences=sentences,
                speakers=speakers,
            )
            if paragraphs is not None:
                dic['paragraphs'] = paragraphs
            fh.write(json.dumps(dic) + "\n")

if __name__ == "__main__":
    if ".git" not in os.listdir(os.path.abspath(os.curdir)):
        raise EnvironmentError("Needs to run from project root")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--folder",
        type=str,
        help="folder containing .conll files"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="output folder of .jsonl files"
    )
    
    _args = parser.parse_args()
    main(infpath=_args.folder, outfpath=_args.output)
