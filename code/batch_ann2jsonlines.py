import argparse
import json
import os

from code.conversion.ann_transform import convert_coref
from code.utils import make_jsonline


def ann2jsonlines(source_path, parse_path, verbose = 1):
    # source_path = os.path.join(os.getcwd(), source_folder)
    if not os.path.exists(source_path):
        raise FileNotFoundError(
            f"No annotation files found in folder: {source_path}"
        )

    # parse_path = os.path.join(os.getcwd(), source_folder + "_jsonlines")
    if not os.path.exists(parse_path):
        print("Creating folder for parsed files...")
        os.makedirs(parse_path)

    parsed_data = []
    for file in os.listdir(source_path):
        # just use the .ann files and fetch the text
        # during the parsing phase (by id ref)
        if ".txt" in file:
            continue

        file_path = os.path.join(source_path, file)

        if verbose > 0:
            print("Loading ", file_path)

        sentences, tokens, clusters = convert_coref(from_file=file_path)
        doc_key = file.split(".")[0]

        parsed_data.append(make_jsonline(
            doc_key, sentences, tokens, clusters
        ))

    for jsonline in parsed_data:
        jsonline_path = os.path.join(
            parse_path, jsonline["doc_key"] + ".jsonl"
        )
        with open(jsonline_path, "w", encoding="utf-8") as jsonline_file:
            json.dump(jsonline, jsonline_file, ensure_ascii=False)

if __name__ == "__main__":
    if ".git" not in os.listdir(os.path.abspath(os.curdir)):
        raise EnvironmentError("Needs to run from project root")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--folder",
        type=str,
        default="data/annotations",
        help="folder with combined annotations"
    )
    parser.add_argument(
        "--verbose",
        type=int,
        default=1,
        help="level of verbosity. 0: no prints, 1: some prints, 2: all"
    )
    parser.add_argument(
        "--parsepath",
        type=str,
        default="data/jsonlines",
        help="destination folder for jsonlines documents"
    )

    ann2jsonlines(parser.folder, parser.parsepath ,verbose = parser.verbose)
