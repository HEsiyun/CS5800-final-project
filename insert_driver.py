from read_data import read_in_data, choose_index, sort_data, add_row_number
from b_tree_v0 import BTree, BTreeNode, choose_max_degree
import pandas as pd

    


def insert_driver():
    # ask the user whether to read in the data from a file or generate the data
    while True:
        try:
            choice = int(input("Enter 1 to read in data from a file, 2 to generate data: "))
            if choice not in [1, 2]:
                raise ValueError("Invalid choice")
            break
        except ValueError as error:
            print("Invalid value:", error)
    if choice == 1:
        data = read_in_data()
        key = choose_index(data)
        data = sort_data(data, key)
        data = add_row_number(data)

        # store row_number and key in a list of tuples, put key in the first element of the tuple
        keys = list(zip(data[key], data['row_number']))
        print(keys)
        # get the max degree of the BTree
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
        # ask user if they want to insert more keys
        while True:
            try:
                choice = input("Do you want to insert more keys? (y/n): ")
                if choice not in ['y', 'n']:
                    raise ValueError("Invalid choice")
                break
            except ValueError as error:
                print("Invalid value:", error)
    

insert_driver()

