# Description

This project uses a foundation model and supervised learning to estimate the difficulty of a hiking based on its satellite image.

***

# Usage

## Step 1

You will first have to download the dataset on kaggle : https://www.kaggle.com/datasets/roccoli/gpx-hike-tracks/data
This dataset is tabular but still quite large.

## Step 2

`clone` this repository and add your dataset `.csv` to it. 

## Step 3

Launch the notebook `hiking.ipynb`. It will create a `hikes.json` file from `.csv` dataset

## Step 4

Launch the `setup.py` file in order to extract every satellite image from the dataset.
This step takes a large amount of time because it will manually take a screenshot of every hike and save it into a "screenshots" folder

## Step 5

Launch the `setup-2.py` to organize every screenshot according to its difficulty

## Step 6

Launch the `estimate.py` to train the AI to estimate the difficulty ...
