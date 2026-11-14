# C4 - my own block: a data-quality gate between load_iris and prepare_data.

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
def validate(df, *args, **kwargs):
    """Pass the data through unchanged and print a short quality summary."""
    print('Missing values:', int(df.isnull().sum().sum()), '| Classes:', sorted(df['target'].unique().tolist()))
    return df


@test
def test_no_missing_and_three_classes(output, *args):
    assert output.isnull().sum().sum() == 0, 'Iris must have no missing values'
    assert output['target'].nunique() == 3, 'Iris must have exactly 3 classes'
