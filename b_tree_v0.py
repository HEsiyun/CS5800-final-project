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
        # Make sure k[0] is compared with x.keys[i][0] since both are tuples
        while i < len(x.keys) and k > x.keys[i][0]:
            i += 1
        # Check if the key is found in the current node
        if i < len(x.keys) and k == x.keys[i][0]:
            return (i, x, parent)
        elif x.leaf:  # If reached a leaf node, the key is not present
            return None
        else:  # Otherwise, move to the appropriate child node
            return self.search_key(k, x.child[i], x)

    def remove(self, k:int, x=None, parent=None):
        # A function to remove key k from the sub-tree rooted with this node
        result = self.search_key(k, x, parent)
        
        if result is None:
            print(f"The key {k} does not exist in the tree")
            return
        index, target, parent = result
        
        if target.leaf:
            print(f"Removing key {k} from leaf node")
            self.remove_from_leaf(index, target)
        else:
            print(f"Removing key {k} from non-leaf node")
            self.remove_from_non_leaf(index, target)

    def remove_from_leaf(self, k, node):
        # A function to remove the k-th key from this node, which is a leaf node
        if not node.has_minimum_keys(self.t):
            print("This remove is illegal")
            return
        node.keys.pop(k)

    def remove_from_non_leaf(self, index):
        # A function to remove the index-th key from this node, which is a non-leaf node
        k = self.keys[index]

        if self.C[index].n >= self.t:
            pred = self.get_pred(index)
            self.keys[index] = pred
            self.C[index].remove(pred)
        elif self.C[index + 1].n >= self.t:
            succ = self.get_succ(index)
            self.keys[index] = succ
            self.C[index + 1].remove(succ)
        else:
            self.merge(index)
            self.C[index].remove(k)

    
    def get_pred(self, index):
        # A function to get the predecessor of the key at the index-th position in the node
        cur = self.C[index]
        while not cur.leaf:
            cur = cur.C[cur.n]

        return cur.keys[cur.n - 1]

    def get_succ(self, index):
        # A function to get the successor of the key at the index-th position in the node
        cur = self.C[index + 1]
        while not cur.leaf:
            cur = cur.C[0]

        return cur.keys[0]

    def fill(self, index):
        # A function to fill child C[index] which has fewer than t-1 keys
        if index != 0 and self.C[index - 1].n >= self.t:
            self.borrow_from_prev(index)
        elif index != self.n and self.C[index + 1].n >= self.t:
            self.borrow_from_next(index)
        else:
            if index != self.n:
                self.merge(index)
            else:
                self.merge(index - 1)

    def borrow_from_prev(self, index):
        # A function to borrow a key from C[index-1] and insert it into C[index]
        child, sibling = self.C[index], self.C[index - 1]

        for i in range(child.n - 1, -1, -1):
            child.keys[i + 1] = child.keys[i]

        if not child.leaf:
            for i in range(child.n, -1, -1):
                child.C[i + 1] = child.C[i]

        child.keys[0] = self.keys[index - 1]

        if not child.leaf:
            child.C[0] = sibling.C[sibling.n]

        self.keys[index - 1] = sibling.keys[sibling.n - 1]

        child.n += 1
        sibling.n -= 1

    def borrow_from_next(self, index):
        # A function to borrow a key from C[index+1] and place it in C[index]
        child, sibling = self.C[index], self.C[index + 1]

        child.keys[child.n] = self.keys[index]

        if not child.leaf:
            child.C[child.n + 1] = sibling.C[0]

        self.keys[index] = sibling.keys[0]

        for i in range(1, sibling.n):
            sibling.keys[i - 1] = sibling.keys[i]

        if not sibling.leaf:
            for i in range(1, sibling.n + 1):
                sibling.C[i - 1] = sibling.C[i]

        child.n += 1
        sibling.n -= 1

    def merge(self, index):
        # A function to merge C[index] with C[index+1]
        child, sibling = self.C[index], self.C[index + 1]

        child.keys[self.t - 1] = self.keys[index]

        for i in range(sibling.n):
            child.keys[i + self.t] = sibling.keys[i]

        if not child.leaf:
            for i in range(sibling.n + 1):
                child.C[i + self.t] = sibling.C[i]

        for i in range(index + 1, self.n):
            self.keys[i - 1] = self.keys[i]

        for i in range(index + 2, self.n + 1):
            self.C[i - 1] = self.C[i]

        child.n += sibling.n + 1
        self.n -= 1

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
    B = BTree(2)

    for i in range(30):
        B.insertion((i, 2 * i))
        
        print('-' * 50)
    B.print_tree(B.root)
    # Search for the specific key
    search_value = 29
    search_key = (search_value)  # Ensure you're searching for the entire tuple
    result = B.search_key(search_key)
    if result is not None:
        index, node, parent = result
        #found_key = node.keys[index]  # Get only the specific key
        # print(f"Key {search_key} found at index {index} with data: {found_key}")
        print(f"Key {search_key} found in node with keys: {node.keys[index]} at index {index}, parent is {parent.keys}")
    else:
        print(f"Key {search_key} not found in the B-tree.")

    B.remove(29)
    print('-' * 50)
    B.remove(29)
    print('-' * 50)
    B.remove(28)
    
    B.remove(24)
    B.remove(26)
    B.print_tree(B.root)

if __name__ == '__main__':
    main()
