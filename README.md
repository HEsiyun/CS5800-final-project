# Mini-database User Guide
The main functionalities of the mini-database are insert, search, and delete. This mini-database implements a B-tree to manage user-defined indexes, enabling efficient search, insertion, and deletion. A Pandas DataFrame is also used to store and display data to the users.

Call the mini-database in the terminal by typing: 
```
python mini_database.py
```
## Initialization
When the database is completely empty, the users have 2 choices to initialize the databse:

**Choice 1**: Import an existing excel data. Default file path is "data/data_with_grade.xlsx", but the users can enter their own file path. 

**Choice 2**: Generate data by entering column names and the corresponding values.

## Max Degree and Btree Key
After we have some data inside the mini-database, the users can choose a unique column from the dataframe to be the key of the Btree. The users can also choose a maximum degree of the Btree, which is the maximum number of children of each node. The maximum degree must be an even number larger than 3.

## Basic Operations 
The users are given the choices of insert, search, delete, or exit (1 to insert, 2 to search, 3 to delete, 4 to exit).

## Print and Visualization
After the user adds (including inserting, importing, or generating data from scratch) or deletes data from the mini-database, the structure of the B-tree will be printed, and the B-tree will be plotted in a popup window.

# References 
[1] “Part 7 - introduction to the B-tree,” Let’s Build a Simple Database, https://cstack.github.io/db_tutorial/parts/part7.html (accessed Aug. 3, 2024). <p>
[2] Lecture 10 - insertion into a B-tree, https://webdocs.cs.ualberta.ca/~holte/T26/ins-b-tree.html (accessed Aug. 3, 2024). <p> 
[3] J. Kubica, Data Structures the Fun Way: From Binary Search to Quadtrees in 100 Cups of Coffee. San Francisco, CA: No Starch Press, Inc, 2022. <p>
[4] “Introduction of B-tree,” GeeksforGeeks, https://www.geeksforgeeks.org/introduction-of-b-tree-2/ (accessed Jul. 12, 2024). <p>
[5] “Understanding B-trees: The data structure behind modern databases,” YouTube, https://www.youtube.com/watch?v=K1a2Bk8NrYQ (accessed Jul. 11, 2024). <p>
[6] “10.2 b trees and B+ trees. how they are useful in databases,” YouTube, https://www.youtube.com/watch?v=aZjYr87r1b8 (accessed Jul. 11, 2024). <p>
[7] “B-trees,” B-Tree Visualization, https://www.cs.usfca.edu/~galles/visualization/BTree.html (accessed Jul. 11, 2024). <p>

