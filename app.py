from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import pickle
import numpy as np
# from model import NLPModel

app = Flask(__name__)
api = Api(app)

# model = NLPModel()

# clf_path = 'lib/models/BiasClassifier.pkl'
# with open(clf_path, 'rb') as f:
#     model.clf = pickle.load(f)

# argument parsing
parser = reqparse.RequestParser()
parser.add_argument('query')


class PredictBias(Resource):
    def get(self):
        # use parser and find the user's query
        args = parser.parse_args()
        user_query = args['query']

        # Do prediction
        prediction = 0
        pred_proba = np.array([0,0])

        # Output either 'Negative' or 'Positive' along with the score
        if prediction == 0:
            pred_text = 'Negative'
        else:
            pred_text = 'Positive'

        # round the predict proba value and set to new variable
        confidence = round(pred_proba[0], 3)

        # create JSON object
        output = {'prediction': pred_text, 'confidence': int(confidence)}

        return output


# Setup the Api resource routing here
# Route the URL to the resource
api.add_resource(PredictBias, '/')


if __name__ == '__main__':
    app.run(debug=True)
