# -*- coding: utf-8 -*-
"""

#Don't change batch size
batch_size = 64

from torch.utils.data.sampler import SubsetRandomSampler
import torch
import torch.nn as nn
from torchvision import datasets, transforms
from torch.nn import functional as F

import matplotlib.pyplot as plt
import numpy as np
from torch.autograd import Variable

# Extract the MNIST Data
train_data = datasets.MNIST('./data', train=True, download=True,
                   transform=transforms.Compose([
                       transforms.ToTensor(),
                       transforms.Normalize((0.1307,), (0.3081,))
                   ]))
test_data = datasets.MNIST('./data', train=False, download=True,
                   transform=transforms.Compose([
                       transforms.ToTensor(),
                       transforms.Normalize((0.1307,), (0.3081,))
                   ]))

subset_indices = ((train_data.targets == 0) + (train_data.targets == 1)).nonzero()
train_loader = torch.utils.data.DataLoader(train_data,batch_size=batch_size, 
  shuffle=False,sampler=SubsetRandomSampler(subset_indices.view(-1)))


subset_indices = ((test_data.targets == 0) + (test_data.targets == 1)).nonzero()
test_loader = torch.utils.data.DataLoader(test_data,batch_size=batch_size, 
  shuffle=False,sampler=SubsetRandomSampler(subset_indices.view(-1)))

#Data Size 
dataiter=iter(train_loader)
images, labels = dataiter.next()
print(images.shape)
print(labels.shape)

# View the Images
figure = plt.figure()
num_of_images = 60
for index in range(1, num_of_images + 1):
    plt.subplot(6, 10, index)
    plt.imshow(images[index].numpy().squeeze())

# Parameter Configuration 
num_epochs = 20
input_size = 28*28
num_classes = 1 
momentum = 0.9 #moving avg of momentum
learning_rate = 0.001

"""# ***Logistic Regression***"""

#Logistic regression model and Loss Function using Logistic Regression Loss formula 

# ** No Momentum** 
# 1. Defind Model Class for Logistic Regression
class LogisticRegression(torch.nn.Module):
    def __init__(self, input_size, num_classes):
        super(LogisticRegression, self).__init__()
        self.linear = torch.nn.Linear(input_size, num_classes)

    def forward(self, x):
        outputs = self.linear(x)
        return outputs

# 2. Define Model Class for Logstici Loss function
class Logistic_Loss(nn.modules.Module):    
    def __init__(self):
        super(Logistic_Loss,self).__init__()
    def forward(self, outputs, labels):
        batch_size = outputs.size()[0]
        return torch.sum(torch.log(1 + torch.exp(-(outputs.t()*labels))))/batch_size
# 3. Apply Logsitic Regression function to model
logistic_model = LogisticRegression(input_size, num_classes)
# 4. Custom Loss criteria and SGD optimizer
criterion = Logistic_Loss()
#not using momentum optimzer here
log_optimizer = torch.optim.SGD(logistic_model.parameters(), lr=learning_rate)
total_step = len(train_loader)

# 5. Train the model

for epoch in range(num_epochs):
    avg_loss_epoch = 0
    batch_loss = 0
    total_batches = 0

    for i, (images, labels) in enumerate(train_loader):
        # Reshape images to (batch_size, input_size)
        images = images.view(-1, 28*28)   
        #Variables to wrap tensor so we can now easily auto compute the gradients
        labels = Variable(2*(labels.float()-0.5))
        
        # Forward pass and Apply Logistic Loss
        outputs = logistic_model(images)               
        loss = criterion(outputs, labels)    
        
        # Backward, set Zero Gradients and optimize
        log_optimizer.zero_grad()
        loss.backward()
        log_optimizer.step()   

        total_batches += 1     
        batch_loss += loss.item()
    #Print each epoch and its average loss
    avg_loss_epoch = batch_loss/total_batches
    print ('Epoch [{}/{}], Averge Loss:for epoch[{}, {:.4f}]' 
                   .format(epoch+1, num_epochs, epoch+1, avg_loss_epoch ))
   

# 6. Test the model

correct = 0.
total = 0.
for images, labels in test_loader:
    images = images.reshape(-1, 28*28)

    pred=torch.sigmoid(logistic_model(images))
    
    pred[pred>0.5]=1
    pred[pred<0.5]=0
    
    correct += (pred.view(-1).long()== labels).sum()
    total += images.shape[0]
print('Accuracy of the model with only SGD optimizer on the test images: %f %%' % (100 * (correct.float() / total)))
print("the learning rate is ", learning_rate)

#Logistic regression model and Loss Function using Logistic Regression Loss formula 
# ** SGD + Momentum Optimizer ** 
# 1. Define Model Class for Logistic Regression
class LogisticRegression(torch.nn.Module):
    def __init__(self, input_size, num_classes):
        super(LogisticRegression, self).__init__()
        self.linear = torch.nn.Linear(input_size, num_classes)

    def forward(self, x):
        outputs = self.linear(x)
        return outputs

# 2. Define Model Class for Logsitic Loss function
class Logistic_Loss(nn.modules.Module):    
    def __init__(self):
        super(Logistic_Loss,self).__init__()
    def forward(self, outputs, labels):
        batch_size = outputs.size()[0]
        return torch.sum(torch.log(1 + torch.exp(-(outputs.t()*labels))))/batch_size
# 3. Apply Logistic Regression function to model
logistic_model = LogisticRegression(input_size, num_classes)

# 4. Custom Loss criteria and SGD + Momentum optimizer
criterion = Logistic_Loss()

log_optimizer = torch.optim.SGD(logistic_model.parameters(), lr=learning_rate, momentum= momentum)
total_step = len(train_loader)

# 5. Train the model

for epoch in range(num_epochs):
    avg_loss_epoch = 0
    batch_loss = 0
    total_batches = 0

    for i, (images, labels) in enumerate(train_loader):
        # Reshape images to (batch_size, input_size)
        images = images.view(-1, 28*28)   
        #Variables to wrap tensor so we can now easily auto compute the gradients
        labels = Variable(2*(labels.float()-0.5))
        
        # Forward pass and Apply Logistic Loss
        outputs = logistic_model(images)               
        loss = criterion(outputs, labels)    
        
        # Backward, set Zero Gradients and optimize
        log_optimizer.zero_grad()
        loss.backward()
        log_optimizer.step()   

        total_batches += 1     
        batch_loss += loss.item()
    #Print each epoch and its average loss
    avg_loss_epoch = batch_loss/total_batches
    print ('Epoch [{}/{}], Averge Loss:for epoch[{}, {:.4f}]' 
                   .format(epoch+1, num_epochs, epoch+1, avg_loss_epoch ))
   

# 6. Test the model

correct = 0.
total = 0.
for images, labels in test_loader:
    images = images.reshape(-1, 28*28)

    pred=torch.sigmoid(logistic_model(images))
    
    pred[pred>0.5]=1
    pred[pred<0.5]=0
    
    correct += (pred.view(-1).long()== labels).sum()
    total += images.shape[0]
print('Accuracy of the model with SGD + Momentum Optimizer on the test images: %f %%' % (100 * (correct.float() / total)))
print("the learning rate is ", learning_rate)
print( "the momentum is", momentum)

"""### ***Linear SVM***"""

#Logistic regression model and Loss Function using Linear Support Vector Machines Hinge Loss
# ** only SGD no momentum Optimizer ** 
# 1. Apply Logsitic Regression function to SVM model  
svm_model = LogisticRegression(input_size,num_classes)

# 2. Define Model Class for Logstici Loss function
class SVM_Loss(nn.modules.Module):    
    def __init__(self):
        super(SVM_Loss,self).__init__()
    def forward(self, outputs, labels):
         return torch.sum(torch.clamp(1 - outputs.t()*labels, min=0))/batch_size

# 3. Custom Loss criteria and SGD + Momentum optimizer
svm_loss_criteria = SVM_Loss()

svm_optimizer = torch.optim.SGD(svm_model.parameters(), lr=learning_rate)
total_step = len(train_loader)

# 4. Train the SVM model
for epoch in range(num_epochs):
    avg_loss_epoch = 0
    batch_loss = 0
    total_batches = 0
    for i, (images, labels) in enumerate(train_loader):
        # Reshape images to (batch_size, input_size)
        images = images.view(-1, 28*28)                      
        labels = Variable(2*(labels.float()-0.5))
                
        # Forward pass and Apply SVM Loss     
        outputs = svm_model(images)           
        loss_svm = svm_loss_criteria(outputs, labels)    
       
        # Backward and optimize
        svm_optimizer.zero_grad()
        loss_svm.backward()
        svm_optimizer.step()    
        
        total_batches += 1     
        batch_loss += loss_svm.item()

    #Print each epoch and its average loss
    avg_loss_epoch = batch_loss/total_batches
    print ('Epoch [{}/{}], Averge Loss:for epoch[{}, {:.4f}]' 
                   .format(epoch+1, num_epochs, epoch+1, avg_loss_epoch ))
        

# 5. Test the model
correct = 0.
total = 0.
for images, labels in test_loader:
    images = images.reshape(-1, 28*28)
    
    outputs = svm_model(images)    
    predicted = outputs.data >= 0
    total += labels.size(0) 
    correct += (predicted.view(-1).long() == labels).sum()    
 
print('Accuracy of the model with only SGD optimizer on the test images: %f %%' % (100 * (correct.float() / total)))
print("the learning rate is ", learning_rate)

#Logistic regression model and Loss Function using Linear Support Vector Machines Hinge Loss
# ** SGD + Momentum Optimizer ** 
# 1. Apply Logsitic Regression function to SVM model  
svm_model = LogisticRegression(input_size,num_classes)

# 2. Define Model Class for Logstici Loss function
class SVM_Loss(nn.modules.Module):    
    def __init__(self):
        super(SVM_Loss,self).__init__()
    def forward(self, outputs, labels):
         return torch.sum(torch.clamp(1 - outputs.t()*labels, min=0))/batch_size

# 3. Custom Loss criteria and SGD + Momentum optimizer
svm_loss_criteria = SVM_Loss()

svm_optimizer = torch.optim.SGD(svm_model.parameters(), lr=learning_rate, momentum=momentum)
total_step = len(train_loader)

# 4. Train the SVM model
for epoch in range(num_epochs):
    avg_loss_epoch = 0
    batch_loss = 0
    total_batches = 0
    for i, (images, labels) in enumerate(train_loader):
        # Reshape images to (batch_size, input_size)
        images = images.view(-1, 28*28)                      
        labels = Variable(2*(labels.float()-0.5))
                
        # Forward pass and Apply SVM Loss     
        outputs = svm_model(images)           
        loss_svm = svm_loss_criteria(outputs, labels)    
       
        # Backward and optimize
        svm_optimizer.zero_grad()
        loss_svm.backward()
        svm_optimizer.step()    
        
        total_batches += 1     
        batch_loss += loss_svm.item()

    #Print each epoch and its average loss
    avg_loss_epoch = batch_loss/total_batches
    print ('Epoch [{}/{}], Averge Loss:for epoch[{}, {:.4f}]' 
                   .format(epoch+1, num_epochs, epoch+1, avg_loss_epoch ))
        

# 5. Test the model
correct = 0.
total = 0.
for images, labels in test_loader:
    images = images.reshape(-1, 28*28)
    
    outputs = svm_model(images)    
    predicted = outputs.data >= 0
    total += labels.size(0) 
    correct += (predicted.view(-1).long() == labels).sum()    
 
print('Accuracy of the model with both SGD + Momentum optimizer on the test images: %f %%' % (100 * (correct.float() / total)))
print("the learning rate is ", learning_rate)
print( "the momentum is", momentum)
