from read_data import read_in_data, choose_index, sort_data, add_row_number
from insert import BTree, BTreeNode
import pandas as pd

def main():
    data = read_in_data()
    key = choose_index(data)
    data = sort_data(data, key)
    data = add_row_number(data)
    #print(data)
    # store row_number and key in a list of tuples
    keys = list(zip(data['row_number'], data[key]))
    print(keys)

if __name__ == "__main__":
    main()