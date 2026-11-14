import pandas as pd
from sklearn.model_selection import train_test_split

# Use Mage's decorators when running inside Mage. Outside Mage (pytest, CI) mage-ai is not
# installed, so fall back to no-op decorators and the file can still be imported.
try:
    if 'transformer' not in globals():
        from mage_ai.data_preparation.decorators import transformer
    if 'test' not in globals():
        from mage_ai.data_preparation.decorators import test
except ImportError:
    def transformer(func):
        return func

    def test(func):
        return func


@transformer
def transform(df, *args, **kwargs):
    """Split 80/20 and label each row in a new 'split' column."""
    train_df, test_df = train_test_split(df, test_size=0.3, random_state=42)

    train_df = train_df.copy()
    test_df = test_df.copy()
    train_df['split'] = 'train'
    test_df['split'] = 'test'

    result = pd.concat([train_df, test_df])
    print('Train rows:', len(train_df), '| Test rows:', len(test_df))
    return result


@test
def test_output(output, *args):
    assert 'split' in output.columns, 'split column missing'
