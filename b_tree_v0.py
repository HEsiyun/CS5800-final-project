import matplotlib.pyplot as plt
import networkx as nx

def choose_max_degree(df_length: int) -> int:
    '''
    Function choose_max_degree
    This function takes the length of the dataframe and prompts the user to enter the maximum degree of the B tree.
    Let the user choose the maximum degree of the B tree. The minimum degree is half of the maximum degree. The maximum degree must be an even number larger than 3.
    Parameters:
    df_length -- the length of the dataframe
    Returns the minimum degree of the B tree.
    '''
    while True:
        try:
            max_degree = int(input("Enter the maximum degree of the B tree, please choose an even number larger than 3: "))
            if max_degree < 4:
                raise ValueError("Degree must be greater than 3")
            return int(max_degree / 2) # Convert to minimum degree
            # if the max_degree is not even, raise an error
            if max_degree % 2 != 0:
                raise ValueError("Degree must be an even number")
        except ValueError as error:
            print("Invalid value:", error)

# B tree node class
# Even max degree only
class BTreeNode:
    '''
    Class BTreeNode
    This class represents a node in the B tree.
    '''
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []  # This will store tuples
        self.child = []

class BTree:
    '''
    class Btree
    This class represents a B tree. It has the following attributes: root and minimum degree. The class has the following methods:
    - insertion: insert a key into the B tree
    - insert_none_full: insert a key into a non-full node
    - split_child: split a child node
    - search_key: search for a key in the B tree
    - print_tree: print the B tree
    - visualize: visualize the B tree
    '''
    def __init__(self, t):
        self.root = BTreeNode(True)  # Initially, root should be a leaf
        self.t = t  # Minimum degree

    def insertion(self, k):
        '''
        Function insertion
        This function inserts a key into the B tree.
        Parameters:
        k -- the key to be inserted
        '''
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:  # If root is full, split it
            temp = BTreeNode(False)
            temp.child.insert(0, self.root)
            self.split_child(temp, 0)
            self.root = temp  # Update root
            self.insert_none_full(self.root, k)
        else:
            self.insert_none_full(root, k)

    def insert_none_full(self, x, k):
        '''
        Function insert_none_full
        This function inserts a key into a non-full node.
        Parameters:
        x -- the node to insert the key
        k -- the key to be inserted
        '''
        i = 0  # Start from the beginning of the keys list

        if x.leaf:
            # Find the position to insert the new key
            while i < len(x.keys) and k > x.keys[i]:
                i += 1
            x.keys.insert(i, k)  # Insert the key at the found position
        else:
            # Find the child which is going to have the new key
            while i < len(x.keys) and k > x.keys[i]:
                i += 1

            # Split the child if it is full
            if len(x.child[i].keys) == (2 * self.t) - 1:
                self.split_child(x, i)
                # After splitting, the middle key of x.child[i] moves up and is now at x.keys[i]
                # We need to decide whether to insert k to the left or right of this middle key
                if k > x.keys[i]:
                    i += 1

            # Recursively insert the key in the child node
            self.insert_none_full(x.child[i], k)

    def split_child(self, x, i):
        '''
        Function split_child
        This function splits a child node.
        Parameters:
        x -- the parent node
        i -- the index of the child to split
        '''
        t = self.t
        left_child = x.child[i]
        right_child = BTreeNode(left_child.leaf)
        
        x.child.insert(i + 1, right_child)
        x.keys.insert(i, left_child.keys[t - 1])

        right_child.keys = left_child.keys[t: (2 * t) - 1]
        left_child.keys = left_child.keys[:t - 1]

        if not left_child.leaf:
            right_child.child = left_child.child[t:]
            left_child.child = left_child.child[:t]
    
    def searching(self, k, x=None):
        '''
        Function search_key
        This function searches for a key in the B tree.
        Parameters:
        k -- the key to search
        x -- the node to start the search from
        Returns the node and index of the key if found, otherwise None.
        '''
        if x is None:
            x = self.root  # Start from the root if no node is provided
        i = 0
        # Navigate through the keys of the node to find the possible location of the key
        # Make sure k[0] is compared with x.keys[i][0] since both are tuples
        while i < len(x.keys) and k > x.keys[i][0]:
            i += 1
        # Check if the key is found in the current node
        if i < len(x.keys) and k == x.keys[i][0]:
            return (x, i)
        elif x.leaf:  # If reached a leaf node, the key is not present
            return None
        else:  # Otherwise, move to the appropriate child node
            return self.searching(k, x.child[i])

    def delete(self, k, x=None):
        '''
        Function delete
        This function deletes a key from the B tree.
        Parameters:
        k -- the key to delete
        x -- the node to start the deletion from     
        '''

        if not x:
            x = self.root
        t = self.t
        # Find the index of the key or the child which should have the key
        result = self.searching(k, x) 
        if result:
            x, i = result
        else:
            print(f"Key {k} not found in the B-tree")
            return

        if x.leaf:
            # If the key is in a leaf node and matches, remove it directly
            x.keys.pop(i)
            return
        # Key is not in leaf, handle internal node case
        if len(x.child[i].keys) >= t:
            
            x.keys[i] = self.delete_predecessor(x.child[i])
        elif len(x.child[i + 1].keys) >= t:
            x.keys[i] = self.delete_successor(x.child[i + 1])
        else:
            self.merge_nodes(x, i)
            
            # After merging, the key count decreases, continue deletion on the merged node
            if i < len(x.child):
                self.delete(k, x.child[i])


    def delete_predecessor(self, x):
        '''
        Function delete_predecessor
        This function follows the left subtree until the rightmost key
            is found (predecessor), and removes the predecessor
            ensuring the node meets the B-tree properties.
        Parameters:
        x -- the node to start from
        '''
        if x.leaf:
            return x.keys.pop()

    # Recursive case: Ensure the last child has enough keys, rebalance if necessary
        if len(x.child[-1].keys) < self.t:
            self.rebalance_before_delete(x, len(x.child) - 1)

        # Recur on the last child
        return self.delete_predecessor(x.child[-1])

    def delete_successor(self, x):
        """
        Follows the right subtree until the leftmost key is found (successor),
        and removes the successor, ensuring the node meets the B-tree properties.
        """
        # Traverse until a leaf is found
        if x.leaf:
            return x.keys.pop(0)
    # Recursive case: Ensure the first child has enough keys, rebalance if necessary
        if len(x.child[0].keys) < self.t:
            self.rebalance_before_delete(x, 0)

        # Recur on the first child
        return self.delete_successor(x.child[0])

    def rebalance_before_delete(self, x, idx):
        '''
        Function rebalance_before_delete
        This function rebalances the node before deletion.
        Parameters:
        x -- the parent node
        idx -- the index of the child node to rebalance
        '''
        if idx > 0:
            self.merge_nodes(x, idx - 1)
        else:
            self.merge_nodes(x, idx)

    def merge_nodes(self, x, idx):
        '''
        Function merge_nodes
        This function merges the node with its sibling.
        Parameters:
        x -- the parent node
        idx -- the index of the child node to merge
        '''
        left_child = x.child[idx]
        right_child = x.child[idx + 1]
        left_child.keys.append(x.keys.pop(idx))
        left_child.keys.extend(right_child.keys)
        if not left_child.leaf:
            left_child.child.extend(right_child.child)
        x.child.pop(idx + 1)
    
    # Print the tree
    def print_tree(self, x, l=0, prefix=""):
        '''
        Function print_tree
        This function prints the B tree.
        Parameters:
        x -- the node to start printing from
        l -- the level of the node
        prefix -- the prefix to print before the node
        '''
        if l == 0:
            print("Root:", end=" ")
        else:
            print(prefix + "Level " + str(l) + ":", end=" ")

        # Print the current node's keys
        print("[", end="")
        for i, key in enumerate(x.keys):
            print(key, end="")
            if i < len(x.keys) - 1:
                print(", ", end="")
        print("]")

        # Recursively print child nodes with an updated prefix
        if not x.leaf:
            for i, child in enumerate(x.child):
                child_prefix = prefix + " " * (12 + l * 4)  # Adjust spacing based on level
                self.print_tree(child, l + 1, child_prefix)

    def visualize(self):
        '''
        Function visualize
        This function visualizes the B tree.
        '''
        def add_edges(graph, node, pos, x=0, y=0, level=1, width=1.0):
            if node is not None:
                pos[node] = (x, y)
                if not node.leaf:
                    dx = width / len(node.child)  # Width divided by the number of children
                    next_x = x - width / 2 + dx / 2  # Centering children under the parent node
                    for child in node.child:
                        graph.add_edge(node, child)
                        add_edges(graph, child, pos, x=next_x, y=y-2, level=level+1, width=dx)  # Pass the new width to the next level
                        next_x += dx

        graph = nx.DiGraph()
        pos = {}
        add_edges(graph, self.root, pos)

        fig, ax = plt.subplots(figsize=(12, 8))
        nx.draw(graph, pos, ax=ax, with_labels=False, node_size=3, arrowsize=20)

        # Draw node labels with each key on a new line
        for node, (x, y) in pos.items():
            label = '\n'.join(str(key) for key in node.keys)
            ax.text(x, y, label, fontsize=12, ha='center', va='center',
                    bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='round,pad=0.2'))  # Changed facecolor to 'lightgray'

        plt.show()


def main():
    B = BTree(3)
    
    for i in range(80):
        B.insertion((i, "o"))
    print("construction done")
    B.print_tree(B.root)
    # for i in range(10):
    #     print(f"Deleting {i}")
    
    B.delete(53)
    
    B.print_tree(B.root)
    B.delete(44)
    B.print_tree(B.root)
    
    # for i in range(61, 200):
    #     B.insertion((i, "o"))
    # B.insertion((1, "o"))
    # B.insertion((20, "o"))
    # B.insertion((21, "o"))
    
    # print("deletion done")
    # B.print_tree(B.root)
    # for i in range(25):        
    #     B.insertion((i, "o"))
    # B.print_tree(B.root)
       
        
    

    # Search for the specific key
    # search_value = 11
    # result = B.searching(search_value)
    # if result is not None:
    #     node, index = result
    #     print(f"Key {search_value} found in node with keys: {node.keys[index]} at index {index}")
    # else:
    #     print(f"Key {search_value} not found in the B-tree.")

    # for i in range(100):
    #     print(f"Deleting {i}")
    #     B.delete(i)
    #     B.print_tree(B.root)
    # for i in range(100):
    #     B.insertion((i, "o"))
    #     print(f"Inserting {i}")
    #     B.print_tree(B.root)

if __name__ == '__main__':
    main()