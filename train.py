# -*- coding: utf-8 -*-
"""train.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ay5dNNCO7IRjZnz1nYJ53PHdcWrQ4SbU
"""

import os
import torch
from torch import nn, optim
from torchvision import datasets, transforms, models
import argparse
from torch.utils.data import DataLoader
from collections import OrderedDict

# Parse command line arguments
def parse_args():
    parser = argparse.ArgumentParser(description='Train a neural network on a dataset')
    parser.add_argument('data_dir', type=str, help='Path to dataset')
    parser.add_argument('--save_dir', type=str, default='./', help="Directory to save the model checkpoint")
    parser.add_argument('--architecture', type=str, default='vgg16', help="Model architecture")
    parser.add_argument('--epochs', type=int, default=10, help='Number of training epochs')
    parser.add_argument('--batch_size', type=int, default=32, help="Batch size for DataLoader")
    parser.add_argument('--hidden_units', type=int, default=512, help="Number of hidden units in the classifier")
    parser.add_argument('--learning_rate', type=float, default=0.001, help='Learning rate')
    parser.add_argument('--gpu', action='store_true', help="Use GPU")

    return parser.parse_args()


# Load the data
def load_data(data_directory):
    train_path = os.path.join(data_directory, 'train')
    test_path = os.path.join(data_directory, 'test')
    validation_path = os.path.join(data_directory, 'valid')

    train_transform = transforms.Compose([
        transforms.RandomRotation(30),
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    test_transform = transforms.Compose([
        transforms.Resize(255),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    validation_transform =  transforms.Compose([
        transforms.Resize(255),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    train_dataset = datasets.ImageFolder(train_path, transform=train_transform)
    test_dataset = datasets.ImageFolder(test_path, transform=test_transform)
    validation_dataset = datasets.ImageFolder(validation_path, transform=validation_transform)

    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=64, shuffle=True)
    test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=32, shuffle=False)
    validation_loader = torch.utils.data.DataLoader(validation_dataset, batch_size=32, shuffle=False)

    return train_loader, validation_loader, test_loader, train_dataset

def build_model(arch, hidden_units):
    if arch == "vgg16":
        model = models.vgg16(pretrained=True)
        input_features = 25088
    elif arch == "efficientnet_b0":
        model = models.efficientnet_b0(pretrained=True)
        input_features = 1280
    else:
        raise ValueError("Unsupported architecture. Please choose 'vgg16' or 'efficientnet_b0'")

    # Freeze parameters so we don't backpropagate through them
    for param in model.parameters():
        param.requires_grad = False


    # Define classifier
    classifier = nn.Sequential(
          OrderedDict([
              ("fc1", nn.Linear(input_features, 4096)),
              ("relu1", nn.ReLU()),
              ("dropout1", nn.Dropout(p=0.3)),
              ("fc2", nn.Linear(4096, hidden_units)),
              ("relu2", nn.ReLU()),
              ("dropout2", nn.Dropout(p=0.3)),
              ("fc3", nn.Linear(hidden_units, 102)),
              ("output", nn.LogSoftmax(dim=1)),
          ]))

    if arch == "vgg16":
      model.classifier = classifier
    elif arch == "efficientnet_b0":
      model.classifier = classifier

    return model, arch


# Train model
def train_model(model, train_loader, valid_loader, criterion, optimizer, device, epochs):
    model.to(device)
    train_loss,valid_loss, accuracy = 0, 0, 0

    for epoch in range(epochs):
        model.train()

        # Training
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            train_loss += loss.item()

        # Validation
        model.eval()

        with torch.no_grad():
            for inputs, labels in valid_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                valid_loss += loss.item()

                # Accuracy
                top_class = outputs.argmax(dim=1)
                accuracy += (top_class == labels).float().mean().item()

        # Output training and validation results
        print(f"Epoch {epoch+1}/{epochs}.. "
              f"Train Loss: {train_loss/len(train_loader):.3f}.. "
              f"Validation Loss: {valid_loss/len(valid_loader):.3f}.. "
              f"Validation Accuracy: {accuracy/len(valid_loader):.2f}")


# Save trained model
def save_checkpoint(model, save_dir, arch, hidden_units, train_data):
    checkpoint = {
        'arch': arch,
        'hidden_units': hidden_units,
        'state_dict': model.state_dict(),
        'class_to_idx': train_data.class_to_idx,
    }

    save_path = os.path.join(save_dir, 'checkpoint.pth')
    torch.save(checkpoint, save_path)
    print(f"Checkpoint saved ")


# Main function
def main():
    args = parse_args()
    train_loader, validation_loader, test_loader, train_dataset = load_data(args.data_dir, args.batch_size)


    model, arch = build_model(args.architecture, args.hidden_units)

    device = torch.device("cuda" if args.gpu and torch.cuda.is_available() else "cpu")
    criterion = nn.NLLLoss()
    optimizer = torch.optim.Adam(model.classifier.parameters(), lr=args.learning_rate)

    train_model(model, train_loader, validation_loader, criterion, optimizer, device, args.epochs)

    save_checkpoint(model, args.save_dir, args.architecture, args.hidden_units, train_dataset)

if __name__ == "__main__":
    main()