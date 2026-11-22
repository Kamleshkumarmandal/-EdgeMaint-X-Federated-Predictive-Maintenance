# Experimental methodology

## Initial task

Bearing-condition classification using public vibration recordings.

The first experiment will use a clearly documented subset of CWRU recordings. Dataset selection, labels, sampling rates, channel selection and source recording identifiers must be tracked in a manifest.

## Preprocessing

1. Load the selected MATLAB channel.
2. Validate the waveform and sampling rate.
3. Optionally remove a documented mean or baseline offset; do not silently filter signals.
4. Segment into fixed-length windows with a documented window size and stride.
5. Associate every window with its source recording identifier and class label.
6. Split at source-recording level before fitting any learned preprocessing.

Overlapping windows from a single source recording must not be randomly divided across train and test. This would leak highly correlated signal segments and inflate evaluation results.

## Baselines

Train a Random Forest and a scaled Support Vector Machine using extracted statistical and frequency-domain features. Fix random seeds and record library versions.

## Deep learning

Train a 1D-CNN on fixed-length vibration windows. Define the input sample rate, window size, architecture, optimizer, learning rate, batch size, epoch count and stopping rule in a tracked experiment configuration.

## Federated learning

Create three to five virtual clients. Compare:

- IID client partitions.
- Non-IID client label proportions generated with a Dirichlet distribution.
- Centralized training against sample-weighted FedAvg.

All clients must use the same model definition and compatible parameter names and shapes.

## Evaluation

Report:

- Accuracy.
- Macro precision, macro recall and macro-F1.
- Per-class precision, recall and F1.
- Confusion matrix.
- Training and inference time.
- Number of communication rounds.
- Model update size and communication volume.
- Centralized vs federated performance difference.

Report test results only after the experiment has run. Include dataset subset, split strategy, seeds, hyperparameters and software versions so that results can be reproduced.

## Limits

This project starts with fault classification. It does not claim Remaining Useful Life prediction, certified industrial diagnosis, formal privacy guarantees or deployment-grade safety assurance.
