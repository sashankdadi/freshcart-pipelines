import joblib
from sklearn.tree import DecisionTreeClassifier

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

FEATURES = ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']


@transformer
def train(df, *args, **kwargs):
    """Train a decision tree. max_depth comes from the pipeline variables / --runtime-vars."""
    max_depth = int(kwargs.get('max_depth', 3))

    train_df = df[df['split'] == 'train']
    test_df = df[df['split'] == 'test'].copy()

    model = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
    model.fit(train_df[FEATURES], train_df['target'])

    test_df['predicted'] = model.predict(test_df[FEATURES])
    accuracy = (test_df['predicted'] == test_df['target']).mean()
    print('max_depth =', max_depth, '| Test accuracy =', round(accuracy, 3))

    joblib.dump(model, 'iris_model.pkl')
    return test_df


@test
def test_accuracy(output, *args):
    """The gate: if this fails, save_results and evaluate_model never run."""
    accuracy = (output['predicted'] == output['target']).mean()
    assert accuracy >= 0.8, 'Model accuracy is below 80%'
