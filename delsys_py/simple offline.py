# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 12:36:34 2024

@author: Lab412
"""

from libemg.datasets import OneSubjectMyoDataset
from libemg.emg_predictor import EMGClassifier
from libemg.feature_extractor import FeatureExtractor
from libemg.offline_metrics import OfflineMetrics
import matplotlib.pyplot as plt

WINDOW_SIZE = 20
WINDOW_INCREMENT = 10
FEATURE_SET = "HTD"
fe = FeatureExtractor()
om = OfflineMetrics()

# Load in dataset
dataset = OneSubjectMyoDataset()
data = dataset.prepare_data()

# Split data into training and testing
train_data = data.isolate_data("sets", [0,1,2])
test_data = data.isolate_data("sets", [3,4,5])

# Extract windows
train_windows, train_meta = train_data.parse_windows(WINDOW_SIZE, WINDOW_INCREMENT)
test_windows, test_meta = test_data.parse_windows(WINDOW_SIZE, WINDOW_INCREMENT)

# Create data set dictionary using training data
data_set = {}
data_set['training_features'] = fe.extract_feature_group(FEATURE_SET, train_windows)
data_set['training_labels'] = train_meta['classes']

test_features = fe.extract_feature_group(FEATURE_SET, test_windows)

classifiers = ["LDA","SVM","KNN","RF","QDA"]

# Extract metrics for each classifier
for classifier in classifiers:
    model = EMGClassifier(classifier)

    # Fit and run the classifier
    model.fit(data_set.copy())
    preds, probs = model.run(test_features)

    # Null label is 2 since it is the no movement class
    metrics = om.extract_common_metrics(test_meta["classes"], preds, 2)
    
# Plot feature space
fe.visualize_feature_space(data_set['training_features'], projection="PCA", classes=train_meta['classes'], test_feature_dic=test_features, t_classes=test_meta['classes'])
