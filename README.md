# Fraud Detection System

Coursework for the PAP (Predictive Analytics for Prediction) MSc course: a binary
classifier for fraud detection on the NeurIPS 2022 [Bank Account Fraud](https://www.kaggle.com/datasets/sgpjesus/bank-account-fraud-dataset-neurips-2022)
dataset.

[`fraud-detection/`](fraud-detection/) has the exploration and per-model
hyperparameter tuning notebooks.

## TODO: productionize

Turn the notebook work into something closer to a real productin service:

- [ ] Abstract the model layer (training/inference behind a common interface, not notebook cells)
- [ ] Serving API for inference
- [ ] Monitoring
- [ ] Pipelines for cleaning and training
