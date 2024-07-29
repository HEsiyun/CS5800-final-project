import matplotlib.pyplot as plt
import networkx as nx

def choose_max_degree(df_length: int) -> int:
    '''
    Function choose_max_degree
    This function takes the length of the dataframe and prompts the user to enter the maximum degree of the B tree.
    Let the user choose the maximum degree of the B tree. The minimum degree is half of the maximum degree.
    Parameters:
    df_length -- the length of the dataframe
    Returns the minimum degree of the B tree.
    '''
    while True:
        try:
            max_degree = int(input("Enter the maximum degree of the B tree, please choose an even number larger than 3: "))
            if max_degree < 4:
                raise ValueError("Degree must be greater than 3")
            # if max_degree >= df_length:
            #     raise ValueError("Degree must be less than the number of rows in the dataframe")
            return int(max_degree / 2) # Convert to minimum degree
        except ValueError as error:
            print("Invalid value:", error)

# B tree node class
# Even max degree only
class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []  # This will store tuples
        self.child = []

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(True)  # Initially, root should be a leaf
        self.t = t  # Minimum degree

    def insertion(self, k):
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
        i = 0  # Start from the beginning of the keys list

        if x.leaf:
            # Find the position to insert the new key
            while i < len(x.keys) and k > x.keys[i]:
                i += 1
            # if i == len(x.keys) or k != x.keys[i]:
            x.keys.insert(i, k)  # Insert the key at the found position
            # else:
            #     # If the key is already in the tree, we can update the value
            #     x.keys[i] = k
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
            
    def search_key(self, k, x=None):
        """Search for a key in the B-tree and return the node and index of the key if found."""
        if x is None:
            x = self.root  # Start from the root if no node is provided
        i = 0
        # Navigate through the keys of the node to find the possible location of the key
        while i < len(x.keys) and k > x.keys[i][0]:
            i += 1
        # Check if the key is found in the current node
        if i < len(x.keys) and k == x.keys[i][0]:
            return (x, i)
        elif x.leaf:  # If reached a leaf node, the key is not present
            return None
        else:  # Otherwise, move to the appropriate child node
            return self.search_key(k, x.child[i])
    
    # Print the tree
    def print_tree(self, x, l=0, prefix=""):
        """Print a structured representation of the B-tree."""
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
        B.print_tree(B.root)
        print('-' * 50)
    
    # Search for the specific key
    search_value = 8
    result = B.search_key(search_value)
    if result is not None:
        node, index = result
        print(f"Key {search_value} found in node with keys: {node.keys} at index {index}")
    else:
        print(f"Key {search_value} not found in the B-tree.")

if __name__ == '__main__':
    main()