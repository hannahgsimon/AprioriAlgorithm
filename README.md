# Apriori Algorithm Implementation

## Overview
- The Apriori algorithm is a classic algorithm used in data mining for extracting frequent itemsets from large datasets. It operates under the principle of "bottom-up" generation, where it generates candidate itemsets from the frequent itemsets found in the previous iteration. This code is designed to analyze a CSV file containing data and identify itemsets that meet a specified minimum support threshold.
- This README focuses on the command-line version from the last commit on 11/03/2024. The latest commit introduces a Flask web application that implements the same functionality.

## Requirements
- Python 3.x
- Standard Python libraries: `itertools`, `sys`

## Usage
1. Prepare your dataset in a CSV file format. Each row should represent a numerical data entry, with each item in a separate cell. The first column is ignored, and only the subsequent columns are processed as items. This program assumes that items are in ascending numerical order within each row, and ignores duplicates within a single row.
2. Run the script with the CSV `file_name` and the desired minimum support threshold `min_sup` passed as command-line arguments..
   ```bash
   python3 apriori-algorithm.py 1000-out1.csv 20

## Output
The program generates the following output to the command terminal: 
- File Run: `file_name`
- Minimum Support: `min_sup`
- List of frequent itemsets
- Number of frequent itemsets

## Author
Hannah G. Simon is the sole developer of this Apriori algorithm implementation.
