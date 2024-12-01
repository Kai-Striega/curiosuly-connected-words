import pickle
from typing import Protocol

import gensim.downloader
import numpy as np


class Word2VecModel(Protocol):

    def get_vector(self, word: str) -> np.ndarray:
        ...


def load_gensim_model(model_name: str) -> Word2VecModel:
    try:
        with open(f"{model_name}.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        model = gensim.downloader.load(model_name)

        with open(f"{model_name}.pkl", "wb") as f:
            pickle.dump(model, f)

        return model

