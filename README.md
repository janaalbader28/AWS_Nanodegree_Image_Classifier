# AWS_Nanodegree_Image_Classifier_VGG

This project is part of Udacity's AWS AI & ML Scholarship Nanodegree program. It involves training an image classifier to recognize different species of flowers using a deep learning model (VGG16). The model achieved a test accuracy of 92.70%.

## Project Structure
The project consists of three main files:

### 1. `train.py`
- Handles the training of the neural network on a dataset of flower images.
- Supports **VGG16** and **EfficientNet-B0** architectures.
- Uses **PyTorch** for model training and optimization.
- Implements data augmentation and normalization.
- Saves the trained model checkpoint.

### 2. `predict.py`
- Loads a trained model and performs inference on new images.
- Supports **top-K class predictions**.
- Can run on **CPU** or **GPU**.
- Accepts a JSON file for mapping class indices to class names.

### 3. `Image_Classifier_Project_final v3.ipynb`
- A Jupyter Notebook that integrates training and inference steps.
- Provides an interactive interface to test predictions.
- Visualizes the model’s performance.
