#!/bin/bash
#SBATCH --job-name=narc
#SBATCH --mail-type=FAIL
#SBATCH --account=ec30
#SBATCH --partition=accel    # To use the accelerator nodes
#SBATCH --gpus=a100:1
#SBATCH --time=1:30:00      # Max walltime is 14 days.
#SBATCH --mem-per-cpu=32G
#SBATCH --nodes=1

set -o errexit  # Recommended for easier debugging
source /etc/profile
## Load your modules
module purge
module load PyTorch/1.9.0-fosscuda-2020b
python3 -m venv /fp/homes01/u01/ec-egilron/venvs/trans_nopt --clear
source /fp/homes01/u01/ec-egilron/venvs/trans_nopt/bin/activate
pip install jsonlines
pip install toml
pip install transformers==3.2.0


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