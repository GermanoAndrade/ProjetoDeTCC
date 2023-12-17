from opensearchpy import OpenSearch
from opensearchpy.helpers import bulk
import numpy as np
import os
from dotenv import load_dotenv

# get env variables
load_dotenv()
OPENSEARCH_HOST = os.getenv('OPENSEARCH_HOST')
DATA_PATH = os.getenv('DATA_PATH')


# create function to get generic list with values from a given filename
def get_list(filename):
    file = open(DATA_PATH+filename, "r", encoding="UTF-8")
    values = file.read().split("\n")[:-1]
    file.close()
    return values

# loading matrices to be stored in the database
A = np.load(DATA_PATH+"A.npy")
B = np.load(DATA_PATH+"B.npy")
K = np.load(DATA_PATH+"K.npy")

# get corresponding line names from files
drugs = get_list("drugs.txt")
viruses = get_list("viruses.txt")
proteins_kernel = get_list("proteins_kernel.txt")

# Create the Opensearch client with SSL/TLS enabled
client = OpenSearch(
    hosts = [{'host': OPENSEARCH_HOST, 'port': 9200}],
    http_compress = True, # enables gzip compression for request bodies
    use_ssl = False,
    verify_certs = False,
)

# Create mapping with fields for every index in the database
index_mapping = {
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0,
    "index": {
      "codec": "best_compression"
    }
  },
  "mappings": {
    "properties": {
      "id": {
        "type": "keyword",
        "index": True,
        "store": True
      },
      "line" : {
        "type" : "float"
      }
    }
  }
}

# list with indexes to be created
index_names = ["a_matrix", "b_matrix", "k_matrix"]

# creating indexes
for index_name in index_names:
    response = client.indices.create(index_name, body=index_mapping)
    
### START INSERTING

# insert lines of A
batch = []
for Aid in range(A.shape[0]):
    document = {
        'line': A[Aid,:]
    }
    each_val = {"_op_type": "index", 
                "_index": index_names[0], 
                "_id": drugs[Aid], 
                "_source": document}
    batch.append(each_val)
    if len(batch) == 10 :
        success, failed = bulk(client, batch, index=index_names[0], raise_on_error=True)
        batch.clear()
if len(batch) > 0:
    success, failed = bulk(client, batch, index=index_names[0], raise_on_error=True)
    batch.clear()
    
# insert lines of B
batch = []
for Bid in range(B.shape[0]):
    document = {
        'line': B[Bid,:]
    }
    each_val = {"_op_type": "index", 
                "_index": index_names[1], 
                "_id": viruses[Bid], 
                "_source": document}
    batch.append(each_val)
    if len(batch) == 10 :
        success, failed = bulk(client, batch, index=index_names[1], raise_on_error=True)
        batch.clear()
if len(batch) > 0:
    success, failed = bulk(client, batch, index=index_names[1], raise_on_error=True)
    batch.clear()    

# insert lines of K
batch = []
for Kid in range(K.shape[0]):
    document = {
        'line': K[Kid,:]
    }
    each_val = {"_op_type": "index", 
                "_index": index_names[2], 
                "_id": proteins_kernel[Kid], 
                "_source": document}
    batch.append(each_val)
    if len(batch) == 10 :
        success, failed = bulk(client, batch, index=index_names[2], raise_on_error=True)
        batch.clear()
if len(batch) > 0:
    success, failed = bulk(client, batch, index=index_names[2], raise_on_error=True)
    batch.clear()

