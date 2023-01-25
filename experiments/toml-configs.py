# %% [markdown]
# ## Take the basic toml config file, and make iterations

# %%
import toml
import os
# from transformers import AutoModel, BertModel, AutoModelForMaskedLM

run_id = "POC5"

# %%
# Paths from "experiments" folder
source = "/fp/homes01/u01/ec-egilron/narc-baseline/wl-coref-ncc/config.toml"
toml_folder = "/fp/homes01/u01/ec-egilron/narc-baseline/experiments/tomls"
train_path = "/fp/homes01/u01/ec-egilron/narc-baseline/data/wl-formatted_heads/narc_train_head.jsonl"
runpath = "/fp/homes01/u01/ec-egilron/narc-baseline/wl-coref-ncc/run.py"
fox_slurm_base = "/fp/homes01/u01/ec-egilron/narc-baseline/experiments/tomls/fox_base.slurm"

script_path = os.path.join(toml_folder, run_id+".sh")
fox_slurm_path = os.path.join(toml_folder, run_id+"_fox.slurm")



with open(source) as rf:
    base_toml ={'DEFAULT': toml.loads(rf.read())['DEFAULT']}

defaults = base_toml['DEFAULT']
# for key, value in defaults.items():
#     print(key,":\t", value)




# %%

# ## Changes from the default that is shared by all experiments go here

defaults["rough_k"] = 50
defaults["train_data"] = train_path
defaults["test_data"] = train_path.replace("train", "test")
defaults["dev_data"] = train_path.replace("train", "development")
#defaults["dev_data"] = defaults["test_data"]    ########################## WARNING 





defaults["bert_model"] = "/fp/homes01/u01/ec-egilron/transformers/roberta_jan_128_scandinavian"
defaults["device"] = "cuda:0"
defaults["bert_finetune"] = True
defaults["train_epochs"] = 20


out_folder = os.path.join(toml_folder, run_id)
defaults["conll_log_dir"] = os.path.join(out_folder, "conll_logs")
defaults["data_dir"] = out_folder
if not os.path.exists(out_folder):
    os.mkdir(out_folder)
    if not os.path.exists(defaults["conll_log_dir"]):
        os.mkdir(defaults["conll_log_dir"])




# %%
# ## Create lists of what should be iterated over, and write a toml file with each of these experiments in the one file
# alternatives = {"bert_models": ["/fp/homes01/u01/ec-egilron/norbert2", "xlm-roberta-base", "bert-base-multilingual-cased", "/fp/homes01/u01/ec-egilron/nb-bert-base"]}
# alternatives = {"bert_models": ["/fp/homes01/u01/ec-egilron/transformers/nb-bert-base",  "xlm-roberta-base"]}
alternatives = {"bert_model": [  "/fp/homes01/u01/ec-egilron/transformers/221", "xlm-roberta-base", "/fp/homes01/u01/ec-egilron/transformers/roberta_jan_128_scandinavian" , "bert-base-multilingual-cased", "/fp/homes01/u01/ec-egilron/nb-bert-base"]}
exp_names = ["norBERT2", "xlm-r", "roberta-scand", "mbert", "nbBERT"]
exp_ids = []
out_toml = {'DEFAULT': defaults}
for param_name, alts in alternatives.items():
    for idx, alt in zip(exp_names,alts):
        experiment_id = run_id+"-"+idx
        out_toml[experiment_id] = {param_name: alt}
        exp_ids.append(experiment_id)
out_toml_path = os.path.join(toml_folder, run_id+".toml")
with open(out_toml_path, "w") as wf:
    toml.dump(out_toml, wf)

def check_models(m_list):
    from transformers import AutoModel
    for model in m_list:
        print("Checking model:", model)
        if model[0] == "/":
            try:
                m = AutoModel.from_pretrained(model, local_files_only=True).to("cpu")
                print("success load local")
            except (OSError, ValueError) as e:
                print("failure load local", model)
                print(e)
        
        else:
            try:
                m = AutoModel.from_pretrained(model).to("cpu")
                print("success", model)
            except OSError as e:
                print("failure", model)
        # print(e, "\n")

# check_models(alternatives["bert_models"])


# %% [markdown]
# ## Norwegian models
# Got them to run with cloned and local path, and torch=1.6 in stead of 1.4


# %%

# Create scripts adapted to the environment



scriptlines  = ["#!/bin/sh"]
for exp in exp_ids:
    scriptlines.append(f'echo "Starting experiment {exp}" ')
    scriptlines.append(" ".join(["python", runpath, "train", exp, "--config-file", out_toml_path]))




# print(runpath)
# print("\n".join(scriptlines))

fox = True
if fox:
    print(fox_slurm_path )
    with open(fox_slurm_base) as rf:
        base = rf.read()
        with open (fox_slurm_path, "w") as wf:
            out_file = base+"\n"+"\n".join(scriptlines[1:])
            wf.write(out_file) 


with open (script_path, "w") as wf:
    wf.write("\n".join(scriptlines))
print(script_path)




