"""Reproducible scikit-learn baseline estimators."""
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


def build_random_forest(random_state: int = 42) -> RandomForestClassifier:
    return RandomForestClassifier(
        n_estimators=300,
        class_weight="balanced",
        random_state=random_state,
        n_jobs=-1,
    )


def build_svm(random_state: int = 42) -> Pipeline:
    return Pipeline(
        steps=[
            ("scale", StandardScaler()),
            ("classifier", SVC(class_weight="balanced", probability=True, random_state=random_state)),
        ]
    )
