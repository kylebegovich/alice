import random

import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier

# {{{ Command Matching Model

class CommandMatchingModel:

    def __init__(self, dataset, shuffle=True, train=False, name="",
            grammar=None, loss="squared_hinge", penalty="elasticnet",
            alpha=1e-3, n_iter=5):
        """
        Creates an instance of the CommandMatchingModel.

        Params:
            dataset -   Python 2D List. Should have length 2, where the 0th
                        index contains the "True" data values and the 1st index
                        contains the "False" data values
            shuffle -   Boolean. If true, will shuffle the dataset using
                        random.shuffle. True by default.
            train   -   Boolean. If true, will train the classifier within the
                        constructor. False by default.
            name    -   The name of the model. This is optional, and is only
                        used to identify the model externally
            grammar -   Optional dictionary of grammatical rules that any
                        matches must follow. None by default.

            The below parameters are parameters for the SKLearn SGDClassifier.
            See the sci-kit learn documentation for their meanings.

                - loss
                - penalty
                - alpha
                - n_iter

        """
        assert(len(dataset.keys()) == 2 and type(dataset["true"]) == list and type(dataset["false"]) == list)

        self.name = name
        self.grammar = grammar
        self.loss = loss
        self.penalty = penalty
        self.alpha = alpha
        self.n_iter = n_iter

        self.data = [ (i, "True") for i in dataset["true"] ] + [ (i, "False") for i in dataset["false"] ]
        if shuffle:
            random.shuffle(self.data)

        self.trained = False
        if train:
            try:
                self.train()
                self.trained = True
            except:
                pass

    def train(self):
        # Build training_set as a scikit-learn Bunch
        training_set = {
            "description" : "dataset for " + self.name,
            "data" : [ t[0] for t in self.data ],
            "target_names" : ["True", "False"],
            "target" : [ t[1] for t in self.data ]
        }

        # Use Pipeline to train using SVM and Tfidf Feature Extraction
        self.classifier = Pipeline(
            [   ("vect", CountVectorizer()),
                ("tfidf", TfidfTransformer()),
                ("clsfr", SGDClassifier(
                    loss=self.loss,
                    penalty=self.penalty,
                    alpha=self.alpha,
                    n_iter=self.n_iter,
                    random_state=random.randint(0, 1000)
                )),
            ])
        _ = self.classifier.fit(training_set["data"], training_set["target"])

    def match(self, s):
        """
        Return Values:
            True -  s matches the classifier
            False - s does not match the classifier
            None -  the classifier has not been trained yet
        """
        if self.trained == False:
            print "Classifier has not been trained yet! Cannot match!"
            return None

        test = [ s.lower() ]
        predicted = self.classifier.predict(test)
        return predicted[0] == "True"

# }}}
# {{{ Ordinal Scale Model
class OrdinalScaleModel:

    def __init__(self, dataset, shuffle=True, train=False, name="",
            grammar=None, loss="squared_hinge", penalty="elasticnet", alpha=1e-3, n_iter=5):
        """
        Creates an instance of the CommandMatchingModel.

        Params:
            dataset -   Python Dictionary object. The key denotes the ordinal
                        value, and the value is a list of all data points that
                        are to be matched with corresponding ordinal value
            shuffle -   Boolean. If true, will shuffle the dataset using
                        random.shuffle. True by default.
            train   -   Boolean. If true, will train the classifier within the
                        constructor. False by default.
            name    -   The name of the model. This is optional, and is only
                        used to identify the model externally
            grammar -   Always None. Parameter exists for conformity.

            The below parameters are parameters for the SKLearn SGDClassifier.
            See the sci-kit learn documentation for their meanings.

                - loss
                - penalty
                - alpha
                - n_iter

        """
        assert(type(dataset) == dict)
        for key in dataset:
            assert(type(key) == str and type(dataset[key]) == list)

        self.name = name
        self.loss = loss
        self.penalty = penalty
        self.alpha = alpha
        self.n_iter = n_iter

        self.data = []
        self.target_names = []
        for key in dataset:
            self.data += [ (i, key) for i in dataset[key] ]
            self.target_names.append(key)

        if shuffle:
            random.shuffle(self.data)

        self.trained = False
        if train:
            try:
                self.train()
                self.trained = True
            except:
                pass

    def train(self):
        # Build training_set as a scikit-learn Bunch
        training_set = {
            "description" : "dataset for " + self.name,
            "data" : [ t[0] for t in self.data ],
            "target_names" : self.target_names,
            "target" : [ t[1] for t in self.data ]
        }

        # Use Pipeline to train using SVM and Tfidf Feature Extraction
        self.classifier = Pipeline(
            [   ("vect", CountVectorizer()),
                ("tfidf", TfidfTransformer()),
                ("clsfr", SGDClassifier(
                    loss=self.loss,
                    penalty=self.penalty,
                    alpha=self.alpha,
                    n_iter=self.n_iter,
                    random_state=random.randint(0, 1000)
                )),
            ])
        _ = self.classifier.fit(training_set["data"], training_set["target"])

    def rate(self, s):
        """
        Return Values:
            int - Denotes the rating of input phrase
        """
        if self.trained == False:
            print "Classifier has not been trained yet! Cannot match!"
            return None

        test = [ s.lower() ]
        predicted = self.classifier.predict(test)
        try:
            return int(predicted[0])
        except:
            return -1

    def get_range(self):
        tmp = self.target_names
        try:
            tmp = map(int, tmp)
        except:
            print "[ ERROR ] Non-int key found in Model: %s" % (self.name,)
            return None
        return ( min(tmp), max(tmp) )

# }}}

