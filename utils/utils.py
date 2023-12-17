import os
from dotenv import dotenv_values
import numpy as np

env_dict = dotenv_values(".env")
DATA_PATH = env_dict['DATA_PATH']

def get_list(filename, datatype=""):
    file = open(filename, "r", encoding="UTF-8")
    values = file.read().split("\n")[:-1]
    file.close()
    if datatype == "int":
        for i in range(len(values)):
            values[i] = int(values[i])
    return values

# It computes the cost function.
# nas indicates the missing values
# Here we assume that G has 0 where values are missing.
def objectiveFunction(A, B, G, D, V, P, U, lambda1, lambda2, lambda3, 
                              lambda4, alpha=1, nas=None):
    VU = np.dot(V, U)
    
    if nas is not None:
        VU[nas] = 0
    if alpha == 0:
        U = 0
    return np.sum((A - np.dot(D, P))**2) + np.sum((B - np.dot(V, P))**2) + np.sum(alpha * (G - VU)**2) + np.sum(lambda1 * (D**2)) + np.sum(lambda2 * (V**2)) + np.sum(lambda3 * (P**2)) + np.sum(lambda4 * (U**2))

# It creates a matrix with n rows and m cols with random values ranging from
# min to max.
# Optionally, it sets the column names or row names.
def initializeEmbedding(n, m, minimum, maximum, row_names=None, col_names=None):
    X = np.random.uniform(minimum, maximum, size=(n, m))
    if row_names is not None:
        X = np.column_stack((row_names, X))
    if col_names is not None:
        X = np.vstack((col_names, X))
    return X

# It checks whether the cost function converges to a fix value.
def checkStoppingCondition(value, i, eps, max_it):
    if max_it is not None:
        return i <= max_it
    return value > eps

def gradientDescent(A, B, G, k=15, lambda1=0.1, lambda2=0.1, lambda3=0.1, lambda4=0.1, alpha=1, eps=1e-4, max_it=None, eta=0.001,
                     beta1=0.9, beta2=0.999, epsilon=1e-8, init_value=0.001):
    # Initializing embeddings with random values
    D = initializeEmbedding(A.shape[0], k, 0, init_value)
    V = initializeEmbedding(B.shape[0], k, 0, init_value)
    P = initializeEmbedding(k, A.shape[1], 0, init_value)
    U = initializeEmbedding(k, G.shape[1], -init_value, init_value)

    # Setting missing values to 0
    nas = np.isnan(G)
    G[nas] = 0

    # Number of iterations
    i = 1

    # Vector of cost per iteration
    cost = []

    cost.append(objectiveFunction(A, B, G, D, V, P, U, lambda1, lambda2, lambda3, lambda4, alpha=alpha, nas=nas))

    # Change of cost function between two iterations
    change = 1

    # Setting learning step
    eta = 1e-6

    # Iterations for updating embeddings until convergence criterion is satisfied
    while checkStoppingCondition(change, i, eps, max_it):
        old_D = D.copy()
        old_V = V.copy()
        old_P = P.copy()
        old_U = U.copy()

        # Updating D
        D = D - eta * (-np.dot(A, P.T) + np.dot(np.dot(D, P), P.T) + lambda1 * D)
        # Forcing D to be nonnegative
        D[D < 0] = 0

        VU = np.dot(V, U)
        # Adding mask for ignoring missing values
        if nas is not None:
            VU[nas] = 0

        # Updating V
        V = V - eta * (-np.dot(B, P.T) + np.dot(np.dot(V, P), P.T) - alpha * np.dot(G, U.T) + alpha * np.dot(VU, U.T) + lambda2 * V)
        # Forcing V to be nonnegative
        V[V < 0] = 0

        # Updating P
        P = P - eta * (-np.dot(D.T, A) + np.dot(np.dot(D.T, D), P) - np.dot(V.T, B) + np.dot(np.dot(V.T, V), P) + lambda3 * P)
        # Forcing P to be nonnegative
        P[P < 0] = 0

        # Adding mask for ignoring missing values
        VU = np.dot(V, U)
        if nas is not None:
            VU[nas] = 0

        # Updating U
        U = U - eta * (-alpha * np.dot(V.T, G) + alpha * np.dot(V.T, VU) + lambda4 * U)
        i += 1

        # Updating cost function
        cost.append(objectiveFunction(A, B, G, D, V, P, U, lambda1, lambda2, lambda3, lambda4, alpha=alpha, nas=nas))

        # If cost decreased, try to increase the learning step
        if (cost[-1] < cost[-2]):
            eta = eta*1.2
            change = cost[-2] - cost[-1]
        # Otherwise, reduce the learning step and undo the update of the embeddings
        else:
            eta *= 0.8
            i -= 1
            D = old_D.copy()
            V = old_V.copy()
            P = old_P.copy()
            U = old_U.copy()
            cost.pop()

    scores = np.dot(D, V.T)
    return {"scores": scores, "D": D, "V": V, "P": P, "U": U}

# It learns drug, virus, protein and gene embedding by minimizing the cost
# function with the Adam gradient descent algorithm.
# INPUT:
# - A is a matrix of 0s and 1s indicating which proteins (columns) are perturbed 
# by each drug (rows).
# - B indicates which proteins (columns) are perturbed by each virus (rows).
# - G is a matrix of -1s, 0s and 1s that indicates which genes (columns) are up 
# or down regulated for each virus (row).
# - k is the dimension of the embedding
# - lambda1, lambda2, lamnda3, and lambda4 are parameters for controlling the
# regularization of D, V, P, U, respectively.
# - alpha is a parameter controlling the contribution of the gene expression data
# - eps is used for checking the stopping criterion when max_it is NULL
# - max_it fixes the number of iterations, if it is provided
# - eta, beta1, and beta2 are parameter used by Adam gradient descent algorithm
# - epsilon is small number added for avoiding divisions by 0
# - init_value is a positive number used for defining the range for the initial
# values in the embedding. D, V, and P are initialized with random values from
# a untiform distribution between 0 and init_value. U is initialized with random
# values between -init_value and +init_value.
# OUTPUT
# List containing:
# - scores is a matrix with the final prediction scores
# - D - drug representation in a k-dimension space, with latent features on the
# columns
# - V - virus representation in a k-dimension space, with latent features on the
# columns
# - P - protein representation in a k-dimension space, with latent features on
# the rows
# - U - gene representation in a k-dimension space, with latent features on the
# rows
# - cost is a vector of costs per iteration

def gradientDescentAdam(A, B, G, k=15, lambda1=0.1, lambda2=0.1, lambda3=0.1, lambda4=0.1, alpha=1, eps=1e-4, max_it=None, eta=0.001,
                           beta1=0.9, beta2=0.999, epsilon=1e-8, init_value=0.001):
    # Initializing embeddings with random values
    D = initializeEmbedding(A.shape[0], k, 0, init_value)
    V = initializeEmbedding(B.shape[0], k, 0, init_value)
    P = initializeEmbedding(k, A.shape[1], 0, init_value)
    U = initializeEmbedding(k, G.shape[1], -init_value, init_value)

    # Setting missing values to 0
    nas = np.isnan(G)
    G[nas] = 0

    # Number of iterations
    i = 1

    # Vector of cost per iteration
    cost = []

    cost.append(objectiveFunction(A, B, G, D, V, P, U, lambda1, lambda2, lambda3, lambda4, alpha=alpha, nas=nas))

    # Change of cost function between two iterations
    change = 1

    # Variables used for Adam optimization
    mD = mV = mP = mU = 0
    vD = vV = vP = vU = 0

    # Iterations for updating embeddings until convergence criterion is satisfied
    while checkStoppingCondition(change, i, eps, max_it):
        # Derivative for updating D
        gradD = -np.dot(A, P.T) + np.dot(np.dot(D, P), P.T) + lambda1 * D
        mD = beta1 * mD + (1 - beta1) * gradD
        vD = beta2 * vD + (1 - beta2) * (gradD**2)
        mD_ = mD / (1 - beta1**i)
        vD_ = vD / (1 - beta2**i)
        # Updating D
        D -= eta * mD_ / (np.sqrt(vD_) + epsilon)
        # Forcing D to be nonnegative
        D[D < 0] = 0
        VU = np.dot(V, U)
        # Adding a mask for ignoring missing values
        if nas is not None:
            VU[nas] = 0
        # Derivative for updating V
        gradV = -np.dot(B, P.T) + np.dot(np.dot(V, P), P.T) - alpha * np.dot(G, U.T) + alpha * np.dot(VU, U.T) + lambda2 * V
        mV = beta1 * mV + (1 - beta1) * gradV
        vV = beta2 * vV + (1 - beta2) * (gradV**2)
        mV_ = mV / (1 - beta1**i)
        vV_ = vV / (1 - beta2**i)
        # Updating V
        V -= eta * mV_ / (np.sqrt(vV_) + epsilon)
        # Forcing V to be nonnegative
        V[V < 0] = 0
        # Derivative for updating P
        gradP = -np.dot(D.T, A) + np.dot(np.dot(D.T, D), P) - np.dot(V.T, B) + np.dot(np.dot(V.T, V), P) + lambda3 * P
        mP = beta1 * mP + (1 - beta1) * gradP
        vP = beta2 * vP + (1 - beta2) * (gradP**2)
        mP_ = mP / (1 - beta1**i)
        vP_ = vP / (1 - beta2**i)
        # Updating P
        P -= eta * mP_ / (np.sqrt(vP_) + epsilon)
        # Forcing P to be nonnegative
        P[P < 0] = 0
        VU = np.dot(V, U)
        # Adding mask for ignoring missing values
        if nas is not None:
            VU[nas] = 0
        # # Derivative for updating U
        gradU = -alpha * np.dot(V.T, G) + alpha * np.dot(V.T, VU) + lambda4 * U
        mU = beta1 * mU + (1 - beta1) * gradU
        vU = beta2 * vU + (1 - beta2) * (gradU**2)
        mU_ = mU / (1 - beta1**i)
        vU_ = vU / (1 - beta2**i)
        # Updating U
        U -= eta * mU_ / (np.sqrt(vU_) + epsilon)
        i += 1
        # Updating cost function
        cost.append(objectiveFunction(A, B, G, D, V, P, U, lambda1, lambda2, lambda3, lambda4, alpha=alpha, nas=nas))
        # Calculating difference in the cost function
        change = cost[-2] - cost[-1]

    scores = np.dot(D, V.T)
    return {"scores": scores, "D": D, "V": V, "P": P, "U": U}

def convert_result(resultado):
    resultado["scores"] = resultado["scores"].tolist()
    resultado["D"] = resultado["D"].tolist()
    resultado["V"] = resultado["V"].tolist()
    resultado["P"] = resultado["P"].tolist()
    resultado["U"] = resultado["U"].tolist()
    return resultado

