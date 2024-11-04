from flask import Flask, request, jsonify, render_template
import sys
from itertools import combinations
import pandas as pd
import time

# @author hannahgsimon
# This code assumes that items in each transaction are in numerical order.
# Duplicates in one transaction aren't accounted for in this algorithm

app = Flask(__name__, template_folder='.')

class Apriori:
    def __init__(self, transactions, min_sup):
        self.transactions = transactions
        self.min_sup = min_sup
        self.freq_itemsets = []

    def find_freq_1_itemsets(self):
        item_counts = {}
        for transaction in self.transactions:
            for item in transaction:
                if item in item_counts:
                    item_counts[item] += 1
                else:
                    item_counts[item] = 1
        return [(item,) for item, count in item_counts.items() if count >= self.min_sup] #tuple

    def apriori_gen(self, prev_freq_itemsets):
        candidates = set()
        for i in range(len(prev_freq_itemsets)):
            for j in range(i + 1, len(prev_freq_itemsets)):
                l1, l2 = prev_freq_itemsets[i], prev_freq_itemsets[j]
                if l1[:-1] == l2[:-1]:
                    candidate = tuple(sorted(set(l1).union(l2)))
                    if not self.has_infreq_subset(candidate, prev_freq_itemsets):
                        candidates.add(candidate)
        return list(candidates)

    def has_infreq_subset(self, candidate, prev_freq_itemsets):
        k_minus_1_subsets = list(combinations(candidate, len(candidate) - 1))
        for subset in k_minus_1_subsets:
            if subset not in prev_freq_itemsets:
                return True 
        return False

    def count_support(self, candidates):
        candidate_counts = {candidate: 0 for candidate in candidates}
        transactions_set = [set(transaction) for transaction in self.transactions]
        for transaction_set in transactions_set:
            for candidate in candidates:
                if set(candidate).issubset(transaction_set):
                    candidate_counts[candidate] += 1
        return candidate_counts

    def remove_freq_subsets(self, freq_itemsets_k_plus_1, freq_itemsets):
        itemsets_to_remove = set()
        for item in freq_itemsets_k_plus_1:
             k_subsets = [tuple(combination) for combination in combinations(item, len(item) - 1)]
             for subset in k_subsets:
                if subset in freq_itemsets:
                    itemsets_to_remove.add(subset)
        freq_itemsets_set = set(freq_itemsets)
        freq_itemsets_set.difference_update(itemsets_to_remove)
        return list(freq_itemsets_set)

    def run(self):
        freq_itemsets = []
        freq_k_itemsets = self.find_freq_1_itemsets()
        k = 1 #size of itemsets being considered
        while freq_k_itemsets:
            freq_itemsets.extend(freq_k_itemsets)
            candidates = self.apriori_gen(freq_k_itemsets)
            freq_k_itemsets.clear()
            if candidates:
                candidate_counts = self.count_support(candidates)
                freq_itemsets_k_plus_1 = [candidate for candidate, count in candidate_counts.items() if count >= self.min_sup]
                freq_itemsets = self.remove_freq_subsets(freq_itemsets_k_plus_1, freq_itemsets)
                freq_k_itemsets = freq_itemsets_k_plus_1
                k += 1  
        freq_itemsets = sorted(freq_itemsets, key=lambda x: (len(x), sorted(x)))
        return freq_itemsets

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/apriori', methods=['POST'])
def apriori():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'File type not supported. Please upload a CSV file.'}), 400

    try:
        rows = []
        for line in file:
            row = line.decode('utf-8').strip().split(',')
            filtered_row = [int(value) for value in row if value.strip()]
            rows.append(filtered_row)

        transactions = rows
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    min_sup = request.form.get('min_sup', type=int)

    if min_sup is None:
        return jsonify({'error': 'min_sup parameter is required'}), 400

    start_time = time.time()
    freq_itemsets = Apriori(transactions, min_sup).run()
    total_time = time.time() - start_time

    formatted_output = '{' + ' '.join(['{' + ', '.join(map(str, itemset)) + '}' for itemset in freq_itemsets]) + '}'
    
    file_name = file.filename
    num_items = len(freq_itemsets)
    output = (
        f"Data Mining Apriori Algorithm<br><br>"
        f"Input file: {file_name}<br><br>"
        f"Minimal support: {min_sup}<br><br>"
        f"{formatted_output}<br><br>"
        f"End - total items: {num_items}<br><br>"
        f"Total running time: {total_time:.6f}"
    )
    return output

if __name__ == '__main__':
    app.run(debug=True)