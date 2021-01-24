README
## **UCLA CS260: Machine Learning HW1**

**Data**

We use MNIST digit classification dataset. Pytorch/torchvision has provide a useful dataloader to automatically download and load the data into batches. In this homework, we need two class, digit 0 and digit 1, for binary classification. We have written the data loader for you as follow. You can find it in the attached file.

**Approach** 
We are using Pytorch, in Python to approach this problem; we load the MNSIT data using Pytorch torchvision dataloader to download and extract the source data. In this file, Matplotlib is used to visualize the images of MNIST digit datasit. 

**

**HOW TO RUN**

**
(This code was written and run on MacOS which doesn're support CUDA, please install from source if CUDA is needed on your end) 
PREREQUISITES FOR PYTORCH IS FOR MAC

For other systems please view: https://pytorch.org/get-started/locally/

To run Pytorch, you have the meet the following prerequisites: 
### macOS Version[](https://pytorch.org/get-started/locally/#macos-version)

PyTorch is supported on macOS 10.10 (Yosemite) or above.

### Python[](https://pytorch.org/get-started/locally/#mac-python)

It is recommended that you use Python 3.5 or greater, which can be installed either through the Anaconda package manager (see  [below](https://pytorch.org/get-started/locally/#anaconda)),  [Homebrew](https://brew.sh/), or the  [Python website](https://www.python.org/downloads/mac-osx/).

### Package Manager[](https://pytorch.org/get-started/locally/#mac-package-manager)

To install the PyTorch binaries, you will need to use one of two supported package managers:  [Anaconda](https://www.anaconda.com/download/#macos)  or  [pip](https://pypi.org/project/pip/). Anaconda is the recommended package manager as it will provide you all of the PyTorch dependencies in one, sandboxed install, including Python.

1. Follow instructuions [above](https://pytorch.org/get-started/locally/) to install Pytorch
2. Open .py file in your preferred integrated developer environment (IDE)
3. Run import and Dataloader code to set up 
4. Run Data Size and Visualization (plt) code to view Data Images
5. Run Paratmeter Configuration code to set up for the following models
6. Logistic Regression Model and Loss Models (For Logistic Regression vs. Linear SVM) code are provided and defined
7. There are two separate optimizer setup: one with SGD only, momentum parament is not used here; another one with both SGD + Momentual methods
8. Toggle `learning_rate` or `momentum` parameter setting to see different accuracy scores for the trained models 
