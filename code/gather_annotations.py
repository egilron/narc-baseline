import argparse
import os
import shutil

TXT = ".txt"
ANN = ".ann"


def gather(variation,
    source_folder = "Norwegian-Coreference-Corpus/finished_bokmaal",
    save_folder = "annotations"):
    # if variation == "nynorsk":
    #     source_folder = "annotation_nynorsk"
    #     # temporary fix until the folders for
    #     # finished annotations are unified
    #     finished_annotations += "_NYNORSK"

    # annotations = os.path.join(os.getcwd(), source_folder, finished_annotations)

    new_annotations_folder = os.path.join(os.getcwd(), save_folder)

    if not os.path.exists(new_annotations_folder):
        os.makedirs(new_annotations_folder)
    # else:
    #     print("Checking metadata against current files...")

    def valid_file(file_name: str) -> bool:
        return TXT in file_name or ANN in file_name

    num_files = 0
    for path, _, filenames in os.walk(source_folder):
        num_files += len(filenames)
        for f in filenames:
            if not valid_file(f):
                continue

            f_path = os.path.join(path, f)
            new_path = os.path.join(save_folder, f"{variation}_{f}")
            shutil.copy2(f_path, new_path)
    print(f"Combined {num_files} .ann and .txt files")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--variation",
        type=str,
        default="bokmaal",
        help="bokmaal or nynorsk"
    )

    gather(parser.parse_args())
