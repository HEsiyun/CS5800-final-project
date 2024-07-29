from read_data import read_in_data, choose_index, add_row_number
from b_tree_v0 import BTree, BTreeNode, choose_max_degree
import pandas as pd

def search_driver(data, btree):
    '''
    Function search_driver
    This function searches for a key in the BTree and displays the row in the dataframe that contains the key.
    Parameters:
    data -- the dataframe of the data
    btree -- the BTree object
    '''
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

def import_driver():
    '''
    Function import_driver
    This function imports the data from a file and creates a BTree object.
    Returns the dataframe of the data, the BTree object, and the user defined key.
    '''
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
    return data, btree, user_defined_key

def insert_driver(data, user_defined_key):
    '''
    Function insert_driver
    This function inserts a new row into the dataframe and the BTree.
    Parameters:
    data -- the dataframe of the data
    user_defined_key -- the user defined key
    Returns the updated dataframe, the new key, and the row number.
    '''
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
    return data, new_key, row_number

def mini_database():
    ''' 
    Function mini_database
    This function is the main function that runs the mini database.
    '''
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
        data, btree, user_defined_key = import_driver()
       
        # ask user if they want to insert, search, update, delete or exit
        while True:
            try:
                crud_choice = input("Do you want to insert, search, update, delete or exit? (1 to insert, 2 to search, 3 to delete, 4 to exit): ")
                if crud_choice not in ['1', '2', '3', '4', '5']:
                    raise ValueError("Invalid choice")
            except ValueError as error:
                print("Invalid value:", error)

            if crud_choice == '1':
                data, new_key, row_number = insert_driver(data, user_defined_key)
                # Display the new dataframe
                print(data)
                # insert the new key into the BTree
                btree.insertion((new_key, row_number))
                btree.print_tree(btree.root)
                print('-'*50)
                btree.visualize()
            elif crud_choice == '2':
                # ask the user if they want to search for a key
                search_driver(data, btree)
            elif crud_choice == '3':
                # delete_driver(data, btree)
                pass
            else:
                break

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
        # ask user if they want to insert, search, update, delete or exit
        while True:
            try:
                crud_choice = input("Do you want to insert, search, update, delete or exit? (1 to insert, 2 to search, 3 to delete, 4 to exit): ")
            except ValueError as error:
                print("Invalid value:", error)

            if crud_choice == '1':
                data, new_key, row_number = insert_driver(data, user_defined_key)
                #Display the new dataframe
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
            elif crud_choice == '2':
                # ask the user if they want to search for a key
                search_driver(data, btree)
            elif crud_choice == '3':
                # delete_driver(data, btree)
                pass
            else:
                break
            
mini_database()