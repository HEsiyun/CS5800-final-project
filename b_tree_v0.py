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
    
    def has_minimum_keys(self, t: int):
        '''
        Function has_minimum_keys
        This function checks if a node contains the minimum number of keys.
        Parameters:
        node -- the node to check
        Returns True if the node contains at least t-1 keys, False otherwise
        '''
        return len(self.keys) > t-1

    def sibling_type(self, parent):
        '''
        Function sibling_type
        This function determines if the current node has a left or right sibling.
        Parameters:
        parent -- the parent node of the current node
        Returns 0 if there is a left sibling, 1 if there is a right sibling, -1 if no siblings are found
        '''
        if parent is None:
            return -1
     
        # Find the index of the current node in the parent's children list
        index = parent.child.index(self)
        
        # Check for left sibling
        if index > 0:
            return 0
        # Check for right sibling
        elif index < len(parent.child) - 1:
            return 1
        else:
            return -1

class BTree:
    '''
    class Btree
    This class represents a B tree. It has the following attributes: root and minimum degree. The class has the following methods:
    - insertion: insert a key into the B tree
    - insert_non_full: insert a key into a non-full node
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
            self.insert_non_full(self.root, k)
        else:
            self.insert_non_full(root, k)

    def insert_non_full(self, x, k):
        '''
        Function insert_non_full
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
            self.insert_non_full(x.child[i], k)

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

        # Split the keys and children of y into y and z
        right_child.keys = left_child.keys[t: (2 * t) - 1]
        left_child.keys = left_child.keys[:t - 1]

        if not left_child.leaf:
            right_child.child = left_child.child[t:]
            left_child.child = left_child.child[:t]
    
    def search_key(self, k: int, x=None, parent=None):
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
        while i < len(x.keys) and k > x.keys[i][0]:
            i += 1

        # Check if the key is found in the current node
        if i < len(x.keys) and k == x.keys[i][0]:
            return (i, x, parent)

        # If the node is a leaf, the key is not present
        if x.leaf:
            print(f"Key {k} not found in the B-tree")
            return None

        # Otherwise, move to the appropriate child node
        # Additional safe guard to prevent index out of range if i is out of bounds
        if i < len(x.child):
            return self.search_key(k, x.child[i], x)
        else:
            return None
    

    def get_parent(self, node, current=None, parent=None):
        '''
        Function get_parent
        This function finds the parent of a given node in the B-tree.
        Parameters:
        node -- the node whose parent is to be found
        current -- the current node being inspected (used for recursion, default is root)
        parent -- the parent of the current node (used for recursion, default is None)
        Returns the parent node if found, otherwise None
        '''
        if current is None:
            current = self.root
        
        if node in current.child:
            return current
        
        for child in current.child:
            if not child.leaf:
                found_parent = self.get_parent(node, child, current)
                if found_parent:
                    return found_parent
        return None

    def remove(self, k:int, x=None, parent=None):
        # A function to remove key k from the sub-tree rooted with this node
        result = self.search_key(k, x, parent)
        
        if result is None:
            print(f"The key {k} does not exist in the tree")
            return
        index, target, parent = result
        
        if target.leaf:
            print(f"Removing key {k} from leaf node")
            self.remove_from_leaf(index, target, parent)
        else:
            print(f"Removing key {k} from non-leaf node")
            self.remove_from_intetnal(index, target)


    def remove_from_leaf(self, k, node:BTreeNode, parent:BTreeNode):
        # A function to remove the k-th key from this node, which is a leaf node
        node.keys.pop(k)
        if not node.has_minimum_keys(self.t):
            print(f"Node with keys {node.keys} has less than {self.t-1} keys")
            sibling = node.sibling_type(parent)
            if sibling == 0 and parent.child[parent.child.index(node) - 1].has_minimum_keys(self.t):
                self.borrow_from_left(node, parent)
                return
                # If the left sibling has t-1 keys, merge with it
            elif sibling == 0 and not parent.child[parent.child.index(node) - 1].has_minimum_keys(self.t):
                self.merge_with_left(node, parent)
                return
            elif sibling == 1 and parent.child[parent.child.index(node) + 1].has_minimum_keys(self.t):
                self.borrow_from_right(node, parent)
                return
                # If the right sibling has t-1 keys, merge with it
            else:
                self.merge_with_right(node, parent)
                return

    def borrow_from_left(self, node, parent):
        '''
        Function borrow_from_left
        This function borrows a key from the left sibling of the node.
        Parameters:
        node -- the node to borrow a key into
        parent -- the parent node of the node
        '''
        index = parent.child.index(node)
        left_sibling = parent.child[index - 1]

        # Pass largest key from left sibling to parent
        node.keys.insert(0, parent.keys[index - 1])
        # Pass largest key from parent to node
        parent.keys[index - 1] = left_sibling.keys.pop()


    def borrow_from_right(self, node, parent):
        '''
        Function borrow_from_right
        This function borrows a key from the right sibling of the node.
        Parameters:
        node -- the node to borrow a key into
        parent -- the parent node of the node
        '''
        index = parent.child.index(node)
        right_sibling = parent.child[index + 1]

        # Pass smallest key from right sibling to parent
        node.keys.append(parent.keys[index])
        # Pass largest key from parent to node
        parent.keys[index] = right_sibling.keys.pop(0)


    def merge_with_left(self, node, parent):
        '''
        Function merge_with_left
        This function merges the node with its left sibling.
        Parameters:
        node -- the node to merge with its left sibling
        parent -- the parent node of the node
        '''
        index = parent.child.index(node)
        left_sibling = parent.child[index - 1]

        # Pass the key from parent to left sibling
        left_sibling.keys.append(parent.keys.pop(index - 1))
        print(left_sibling.keys)

        # Merge the keys and children from node to left sibling
        left_sibling.keys.extend(node.keys)
        print(left_sibling.keys)
        if not node.leaf:
            left_sibling.child.extend(node.child)

        # Remove the merged node from parent's children
        parent.child.pop(index)
        if not parent.has_minimum_keys(self.t):
            print(f"Parent with keys {parent.keys} has less than {self.t-1} keys")
            self.borrow_from_leaf_when_parent_sibling_all_have_minimal_keys(parent)
        

    def merge_with_right(self, node, parent):
        '''
        Function merge_with_right
        This function merges the node with its right sibling.
        Parameters:
        node -- the node to merge with its right sibling
        parent -- the parent node of the node
        '''
        
        index = parent.child.index(node)
        right_sibling = parent.child[index + 1]

        # Pass the key from parent to node
        node.keys.append(parent.keys.pop(index))

        # Merge the keys and children from right sibling to node
        node.keys.extend(right_sibling.keys)
        if not node.leaf:
            node.child.extend(right_sibling.child)

        # Remove the merged node from parent's children
        parent.child.pop(index + 1)
        if not parent.has_minimum_keys(self.t):
            print(f"Parent with keys {parent.keys} has less than {self.t-1} keys")
            self.borrow_from_leaf_when_parent_sibling_all_have_minimal_keys(parent)

    def borrow_from_leaf_when_parent_sibling_all_have_minimal_keys(self, parent:BTreeNode):
        '''
        Function borrow_from_leaf_when_parent_sibling_all_have_minimal_keys
        This function handles the case where both the parent and siblings have minimal keys by recursively
        finding a node with more than minimal keys.
        Parameters:
        k -- the key to remove
        node -- the current node (leaf) from which the key is to be removed
        parent -- the parent node of the current node
        '''
        grandparent = None
        current_node = parent
        current_parent = None

        # Traverse up the tree to find a suitable node with more than minimal keys
        while current_node is not None and current_node.has_minimum_keys(self.t):
            current_parent = self.get_parent(current_node)
            grandparent = current_node
            current_node = current_parent

        # If a suitable node is found, borrow from it
        if current_node is not None and not current_node.has_minimum_keys(self.t):
            if current_parent is not None:
                sibling_type = grandparent.sibling_type(current_parent)
                if sibling_type == 0:
                    self.borrow_from_left(grandparent, current_parent)              

    def remove_from_intetnal(self, k:int, node:BTreeNode):
        # A function to remove the index-th key from this node, which is a non-leaf node
        node.keys.pop(k)
        left_child = node.child[k]
        right_child = node.child[k + 1]

        if left_child.has_minimum_keys(self.t):
            self.borrow_from_left_predecessor(k, node)
        elif right_child.has_minimum_keys(self.t):
            self.borrow_from_right_successor(k, node)
        else:
            self.merge_two_children(k, node)
            self.borrow_from_leaf_when_parent_sibling_all_have_minimal_keys(node)


    def borrow_from_left_predecessor(self, k, node:BTreeNode):
        # A function to borrow the predecessor of the key from the left child of the key
        left_child = node.child[k]
        predecessor = left_child.keys[-1]
        
        # Move the key down from the node to the right child
        node.child[k + 1].keys.insert(0, node.keys[k])
        # Move the predecessor up to the node
        node.keys[k] = predecessor
        
        # Remove the predecessor from the left child
        left_child.keys.pop()
    
    def borrow_from_right_successor(self, k, node):
        '''
        A function to borrow the successor of the key from the right child of the key.
        '''
        right_child = node.child[k + 1]
        successor = right_child.keys[0]
        
        # Move the key down from the node to the left child
        node.child[k].keys.append(node.keys[k])
        # Move the successor up to the node
        node.keys[k] = successor
        
        # Remove the successor from the right child
        right_child.keys.pop(0)

    def merge_two_children(self, k, node):
        '''
        A function to merge the children of the node.
        '''
        left_child = node.child[k]
        right_child = node.child[k + 1]
        
        # Append the key from the node to the left child
        #left_child.keys.append(node.keys[k])
        
        # Merge the keys from the right child to the left child
        left_child.keys.extend(right_child.keys)
        # if not right_child.leaf:
        #     left_child.child.extend(right_child.child)

        # # Remove the key and right child from the node
        # node.keys.pop(k)
        node.child.pop(k + 1)
    

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
        
    
    B.print_tree(B.root)
    # Search for the specific key
    # search_value = 10
    # search_key = (search_value)  # Ensure you're searching for the entire tuple
    # result = B.search_key(search_key)
    # if result is not None:
    #     index, node, parent = result
    #     #found_key = node.keys[index]  # Get only the specific key
    #     # print(f"Key {search_key} found at index {index} with data: {found_key}")
    #     print(f"Key {search_key} found in node with keys: {node.keys[index]} at index {index}, parent is {parent.keys}")
    # else:
    #     print(f"Key {search_key} not found in the B-tree.")

    # B.remove(30)
    # B.print_tree(B.root)
    # print('-' * 50)
    # B.remove(31)
    # B.print_tree(B.root)
    # print('-' * 50)
    # B.remove(33)
    # B.print_tree(B.root)
    # B.remove(34)
    # B.print_tree(B.root)
    # B.remove(18)
    # B.print_tree(B.root)
    # B.remove(24)
    # B.print_tree(B.root)
    # B.remove(25)
    # B.print_tree(B.root)
    # B.remove(32)
    # B.print_tree(B.root)
    # B.remove(29)
    # B.print_tree(B.root)
    # B.remove(28)
    # B.print_tree(B.root)
    # B.remove(27)
    # B.print_tree(B.root)
    # B.remove(0)
    # B.print_tree(B.root)
    # B.remove(4)
    # B.print_tree(B.root)
    # B.remove(13)
    # B.print_tree(B.root)
    


    B.remove(68)

    B.print_tree(B.root)
    index, key, parent = B.search_key(77)
    print("Key found: ", key.keys[index])
    
    B.print_tree(B.root)
    
    #B.remove(3)
    #B.remove(26)
    #B.print_tree(B.root)

if __name__ == '__main__':
    main()
