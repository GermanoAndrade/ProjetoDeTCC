from opensearchpy import OpenSearch
import numpy as np
import os
from dotenv import load_dotenv, dotenv_values
from utils.utils import get_list

# get environment variables to use throughout the code
load_dotenv()
env_dict = dotenv_values(".env")
OPENSEARCH_HOST = env_dict['OPENSEARCH_HOST']
DATA_PATH = env_dict['DATA_PATH']


# loading matrices to be stored in the database
A = np.load(DATA_PATH+"A.npy")
B = np.load(DATA_PATH+"B.npy")
G = np.load(DATA_PATH+"G.npy")

# getting list of genes, which represents the columns of G
proteinas = get_list(DATA_PATH+"proteins.txt")
virus = get_list(DATA_PATH+"viruses.txt")
genes = get_list(DATA_PATH+"genes.txt")

# load A ids related to K for comparing later
A_n_B_order_ids = get_list(DATA_PATH+"ids_A_K_matrices.txt", datatype="int")

# initiate opensearch client
client = OpenSearch(
    hosts = [{'host': OPENSEARCH_HOST, 'port': 9200}],
    http_compress = True,
    use_ssl = False,
    verify_certs = False,
)

# function to get a vector of the K matrix to make a vector to insert in the A matrix
def get_a_vector(user_protein_list, client):
    
    # retrieve lines from given protein id
    A_0 = np.zeros(shape=(0, 18505))
    for each_protein in user_protein_list:
        result = client.get(index="k_matrix", id=each_protein)
        A_0 = np.vstack([A_0, np.array(result["_source"]["line"])])
    
    # get the max of each column
    max_cols = np.max(A_0, axis=0)
    max_cols = max_cols.reshape(1, -1)
    
    # binarizing vector to get only 10% bigger
    threshold = np.percentile(max_cols, 90)
    
    # Assign 1 for values above the threshold and 0 for the remaining
    bin_array = np.where(max_cols > threshold, 1, 0)
    # check the order of the proteins in the column of K and in the column of A
    new_array_list = [None] * len(A_n_B_order_ids)
    # fill the new list with the correct order of the columns
    for i, index in enumerate(A_n_B_order_ids):
        if index != -1:
            new_array_list[index] = bin_array[0,i]
            
    # Now we have the vector with the columns corresponding with the columns of A
    bin_array_ordered = list(filter(lambda x: x is not None, new_array_list))
    bin_array_ordered = np.array([bin_array_ordered])
    return bin_array_ordered

# function to get a vector of the K matrix to make a vector to insert in the B matrix
def get_b_vector(user_protein_list, client):
    ##### B matrix
    
    # retrieve lines from given protein id
    B_0 = np.zeros(shape=(0, 18505))
    for each_protein in user_protein_list:
        result = client.get(index="k_matrix", id=each_protein)
        B_0 = np.vstack([B_0, np.array(result["_source"]["line"])])
    
    # get the max of each column
    max_cols = np.max(B_0, axis=0)
    max_cols = max_cols.reshape(1, -1)
    
    # binarizing vector to get only 10% bigger
    threshold = np.percentile(max_cols, 90)
    
    # Assign 1 for values above the threshold and 0 for the remaining
    bin_array = np.where(max_cols > threshold, 1, 0)
    # check the order of the proteins in the column of K and in the column of A
    
    new_array_list = [None] * len(A_n_B_order_ids)
    
    # fill the new list with the correct order of the columns
    for i, index in enumerate(A_n_B_order_ids):
        if index != -1:
            new_array_list[index] = bin_array[0,i]
            
    # Now we have the vector with the columns corresponding with the columns of A
    bin_array_ordered = list(filter(lambda x: x is not None, new_array_list))
    bin_array_ordered = np.array([bin_array_ordered])
    #bin_array_ordered.reshape(1, -1)
    return bin_array_ordered

def get_g_vector(gene_names, gene_expressions):
    # dict with the column index of each gene
    dict_genes = {}
    for i in range(len(genes)):
        dict_genes[genes[i]] = i

    # vector to be added at the end of G
    new_array_g = np.array([[np.nan] * len(genes)])

    # making the correspondence between the genes passed and the genes in the G matrix
    for i in range(len(gene_names)):
        idx = dict_genes.get(gene_names[i], "NotFound")
        if idx != "NotFound":
            new_array_g[0, idx] = gene_expressions[i]
    return new_array_g
