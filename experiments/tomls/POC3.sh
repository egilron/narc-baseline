#!/bin/sh
echo "Starting experiment POC3-nbBERT" 
python /fp/homes01/u01/ec-egilron/narc-baseline/wl-coref-ncc/run.py train POC3-nbBERT --config-file /fp/homes01/u01/ec-egilron/narc-baseline/experiments/tomls/POC3.toml
echo "Starting experiment POC3-xlm-r" 
python /fp/homes01/u01/ec-egilron/narc-baseline/wl-coref-ncc/run.py train POC3-xlm-r --config-file /fp/homes01/u01/ec-egilron/narc-baseline/experiments/tomls/POC3.toml
echo "Starting experiment POC3-roberta-scand" 
python /fp/homes01/u01/ec-egilron/narc-baseline/wl-coref-ncc/run.py train POC3-roberta-scand --config-file /fp/homes01/u01/ec-egilron/narc-baseline/experiments/tomls/POC3.toml