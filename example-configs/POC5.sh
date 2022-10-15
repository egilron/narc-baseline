#!/bin/sh
echo "Starting experiment POC5-norBERT2" 
python /fp/homes01/u01/ec-egilron/narc-baseline/wl-coref-ncc/run.py train POC5-norBERT2 --config-file /fp/homes01/u01/ec-egilron/narc-baseline/experiments/tomls/POC5.toml
echo "Starting experiment POC5-xlm-r" 
python /fp/homes01/u01/ec-egilron/narc-baseline/wl-coref-ncc/run.py train POC5-xlm-r --config-file /fp/homes01/u01/ec-egilron/narc-baseline/experiments/tomls/POC5.toml
echo "Starting experiment POC5-roberta-scand" 
python /fp/homes01/u01/ec-egilron/narc-baseline/wl-coref-ncc/run.py train POC5-roberta-scand --config-file /fp/homes01/u01/ec-egilron/narc-baseline/experiments/tomls/POC5.toml
echo "Starting experiment POC5-mbert" 
python /fp/homes01/u01/ec-egilron/narc-baseline/wl-coref-ncc/run.py train POC5-mbert --config-file /fp/homes01/u01/ec-egilron/narc-baseline/experiments/tomls/POC5.toml
echo "Starting experiment POC5-nbBERT" 
python /fp/homes01/u01/ec-egilron/narc-baseline/wl-coref-ncc/run.py train POC5-nbBERT --config-file /fp/homes01/u01/ec-egilron/narc-baseline/experiments/tomls/POC5.toml