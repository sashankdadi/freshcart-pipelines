# C3 - evaluation branch: runs in parallel with save_results, both downstream of train_model.
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

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
def evaluate(df, *args, **kwargs):
    y_true = df['target']
    y_pred = df['predicted']

    print('Confusion matrix:')
    print(pd.crosstab(y_true, y_pred, rownames=['actual'], colnames=['predicted']))

    metrics = pd.DataFrame({
        'metric': ['accuracy', 'precision', 'recall', 'f1_score'],
        'value': [
            round(accuracy_score(y_true, y_pred), 3),
            round(precision_score(y_true, y_pred, average='macro', zero_division=0), 3),
            round(recall_score(y_true, y_pred, average='macro', zero_division=0), 3),
            round(f1_score(y_true, y_pred, average='macro', zero_division=0), 3),
        ]
    })
    print('Metrics table:')
    print(metrics.to_string(index=False))
    return metrics


@test
def test_metrics_in_range(output, *args):
    assert len(output) == 4, 'expected 4 metrics'
    assert output['value'].between(0, 1).all(), 'metrics must be between 0 and 1'
