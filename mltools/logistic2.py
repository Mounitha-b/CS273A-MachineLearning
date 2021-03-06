import numpy as np

from .base import classifier
from .base import regressor
from .utils import toIndex, fromIndex, to1ofK, from1ofK
from numpy import asarray as arr
from numpy import atleast_2d as twod
from numpy import asmatrix as mat
import matplotlib.pyplot as plt



################################################################################
## LOGISTIC REGRESSION CLASSIFIER ##############################################
################################################################################


class logisticClassify2(classifier):
    """A binary (2-class) logistic regression classifier

    Attributes:
        classes : a list of the possible class labels
        theta   : linear parameters of the classifier
                  (1xN numpy array, where N=# features)
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor for logisticClassify2 object.

        Parameters: Same as "train" function; calls "train" if available

        Properties:
           classes : list of identifiers for each class
           theta   : linear coefficients of the classifier; numpy array
                      shape (1,N) for binary classification or (C,N) for C classes
        """
        self.classes = []
        self.theta = np.array([])

        if len(args) or len(kwargs):      # if we were given optional arguments,
            self.train(*args,**kwargs)    #  just pass them through to "train"


    def __repr__(self):
        str_rep = 'logisticClassify2 model, {} features\n{}'.format(
                   len(self.theta), self.theta)
        return str_rep


    def __str__(self):
        str_rep = 'logisticClassify2 model, {} features\n{}'.format(
                   len(self.theta), self.theta)
        return str_rep


## CORE METHODS ################################################################

    def plotBoundary(self,X,Y):
        """ Plot the (linear) decision boundary of the classifier, along with data """

        # Plot data (X[:,0] vs X[:,1], colored by class Y[:]
        plt.scatter(X[:,0], X[:,1], c = Y)

        # Plot decision boundary defined by theta0 + theta1 X1 + theta2 X2 == 0
        xs = np.linspace(np.min(X[:, 0]), np.max(X[:, 0]), 200) # densely sample possible x-values
        xs = xs[:, np.newaxis]
        ys = (self.theta[0, 0] + self.theta[0, 1] * xs)/-self.theta[0, 2]
        plt.plot(xs, ys)
        plt.show()

    def predictSoft(self, X):
        """ Return the probability of each class under logistic regression """
        raise NotImplementedError
        ## You do not need to implement this function.
        ## If you *want* to, it should return an Mx2 numpy array "P", with
        ## P[:,1] = probability of class 1 = sigma( theta*X )
        ## P[:,0] = 1 - P[:,1] = probability of class 0
        return P

    def predict(self, X):
        """ Return the predictied class of each data point in X"""
        # Computes linear response for the input data
        z = np.zeros(shape=(X.shape[0], 1))
        z = self.theta[0, 0] + self.theta[0, 1] * X[:,0] + self.theta[0, 2] * X[:,1]

        # Predicting a class based on the linear response
        Yhat = z
        Yhat[Yhat > 0] = self.classes[1]
        Yhat[Yhat <= 0] = self.classes[0]

        return Yhat

    def logistic(self, Z):
        return 1.0 / (1.0 + np.exp(-Z))

    def train(self, X, Y, initStep=1.0, stopTol=1e-4, stopIter=5000, plot=None):
        """ Train the logistic regression using stochastic gradient descent """
        ## First do some bookkeeping and setup:
        self.theta,X,Y = twod(self.theta), arr(X), arr(Y)   # convert to numpy arrays
        M,N = X.shape
        if Y.shape[0] != M:
            raise ValueError("Y must have the same number of data (rows) as X")
        self.classes = np.unique(Y)
        if len(self.classes) != 2:
            raise ValueError("Y should have exactly two classes (binary problem expected)")
        if self.theta.shape[1] != N+1:         # if self.theta is empty, initialize it!
            self.theta = np.random.randn(1,N+1)
        # Some useful modifications of the data matrices:
        X1  = np.hstack((np.ones((M,1)),X))    # make data array with constant feature
        Y01 = toIndex(Y, self.classes)         # convert Y to canonical "0 vs 1" classes

        it   = 0
        done = False
        Jsur = []
        J01  = []
        while not done:
            step = (2.0 * initStep) / (2.0 + it)   # common 1/iter step size change
            si = []
            for i in range(M):  # for each data point i:
                ## Computing the linear response
                zi = X1[i, :].dot(self.theta.T)
                ## Computing the prediction yi
                yi = Y01[i]
                ## Computing soft response
                si.append(self.logistic(zi))
                ## Computing gradient of logistic loss
                gradi = (si[i] - yi) * X1[i, :]
                # Take a step down the gradient
                self.theta = self.theta - step * gradi

            # each pass, compute surrogate loss & error rates:
            J01.append( self.err(X,Y) )
            ## Computing surrogate loss
            sum_i = 0
            for i in range(M):
                sum_i += Y01[i] * si[i] * np.log(si[i]) + (1 - Y01[i]) * (1 - si[i]) * np.log(1 - si[i])
            Jsur.append( sum_i / M ) ## TODO ...

            ## For debugging: print current parameters & losses
            # print self.theta, ' => ', Jsur[-1], ' / ', J01[-1]
            # raw_input()   # pause for keystroke

            # check stopping criteria:
            it += 1
            done = (it > stopIter) or ( (it>1) and (abs(Jsur[-1]-Jsur[-2])<stopTol) )
        self.numberOfIterations = it
        if self.plotFlag == True:
            plt.semilogx(range(it), np.abs(Jsur), label='Surrogate Loss')
            plt.semilogx(range(it), np.abs(J01), label='Error Rate')
            plt.legend(loc='upper right')
            plt.xlabel('# of iterations')
            plt.ylabel('Losses')
            plt.show()


################################################################################
################################################################################
################################################################################
