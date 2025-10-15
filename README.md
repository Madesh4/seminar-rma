# assignment_01_fk

## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

What you need: 

1. Clone this repository to your local machine.
2. Setup up a python environment. You can use [Anaconda](https://www.anaconda.com/products/distribution) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) to create a conda environment. Alternatively, you can use [venv](https://docs.python.org/3/library/venv.html) or [virtualenv](https://virtualenv.pypa.io/en/latest/).
3. Install the required packages: `numpy`, `scipy`, `pandas`, `matplotlib`, `pytest`.
4. Install any autodiff library of your choice (e.g. `jax`, `torch`, `tensorflow`).

## Use of AI

I would discourage the use of agentic AI tools (e.g. ChatGPT, GitHub Copilot) for this assignment - the instructions are quite specific and I want you to implement the functions yourself. However, you can use AI tools to help you understand concepts or get hints on how to implement certain functions. 

## Introduction

1. Open `introduction.ipynb` to get an overview of the assignment and the provided code. Run the cells to familiarize yourself with the data and the kinematic tree structure.
2. Open `task01.ipynb` to implement utility functions for forward kinematics. Follow the instructions in the notebook to complete the tasks.
3. Open `task02.ipynb` and implement the forwards kinematics functions and visualize the skeleton. Follow the instructions in the notebook to complete the tasks.

## What needs to be done
To pass the tests, make sure that `numpy`-type arrays are allowed as inputs to your functions. For example, if you use `torch`, you can check if the input is a `numpy.ndarray` and convert it to a `torch.Tensor` at the beginning of your function.  

1. Show that all tests in `pytest tests.py` pass.
2. Explain the output in `task01.ipynb` and `task02.ipynb`, as well as the implementation of the functions you wrote.

