# Apriori Algorithm Implementation

This repository contains an implementation of the Apriori algorithm for finding frequent itemsets in dataset files. The code is designed to analyze a CSV file containing data and identify itemsets that meet a specified minimum support threshold.

## Author
Hannah G. Simon

## Overview

The Apriori algorithm is a classic algorithm used in data mining for extracting frequent itemsets from large datasets. It operates under the principle of "bottom-up" generation, where it generates candidate itemsets from the frequent itemsets found in the previous iteration.

### Features
- Identifies frequent itemsets from data in CSV format.
- Assumes items are in numerical order within each row.
- Ignores duplicates within a single row.

## Requirements
- Python 3.x
- Standard libraries: `itertools`, `sys`

## Usage

1. Prepare your dataset in a CSV file format. Each row should represent a data entry, with each item in a separate cell. The first column is ignored, and only the subsequent columns are processed as items.

2. Update the `file_name` variable in the code to point to your CSV file.

3. Adjust the `min_sup` variable to set your desired minimum support threshold.

4. Run the script:
   ```bash
   python apriori.py
