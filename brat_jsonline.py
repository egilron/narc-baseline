from code.gather_annotations import gather
from code.batch_ann2jsonlines import ann2jsonlines
from code.jsonlines_wl import jsonlines_wl, splits
from code.ncc_to_heads import get_heads

ANN_FOLDER = "data/annotations"
JSONLINES_DOCWISE = "data/jsonlines"
JSONLINES_WL = "data/wl-formatted"
NAME_CORE = "narc" # First part of wl-formatted filenames
variations = {"bokmaal":"/home/egil/gits_wsl/narc-baseline/Norwegian-Coreference-Corpus/finished_bokmaal"}



for variation, source_path in variations.items():
    gather(variation, source_folder = source_path, save_folder = ANN_FOLDER )

ann2jsonlines(ANN_FOLDER, JSONLINES_DOCWISE)

jsonlines_wl(JSONLINES_DOCWISE, JSONLINES_WL, name_core=NAME_CORE) 

splits(JSONLINES_WL, split_splits = (0.8, 0.9), name_core=NAME_CORE) 

get_heads(JSONLINES_WL, NAME_CORE)