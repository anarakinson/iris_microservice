import pickle
import os
import warnings
import logging
import pandas as pd
warnings.filterwarnings("ignore")


PATH_TO_MODELS = "models"
model_name = "random_forest_model.pkl"

FEATURES = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
TARGETS = ['setosa', 'versicolor', 'virginica']

model_path = os.path.join(PATH_TO_MODELS, model_name)

###
# functions
###
def load_model():
    '''
    Function to create model
    '''
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    return model

def get_pred(model, data):
    """
    Predict function
    Get dictionary with data
    in format like {sepal_length, sepal_width, petal_length, petal_width}
    """
    print(data)
    df = pd.DataFrame(columns=FEATURES)
    df = df.append(data, ignore_index=True)
    df = df.astype("float")
    print(df)
    pred = model.predict_proba(df)
    pred_round = [f"{elem : .3f}" for elem in pred[0]]
    out = pd.concat([pd.Series(TARGETS), pd.Series(pred_round)], axis=1)
    out.columns = ["class", "probability"]

    logging.info(f'[PREDICTION] \n{out}')

    return out


if __name__ == "__main__":
    print(model_path)
    model = load_model()
    data = {
        "sepal_width" : 0.1,
        "sepal_length" : 0.1,
        "petal_width" : 0.1,
        "petal_length" : 0.1,
    }
    pred = get_pred(model, data)
    print(pred)
