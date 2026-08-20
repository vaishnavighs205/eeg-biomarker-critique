from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC


def build_logistic_regression(random_state: int = 42):
    return LogisticRegression(max_iter=5000, class_weight="balanced", random_state=random_state)


def build_linear_svm(random_state: int = 42):
    return SVC(kernel="linear", class_weight="balanced", probability=True, random_state=random_state)
