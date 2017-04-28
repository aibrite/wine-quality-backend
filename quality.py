import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd
import mglearn
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt


class WineQuality:

    def estimate_quality(self, params):

        if len(params) != 11:
            raise ValueError('Not all values have been posted')
        else:
            for param in params:
                if type(param) == float:
                    knn = KNeighborsClassifier(n_neighbors=50)
                    try:
                        dfx = pd.read_csv('resources/winequality.txt',
                                          sep=';', usecols=range(11))
                        dfy = pd.read_csv('resources/winequality.txt',
                                          sep=';', usecols=range(11, 12))
                    except IOError as e:
                        raise IOError(e.args[0])
                    else:
                        X_train, X_test, y_train, y_test = train_test_split(
                            dfx.values, dfy, random_state=0)
                        # iris_dataframe = pd.DataFrame(X_train, columns=dfx.columns.values)
                        # grr = pd.scatter_matrix(iris_dataframe, c=y_train, figsize=(
                        #     15, 15), marker='o', hist_kwds={'bins': 20}, s=60, alpha=.8, cmap=mglearn.cm3)
                        # plt.show()
                        knn.fit(dfx, dfy.values.ravel())
                        y_pred = knn.predict(params)
                        print("Test set score: {:.2f}".format(
                            np.mean(y_pred == y_test.values)))
                        print("KNN set score: {:.2f}".format(
                            knn.score(X_test, y_test)))
                        return y_pred
                else:
                    raise TypeError('Values shall be integers.')
