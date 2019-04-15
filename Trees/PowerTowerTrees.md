
## Power Tower Trees! ##

This module contains the Node class - representing a power tower with a
binary tree structure - and functions to convert between strings and trees.

The Node class has the attributes self.left - the left child - and self.right -
the right child. Note, since we're representing power towers we only need
leaves, so a Node doesn't have a value.
The leaves could theoretically be anything, but I only added parsing handling
for int, float, and string.

For the following examples, assume that
```python
node = Node(Node(2, 3), 4)
```

#### To-String Functions

to_bracket: Tree --> bracket representation
```python
to_bracket(node)
--> '(((2)(3))(4))'
```

to_tower: Tree --> tower representation
```python
to_tower(node)
--> '(2^3)^4'
```

to_LaTeX: Tree --> tower representation, but as LaTeX input
```python
to_LaTeX(node)
--> '\left(2^{3}\right)^{4}'
```

to_tree: Tree --> representation as a graph
```python
to_tree(node)
-->   /\      
     /  \     
    /    \    
   /\     4   
  2  3       

```

#### To-Tree Functions

parse_bracket: Bracket representation --> tree
```python
parse_bracket('(((2)(3))(4))') == node
--> True
```

parse_tower: Tower representation --> tree
```python
parse_tower('(2^3)^4') == node
--> True
```

parse_LaTeX: LaTeX --> tree
```python
parse_LaTeX('\\left(2^{3}\\right)^{4}') == node
--> True
```
