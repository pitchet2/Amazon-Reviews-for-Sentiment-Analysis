# Spacy classification template

This template is a automated pipeline for the following steps:

- Convert: converting data into Spacy format
- Training: training Spacy model
- Evaluate: evaluation of the trained Spacy model
- Register: register the trained Spacy model to AzureML

## Instructions

In order to use the template in Azure Machine Learning Platform, you should follow the steps below.

## Prerequisites

You must fulfill the following requirements for the target environment:

- Run setup.sh to install all the dependencies

## Prepare project

### Training Data

Training data needs to be in csv format with 2 columns:

- **Features** column: Containing the texts which need to be classified
- **Labels** column: Containing the label for each of the text

Put the training data into the **data** folder.

Note: Please rename two columns so they do not have any space in the column name.

### Choose Spacy model

There are 2 Spacy models within this template:

- textcat_multilabel: predicting multiple label from output, suited for multilabel classification
- textcat_singlelabel: predicting a single label from output, suited for binary classification

### Update project.yaml

After choosing the model, open the model folder and find project.yaml

The following fields need to be updated within project.yaml under **vars**:

- csv: Replace with the Training data csv file name
- model_name: Replace with model name to be registered in AzureML
- feature_column: Replace with the name of feature column in training data csv file
- label_column: Replace with the name of label column in training data csv file

![project_yml](.md_resources/project_yml.png)

### Run project

Go back to the **Spacy_classification_template** folder and open **notebooks** folder. There are 2 shell scripts for each of the Spacy model:

- run_project_multilabel.sh
- run_project_singlelabel.sh

Run the shell script for the model you selected and updated the **project.yml**

### Results

The model will be automatically registered to AzureML. A notebook template **spacy_model_prediction.ipynb** can be found under **Spacy_classification_template** folder. Update this notebook for users.

## Any Doubts?

Contact me: [hdu@riskalive.com](mailto:hdu@riskalive.com)
