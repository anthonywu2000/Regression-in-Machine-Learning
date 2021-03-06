import argparse
import numpy as np

import utils
import linear_model

from sklearn.linear_model import LogisticRegression

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-q','--question', required = True)
    io_args = parser.parse_args()
    question = io_args.question


    if question == "2":
        data = utils.load_dataset("logisticData")
        
        XBin, yBin = data['X'], data['y']
        XBinValid, yBinValid = data['Xvalid'], data['yvalid']

        model = linear_model.logReg(maxEvals=400)
        model.fit(XBin,yBin)

        print("\nlogReg Training error %.3f" % utils.classification_error(model.predict(XBin), yBin))
        print("logReg Validation error %.3f" % utils.classification_error(model.predict(XBinValid), yBinValid))
        print("# nonZeros: %d" % (model.w != 0).sum())

    elif question == "2.1":
        data = utils.load_dataset("logisticData")
        XBin, yBin = data['X'], data['y']
        XBinValid, yBinValid = data['Xvalid'], data['yvalid']

        model = linear_model.logRegL2(lammy=1.0, maxEvals=400)
        model.fit(XBin,yBin)

        print("\nlogRegL2 Training error %.3f" % utils.classification_error(model.predict(XBin), yBin))
        print("logRegL2 Validation error %.3f" % utils.classification_error(model.predict(XBinValid), yBinValid))
        print("# nonZeros: %d" % (model.w != 0).sum())
        

    elif question == "2.2":
        data = utils.load_dataset("logisticData")
        XBin, yBin = data['X'], data['y']
        XBinValid, yBinValid = data['Xvalid'], data['yvalid']

        model = linear_model.logRegL1(L1_lambda=1.0, maxEvals=400)
        model.fit(XBin,yBin)

        print("\nlogRegL1 Training error %.3f" % utils.classification_error(model.predict(XBin),yBin))
        print("logRegL1 Validation error %.3f" % utils.classification_error(model.predict(XBinValid), yBinValid))
        print("# nonZeros: %d" % (model.w != 0).sum())

    elif question == "2.3":
        data = utils.load_dataset("logisticData")
        XBin, yBin = data['X'], data['y']
        XBinValid, yBinValid = data['Xvalid'], data['yvalid']

        model = linear_model.logRegL0(L0_lambda=1.0, maxEvals=400)
        model.fit(XBin,yBin)

        print("\nTraining error %.3f" % utils.classification_error(model.predict(XBin),yBin))
        print("Validation error %.3f" % utils.classification_error(model.predict(XBinValid), yBinValid))
        print("# nonZeros: %d" % (model.w != 0).sum())

    elif question == "2.5":
        data = utils.load_dataset("logisticData")
        XBin, yBin = data['X'], data['y']
        XBinValid, yBinValid = data['Xvalid'], data['yvalid']

        # TODO
        ############# L2 ############
        LRL2 = LogisticRegression(penalty = 'l2', fit_intercept = False, C = 1)
        LRL2.fit(XBin, yBin)
        print("\nTraining error %.3f" % utils.classification_error(LRL2.predict(XBin),yBin))
        print("Validation error %.3f" % utils.classification_error(LRL2.predict(XBinValid), yBinValid))
        print("# nonZeros: %d" % (LRL2.coef_ != 0).sum())
        ############# L1 ############
        LRL1 = LogisticRegression(penalty = 'l1', fit_intercept = False, C = 1, solver = 'liblinear')
        LRL1.fit(XBin, yBin)
        print("\nTraining error %.3f" % utils.classification_error(LRL1.predict(XBin),yBin))
        print("Validation error %.3f" % utils.classification_error(LRL1.predict(XBinValid), yBinValid))
        print("# nonZeros: %d" % (LRL1.coef_ != 0).sum())

    elif question == "3":
        data = utils.load_dataset("multiData")
        XMulti, yMulti = data['X'], data['y']
        XMultiValid, yMultiValid = data['Xvalid'], data['yvalid']

        model = linear_model.leastSquaresClassifier()
        model.fit(XMulti, yMulti)

        print("leastSquaresClassifier Training error %.3f" % utils.classification_error(model.predict(XMulti), yMulti))
        print("leastSquaresClassifier Validation error %.3f" % utils.classification_error(model.predict(XMultiValid), yMultiValid))

        print(np.unique(model.predict(XMulti)))

    elif question == "3.2":
        data = utils.load_dataset("multiData")
        XMulti, yMulti = data['X'], data['y']
        XMultiValid, yMultiValid = data['Xvalid'], data['yvalid']

        model = linear_model.logLinearClassifier(maxEvals=500, verbose=0)
        model.fit(XMulti, yMulti)

        print("logLinearClassifier Training error %.3f" % utils.classification_error(model.predict(XMulti), yMulti))
        print("logLinearClassifier Validation error %.3f" % utils.classification_error(model.predict(XMultiValid), yMultiValid))

    elif question == "3.4":
        data = utils.load_dataset("multiData")
        XMulti, yMulti = data['X'], data['y']
        XMultiValid, yMultiValid = data['Xvalid'], data['yvalid']

        model = linear_model.softmaxClassifier(maxEvals=500)
        model.fit(XMulti, yMulti)

        print("Training error %.3f" % utils.classification_error(model.predict(XMulti), yMulti))
        print("Validation error %.3f" % utils.classification_error(model.predict(XMultiValid), yMultiValid))

    elif question == "3.5":
        data = utils.load_dataset("multiData")
        XMulti, yMulti = data['X'], data['y']
        XMultiValid, yMultiValid = data['Xvalid'], data['yvalid']

        # TODO
        ##### One-vs-All ####
        mod1 = LogisticRegression(C = 1e12, fit_intercept = False)
        mod1.fit(XMulti, yMulti)
        print("Training error %.3f" % utils.classification_error(mod1.predict(XMulti), yMulti))
        print("Validation error %.3f" % utils.classification_error(mod1.predict(XMultiValid), yMultiValid))
        ##### softmax ####
        mod2 = LogisticRegression(multi_class = "multinomial", solver = 'lbfgs', C = 1e12, fit_intercept = False)
        mod2.fit(XMulti, yMulti)
        print("Training error %.3f" % utils.classification_error(mod2.predict(XMulti), yMulti))
        print("Validation error %.3f" % utils.classification_error(mod2.predict(XMultiValid), yMultiValid))
