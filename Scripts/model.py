import pandas as pd
import numpy as np
from joblib import load, dump
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import Any


def resource_path(relative_path: str) -> str:
    """
    This function returns the absolute path of the given relative path
    :param relative_path: The relative path
    :return: This returns the absolute path
    """
    import sys
    import os

    try:
        base_path: Any = sys._MEIPASS

    except Exception:
        base_path = os.path.abspath("..")

    return os.path.join(base_path, relative_path)

class Model:
    """
    This class will simplify the of using the Logistic Regression model
    """
    def __init__(self) -> None:
        """
        This contains the instances of LogisticRegression and TfidfVectorizer
        Here we'll load the training dataset and the most commonly used passwords
        """
        self.passwords: pd.DataFrame = pd.read_csv(resource_path("Datasets/data.csv"), sep=";").dropna()
        self.com_passwords: list[int] = pd.read_csv(resource_path("Datasets/10millionPasswords.csv")).iloc[::, 0].to_list()
        self.lr: LogisticRegression = LogisticRegression(max_iter=1000)
        self.vectorizer: TfidfVectorizer = TfidfVectorizer(analyzer="char")

        # here we convert the strength column from str type to int type
        self.passwords = self.passwords[self.passwords["strength"].isin(["0", "1", "2"])]
        self.passwords["strength"] = self.passwords["strength"].astype(int)

        # here, we create the x and y
        self.x: Any = self.vectorizer.fit_transform(self.passwords["password"])
        self.y: np.ndarray[tuple[int, ...], np.dtype[Any]] = self.passwords.iloc[::, -1].values

    def train(self) -> None:
        """
        Here we train the Logistic Regression model
        :return: This doesn't return anything
        """
        self.lr.fit(self.x, self.y)

    def save(self) -> None:
        """
        Here we save the trained Logistic Regression model and the TfidfVectorizer
        :return: This doesn't return anything
        """
        dump(self, resource_path("Model/models.pkl"))

    @staticmethod
    def load() -> Model:
        """
        Here we load this class
        :return: This returns this class
        """
        model: Model = load(resource_path("Model/models.pkl"))
        return model

    def evaluate(self, new_password: str) -> str:
        """
        Here we evaluate the Logistic Regression model and display it in a messagebox
        :param new_password: The new password
        :return: we return a short str telling the user if the password is weak, decent or strong
        """
        if new_password in self.com_passwords:
            return f"Your password: {new_password} is weak and common. Score: 0"

        y_pred: int | str = self.lr.predict(self.vectorizer.transform([new_password]))
        if y_pred == 0:
            y_pred = "weak"
            score = 0

        elif y_pred == 1:
            y_pred = "decent"
            score = 1

        else:
            y_pred = "strong"
            score = 2

        return f"Your password: {new_password} is {y_pred}. Score: {score}"


def main() -> None:
    """
    We train and save the model
    :return: This doesn't return anything
    """
    model: Model = Model()
    model.train()
    model.save()


if __name__ == '__main__':
    main()