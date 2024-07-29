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
        user_defined_key = choose_index(data)
        data = add_row_number(data)

        # store row_number and key in a list of tuples, put key in the first element of the tuple
        keys = list(zip(data[user_defined_key], data['row_number']))
        # get the max degree of the BTree
        t = choose_max_degree(data.shape[0])
        
        #create a BTree object
        btree = BTree(t)
        # insert the keys into the BTree
        for key in keys:
            btree.insertion(key)
        
        # print the tree
        btree.print_tree(btree.root)
        # visualize the tree
        btree.visualize()
       
        # ask user if they want to insert more keys or search for a key
        choice_search_or_insert = input("Do you want to insert more keys or search for a key? (1 to insert, 2 to search): ")
        while choice_search_or_insert not in ['1', '2']:
            choice_search_or_insert = input("Invalid choice. Do you want to insert more keys or search for a key? (1 to insert, 2 to search): ")
        if choice_search_or_insert == '1':
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
                    row_number = data['row_number'].max() + 1
                    # ask the user to input value for all the columns in the dataframe except the key column and row_number column
                    column_name = data.columns.tolist()
                    column_name.remove(user_defined_key)
                    column_name.remove('row_number')
                    values = []
                    for column in column_name:
                        value = input(f"Enter the value for {column}: ")
                        values.append(value)

                    # add the new row to the end of the dataframe
                    new_row = pd.DataFrame({user_defined_key: [new_key], 'row_number': [row_number]})
                    for i in range(len(column_name)):
                        new_row[column_name[i]] = values[i]
                    data = data.append(new_row, ignore_index=True)
                    # Display the new dataframe
                    print(data)
                    # update the keys list
                    # keys.append((new_key, row_number))
                    # insert the new key into the BTree
                    btree.insertion((new_key, row_number))
                    btree.print_tree(btree.root)
                    print('-'*50)
                    btree.visualize()
                else:
                    break
        else:
            # search for a key
            search_value = input("Enter the key you want to search: ")
            result = btree.search_key(search_value)
            if result is not None:
                node, index = result
                # convert node to a list of keys
                print(f"Key {search_value} found in node with keys: {node.keys[index]}")
            else:
                print(f"The key {key} is not found in the BTree")
            # get the row from the dataframe using the row number
            row_number = node.keys[index][1]
            row = data[data['row_number'] == row_number]
            print(row)

    if choice == 2:
        # add a flag to check if the BTree object has been created
        btree = None
        t = None
        # generate data, ask the user the column names they want to generate
        column_names = input("Enter the column names separated by comma: ")
        column_names = column_names.split(',')
        # create a dataframe with the column names
        data = pd.DataFrame(columns=column_names)
        user_defined_key = choose_index(data)
        data = add_row_number(data)
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
                if data.empty:
                    row_number = 0
                else:
                    row_number = data['row_number'].max() + 1
                # ask the user to input value for all the columns in the dataframe except the key column and row_number column
                column_name = data.columns.tolist()
                column_name.remove(user_defined_key)
                column_name.remove('row_number')
                values = []
                for column in column_name:
                    value = input(f"Enter the value for {column}: ")
                    values.append(value)
                # add the new row to the end of the dataframe
                new_row = pd.DataFrame({user_defined_key: [new_key], 'row_number': [row_number]})
                for i in range(len(column_name)):
                    new_row[column_name[i]] = values[i]
                data = data.append(new_row, ignore_index=True)
                # Display the new dataframe
                print(data)
                
                # ask the user to input the max degree of the BTree
                if t is None:
                    t = choose_max_degree(data.shape[0])
                #create a BTree object
                if btree is None:
                    btree = BTree(t)
                # insert the new key into the BTree
                btree.insertion((new_key, row_number))
                btree.print_tree(btree.root)
                btree.visualize()
            else:
                break
        
        
        

insert_driver()

