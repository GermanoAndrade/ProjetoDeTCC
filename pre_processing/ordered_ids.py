import os
from dotenv import dotenv_values
from utils.utils import get_list

env_dict = dotenv_values("../.env")
DATA_PATH = env_dict['DATA_PATH']

proteins= get_list("../"+DATA_PATH+"proteins.txt")
proteins_kernel = get_list("../"+DATA_PATH+"proteins_kernel.txt")

dict_proteins = {}
for i in range(len(proteins)):
    dict_proteins[proteins[i]] = i
    
ids = []
for i in proteins_kernel:
    idx = dict_proteins.get(i, "NotFound")
    if idx != "NotFound":
        ids.append(idx)
    else:
        ids.append(-1)

with open("../"+DATA_PATH+"ids_A_K_matrices.txt", "w", encoding="UTF-8") as f:
    for i in ids:
        f.write(str(i)+"\n")