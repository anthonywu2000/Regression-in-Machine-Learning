import numpy as np
from numpy.linalg import solve
from numpy.linalg import norm
import findMin
from scipy.optimize import approx_fprime
import utils

class logReg:
    # Logistic Regression
    def __init__(self, verbose=0, maxEvals=100):
        self.verbose = verbose
        self.maxEvals = maxEvals
        self.bias = True

    def funObj(self, w, X, y):
        yXw = y * X.dot(w)

        # Calculate the function value
        f = np.sum(np.log(1. + np.exp(-yXw)))

        # Calculate the gradient value
        res = - y / (1. + np.exp(yXw))
        g = X.T.dot(res)

        return f, g

    def fit(self,X, y):
        n, d = X.shape

        # Initial guess
        self.w = np.zeros(d)
        utils.check_gradient(self, X, y)
        (self.w, f) = findMin.findMin(self.funObj, self.w,
                                      self.maxEvals, X, y, verbose=self.verbose)
    def predict(self, X):
        return np.sign(X@self.w)

################ L0 #################

class logRegL0(logReg):
    # L0 Regularized Logistic Regression
    def __init__(self, L0_lambda=1.0, verbose=2, maxEvals=400):
        self.verbose = verbose
        self.L0_lambda = L0_lambda
        self.maxEvals = maxEvals

    def fit(self, X, y):
        n, d = X.shape
        minimize = lambda ind: findMin.findMin(self.funObj, np.zeros(len(ind)), self.maxEvals, X[:, ind], y, verbose=0)
        selected = set()
        selected.add(0)
        minLoss = np.inf
        oldLoss = 0
        bestFeature = -1

        while minLoss != oldLoss:
            oldLoss = minLoss
            print("Epoch %d " % len(selected))
            print("Selected feature: %d" % (bestFeature))
            print("Min Loss: %.3f\n" % minLoss)

            for i in range(d):
                if i in selected:
                    continue

                # this is a set, so list(selected_new) makes to list
                selected_new = selected | {i} # tentatively add feature "i" to the selected set
                # TODO for Q2.3: Fit the model with 'i' added to the features,
                # then compute the loss and update the minLoss/bestFeature

                #first compute the score using minimize
                w, score = minimize(list(selected_new)) 
                score += self.L0_lambda * len(selected_new)
                # findMin returns w, f
                #update the minLoss and bestFeature
                if score < minLoss:
                    minLoss = score
                    bestFeature = i

            selected.add(bestFeature)
        
        self.w = np.zeros(d)
        self.w[list(selected)], _ = minimize(list(selected))


class leastSquaresClassifier:
    def fit(self, X, y):
        n, d = X.shape
        self.n_classes = np.unique(y).size

        # Initial guess
        self.W = np.zeros((self.n_classes,d))

        for i in range(self.n_classes):
            ytmp = y.copy().astype(float)
            ytmp[y==i] = 1
            ytmp[y!=i] = -1

            # solve the normal equations
            # with a bit of regularization for numerical reasons
            self.W[i] = np.linalg.solve(X.T@X+0.0001*np.eye(d), X.T@ytmp)

    def predict(self, X):
        return np.argmax(X@self.W.T, axis=1)

################ Q3.2 #################
class logLinearClassifier: 
    
    def __init__(self, maxEvals = 100, verbose = 0):
        self.maxEvals = maxEvals
        self.verbose = verbose
    
    def funObj(self, w, X, y):
        yXw = y * X.dot(w)

        # Calculate the function value
        f = np.sum(np.log(1. + np.exp(-yXw)))

        # Calculate the gradient value
        res = - y / (1. + np.exp(yXw))
        g = X.T.dot(res)
        return f, g
    
    def fit(self, X, y):
        n, d = X.shape
        self.n_classes = np.unique(y).size

        # Initial guess
        self.W = np.zeros((self.n_classes,d))

        for i in range(self.n_classes):
            ytmp = y.copy().astype(float)
            ytmp[y==i] = 1
            ytmp[y!=i] = -1

            # solve the normal equations
            # with a bit of regularization for numerical reasons
            # self.W[i] = np.linalg.solve(X.T@X+0.0001*np.eye(d), X.T@ytmp)
            
            # this is to optimize over the log regression
            (self.W[i], f) = findMin.findMin(self.funObj, self.W[i],
                                      self.maxEvals, X, ytmp, verbose=self.verbose)
            
            self.w = self.W[i]

    def predict(self, X):
        return np.argmax(X@self.W.T, axis=1)

################ Q3.4 #################

class softmaxClassifier:
    def __init__(self, maxEvals = 100, verbose = 0):
        self.maxEvals = maxEvals
        self.verbose = verbose
    
    def funObj(self, w, X, y): 
        n,d = X.shape
        k = self.n_classes # number of independent classifiers
        W = np.reshape(w, (k, d)) # flatten a matrix W into vector parameters

        XW = np.dot(X, W.T)
        M = np.sum(np.exp(XW), axis = 1)

        y_bin = np.zeros((n, k)).astype(bool)
        y_bin[np.arange(n), y] = 1

        f = -np.sum(XW[y_bin] - np.log(M))
        grad = (np.exp(XW) / M[:,None] - y_bin).T@X

        return f, grad.flatten()

    def fit(self, X, y):
        n, d = X.shape
        self.n_classes = np.unique(y).size
        k = self.n_classes
        self.W = np.zeros(d*k)
        self.w = self.W 
        (self.W, f) = findMin.findMin(self.funObj, self.W,
                                      self.maxEvals, X, y, verbose=self.verbose)
        self.W = np.reshape(self.W, (k, d))

    def predict(self, X):
        return np.argmax(X@self.W.T, axis=1)
    


################ L2 #################

class logRegL2(logReg):

    def __init__(self, lammy = 1.0, verbose=0, maxEvals=100):
        self.verbose = verbose
        self.maxEvals = maxEvals
        self.bias = True
        self.lammy = lammy

    def funObj(self, w, X, y):
        yXw = y * X.dot(w)

        # Calculate the function value
        f = np.sum(np.log(1. + np.exp(-yXw))) + (0.5 * self.lammy * norm(w)**2)
        
        # Calculate the gradient value
        res = - y / (1. + np.exp(yXw))
        g = X.T.dot(res) + self.lammy * w

        return f, g

################ L1 #################

class logRegL1(logReg): 

    def __init__(self, L1_lambda = 1.0, verbose=0, maxEvals=100):
        self.verbose = verbose
        self.maxEvals = maxEvals
        self.bias = True
        self.L1_lambda = L1_lambda

    def funObj(self, w, X, y):
        yXw = y * X.dot(w)

        # Calculate the function value
        f = np.sum(np.log(1. + np.exp(-yXw)))

        # Calculate the gradient value
        result = - y / (1. + np.exp(yXw))
        g = X.T.dot(result)

        return f, g

    def fit(self,X, y):
        n, d = X.shape

        # Initial guess
        self.w = np.zeros(d)
        utils.check_gradient(self, X, y)
        (self.w, f) = findMin.findMinL1(self.funObj, self.w, self.L1_lambda, self.maxEvals, X, y, verbose=self.verbose)



    
