# narc-baseline
Baseline models for the Norwegian Anaphora Resolution Corpus

## Convert and prepare the data
Be in the root of this repository  
### Get the data 


Presently, by `git clone https://github.com/ltgoslo/Norwegian-Coreference-Corpus` 


### Get the machinery 

Clone this fork of wl-coref: `git clone https://github.com/egilron/wl-coref-ncc.git`

### Set up virtual environment 
- Not all Python versions work, need to specify which I have been using. See  `wl-coref-ncc/requirements.txt` for original requirements.
- I have been using a HPC environment with modules loading pyTorch 1.9 and on top of that, installed `jsonlines
, toml,  transformers==3.2.0` with pip. See `wl-coref-ncc/tomls/fox_base.slurm`.



### Run the preprocessing 

`preprocess.py`  
Make sure the paths there are correct for you.  

The script gathers the texts and annotations files from Norwegian-Coreference-Corpus, 
The data are converted to jsonlines, one file per documents. This first jsonlines format can be useful also when the data are used in a different pipeline. This code is written or collected by [Tollef Jørgensen](https://github.com/tollefj).  
The data are then converted to the format that wl-coref requires. Head information is inserted with the SpaCy Norwegian parser. This code is written and collected by [Egil Rønningstad](https://github.com/egilron) and is based on, or copy of the preprocessing scripts in [wl-coref](https://github.com/vdobrovolskii/wl-coref).  
The end result is a folder with `_heads` suffix inside the `data` folder.

## Configure and execute training

- The parameters are set in the toml config file, the wl-coref original file is `wl-coref-ncc/config.toml`
- The training is executed through `python wl-coref-ncc/run.py train <experiment within the toml> <toml-file>`
- The scripts `wl-coref-ncc/tomls/toml-configs.ipynb`and `wl-coref-ncc/tomls/toml-configs.py`can be used to create modification of the toml. These files are working tools, and not neccessarily tidy.

### Notes on the configuration
- The experiments require much GPU memory, 24 GB has not been enough usually. `rough_k` can be set to 5, to train on 12 GB resources, just to see that it runs, but the performance suffers significantly
- Some Norwegian transformers-based models would not download with the transformers Automodel, but we got it to load from a local file storage. 
- With our repo-in-repo structure, setting absolute paths can be helpful
- Originally, wl-coref saves the model after each epoch. This we modify in coref_model.py, where save_weights() is called 







