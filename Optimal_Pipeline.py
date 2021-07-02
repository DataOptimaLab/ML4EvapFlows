import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import make_pipeline, make_union
from sklearn.preprocessing import MaxAbsScaler
from tpot.builtins import StackingEstimator
from xgboost import XGBRegressor
from tpot.export_utils import set_param_recursive

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('target', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'], random_state=20)

# Average CV score on the training set was: -6.2820709345171
exported_pipeline = make_pipeline(
    StackingEstimator(estimator=ExtraTreesRegressor(bootstrap=False, max_features=0.9000000000000001, min_samples_leaf=4, min_samples_split=4, n_estimators=100)),
    MaxAbsScaler(),
    StackingEstimator(estimator=XGBRegressor(learning_rate=0.1, max_depth=10, min_child_weight=3, n_estimators=100, nthread=1, objective="reg:squarederror", subsample=0.55)),
    KNeighborsRegressor(n_neighbors=8, p=1, weights="distance")
)
# Fix random state for all the steps in exported pipeline
set_param_recursive(exported_pipeline.steps, 'random_state', 20)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
