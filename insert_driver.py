from read_data import read_in_data, choose_index, add_row_number
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
        #data = sort_data(data, key)
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
            except ValueError as error:
                print("Invalid value:", error)

            #choice equals 'y'
            if choice == 'y':
                new_key = input("Enter the key you want to insert: ")
                # set the row number to be the last row number + 1
                # row_number = data['row_number'].max() + 1
                # add the key to the dataframe
                # check if the key is unique
                if new_key in data[key].values:
                    print("Key already exists in the dataframe")
                    continue
                # ask the user to input value for all the columns in the dataframe other than the key column
                column_name = data.columns.tolist()
                #column_name.remove(key)
                values = []
                for column in column_name:
                    value = input(f"Enter the value for {column}: ")
                    values.append(value)

                # add the new row to the end of the dataframe
                new_row = pd.DataFrame({key: [key], 'row_number': [row_number]})
                for i in range(len(column_name)):
                    new_row[column_name[i]] = values[i]
                data = data.append(new_row, ignore_index=True)
                # Display the new dataframe
                print(data)
                # update the keys list
                keys.append((key, row_number))
                # insert the new key into the BTree
                # btree.insertion((key, row_number))
                # btree.print_tree(btree.root)
                # print('-'*50)
                # btree.visualize()
            else:
                break


    

insert_driver()

