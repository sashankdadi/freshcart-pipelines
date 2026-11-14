import pandas as pd
from sklearn.datasets import load_iris

try:
    if 'data_loader' not in globals():
        from mage_ai.data_preparation.decorators import data_loader
    if 'test' not in globals():
        from mage_ai.data_preparation.decorators import test
except ImportError:
    def data_loader(func):
        return func

    def test(func):
        return func


@data_loader
def load_data(*args, **kwargs):
    """First step: bring the built-in Iris data in as a DataFrame (4 features + 'target')."""
    iris = load_iris(as_frame=True)
    df = iris.frame
    print('Rows loaded:', len(df))
    return df


@test
def test_output(output, *args):
    assert len(output) == 150, 'Iris must have 150 rows'
