# AWS_Nanodegree_Image_Classifier_VGG

This project is part of Udacity's AWS AI & ML Scholarship Nanodegree program. It involves training an image classifier to recognize different species of flowers using a deep learning model (VGG16). The model achieved a test accuracy of 92.70%.

## Project Structure
The project consists of three main files:


### 1. `Image_Classifier_Project_final.`ipynb`
- A Jupyter Notebook that integrates training and inference steps.
-Loads and preprocesses the image dataset
-Trains a deep learning-based image classifier
-Use the trained classifier to predict image content
-The trained model is saved as a checkpoint along with associated hyperparameters
- Visualizes the model’s performance as.

### 2. `train.py`
- Handles the training of the neural network on a dataset of flower images.
- Supports **VGG16** and **EfficientNet-B0** architectures.
- Uses **PyTorch** for model training and optimization.
- Saves the trained model checkpoint.

### 3. `predict.py`
- Loads a trained model and performs inference on new images.
- Supports **top-K class predictions**.

![Project Completion](image/Project_Completion)
