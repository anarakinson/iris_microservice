import pickle
import os
import warnings

warnings.filterwarnings("ignore")


PATH_TO_MODELS = "models"
model_name = "random_forest_model.pkl"

model_path = os.path.join(PATH_TO_MODELS, model_name)

def load_model(model_path):

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    return model

if __name__ == "__main__":
    print(model_path)
    load_model(model_path)
