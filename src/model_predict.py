import pickle
import warnings

warnings.filterwarnings('ignore')
from utils import extract_feature


class model_predict(object):
    def __init__(self):
        self.model = pickle.load(open("GB_classifier.model", "rb"))

    def predict(self, filename):
        # extract features and reshape it
        features = extract_feature(filename, mfcc=True, chroma=True, mel=True).reshape(1, -1)
        # predict
        result = self.model.predict(features)[0]
        # show the result !
        print(filename, result[0])
        return result


# predict file
# print(model_predict().predict("data\\SAVEE\\DC_a03.wav"))
