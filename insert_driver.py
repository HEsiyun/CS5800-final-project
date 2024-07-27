from read_data import read_in_data, choose_index, sort_data, add_row_number
from insert import BTree, BTreeNode, choose_max_degree
import pandas as pd

def main():
    data = read_in_data()
    key = choose_index(data)
    data = sort_data(data, key)
    data = add_row_number(data)
    # store row_number and key in a list of tuples
    keys = list(zip(data['row_number'], data[key]))
   #print(type(keys))
    
    t = choose_max_degree(data.shape[0])
    
    #create a BTree object
    btree = BTree(t)
    # insert the keys into the BTree
    for key in keys:
        btree.insertion(key)
        # print the tree
        btree.print_tree(btree.root)
        print('-'*50)
    # visualize the tree
    btree.visualize()


if __name__ == "__main__":
    main()