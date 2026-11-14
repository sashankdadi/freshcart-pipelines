import pytest
from sklearn.datasets import load_iris
from iris_project.transformers.validate_data import validate, test_no_missing_and_three_classes as check


def test_clean_iris_passes():
    df = load_iris(as_frame=True).frame
    check(validate(df))


def test_missing_value_is_caught():
    df = load_iris(as_frame=True).frame
    df.iloc[0, 0] = None
    with pytest.raises(AssertionError):
        check(validate(df))
