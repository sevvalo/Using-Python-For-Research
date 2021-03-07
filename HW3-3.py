import numpy as np, random, scipy.stats as ss

def majority_vote_fast(votes):
    mode, count = ss.mstats.mode(votes)
    return mode

def distance(p1, p2):
    return np.sqrt(np.sum(np.power(p2 - p1, 2)))

def find_nearest_neighbors(p, points, k=5):
    distances = np.zeros(points.shape[0])
    for i in range(len(distances)):
        distances[i] = distance(p, points[i])
    ind = np.argsort(distances)
    return ind[:k]

def knn_predict(p, points, outcomes, k=5):
    ind = find_nearest_neighbors(p, points, k)
    return majority_vote_fast(outcomes[ind])[0]

import pandas as pd

wine = pd.read_csv("wine.csv")

is_red = []
for i in wine.itertuples(): 
  if i.color == 'red':
    is_red.append(1)
  else:
    is_red.append(0)
    

wine["is_red"] = is_red

wine_new = wine.drop(["quality", 'color',"high_quality"], axis=1)
d = {"quality":wine["quality"],"high_quality":wine["high_quality"]}
numeric_data = pd.DataFrame(d)


import sklearn.preprocessing as sp
scaled_data = sp.scale(numeric_data)
data = pd.DataFrame(scaled_data, columns = numeric_data.columns )

import sklearn.decomposition as sd
pca = sd.PCA(n_components=2)
principal_components = pca.fit_transform(numeric_data)

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.backends.backend_pdf import PdfPages
observation_colormap = ListedColormap(['red', 'blue'])
x = principal_components[:,0]
y = principal_components[:,1]

plt.title("Principal Components of Wine")
plt.scatter(x, y, alpha = 0.2,
    c = data['high_quality'], cmap = observation_colormap, edgecolors = 'none')
plt.xlim(-8, 8); plt.ylim(-8, 8)
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.show()

def accuracy(predictions, outcomes):  
    return (np.sum(predictions == outcomes)/len(outcomes))*100
sum = 0
for i in numeric_data["high_quality"]:
  if i == 0:
    sum +=1
(sum/len(numeric_data)) * 100

from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors = 5)
knn.fit(data, numeric_data['high_quality'])
library_predictions = knn.predict(data)
accuracy(library_predictions, numeric_data["high_quality"])


n_rows = numeric_data.shape[0]
random.seed(123)
selection = random.sample(range(n_rows), 10)

predictors = np.array(data)
training_indices = [i for i in range(len(predictors)) if i not in selection]
outcomes = np.array(numeric_data["high_quality"])

my_predictions =np.array([predictors[selection], knn_predict(p, predictors[training_indices,:], outcomes[training_indices], k=5)])
percentage = accuracy(my_predictions, data.high_quality.iloc[selection])


















