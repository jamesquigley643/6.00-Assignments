# Problem Set 4A
# Name: James Quigley
# Collaborators: None
# Time Spent: 1:00
# Late Days Used: A lot

# Part A0: Data representation
# Fill out the following variables correctly.
# If correct, the tests named data_representation should pass.
tree1 = [[4,10],5] # TODO: change this assignment
tree2 = [[15,4],[[1,2],10]] # TODO: change this assignment
tree3 = [[12],[14,6,2],[19]] # TODO: change this assignment


# Part A1: Multiplication on tree leaves

def mul_tree(tree):
    """
    Recursively computes the product of all tree leaves.
    Returns an integer representing the product.

    Inputs
       tree: A list (potentially containing sublists) that
       represents a tree structure.
    Outputs
       total: An int equal to the product of all leaves of the tree.

    """

    # TODO: Your code here
    if tree == []: #empty list
        return 1
    
    elif len(tree) == 1 and type(tree[0]) == int: #single element
        return tree[0]
    #multiple elements
    elif type(tree[0]) == int: #first element is an integer
        return prod(tree[0],mul_tree(tree[1:]))
    
    elif type(tree[0]) == list: #first element is a list
        return prod(mul_tree(tree[0]),mul_tree(tree[1:]))


# Part A2: Arbitrary operations on tree leaves

def addem(a,b):
    """
    Example operator function.
    Takes in two integers, returns their sum.
    """
    return a + b

def prod(a,b):
    """
    Example operator function.
    Takes in two integers, returns their product.
    """
    return a * b

def op_tree(tree, op, base_case):
    """
    Recursively runs a given operation on tree leaves.
    Return type depends on the specific operation.

    Inputs
       tree: A list (potentially containing sublists) that
       represents a tree structure.
       op: A function that takes in two inputs and returns the
       result of a specific operation on them.
       base_case: What the operation should return as a result
       in the base case (i.e. when the tree is empty).
    """

    # TODO: Your code here
    if tree == []: #empty list
        return base_case
    
    elif len(tree) == 1 and type(tree[0]) == int: #single element
        return tree[0]
    #multiple elements
    elif type(tree[0]) == int: #first element is an integer
        return op(tree[0],op_tree(tree[1:],op,base_case))
    
    elif type(tree[0]) == list: #first element is an list
        return op(op_tree(tree[0],op,base_case),op_tree(tree[1:],op,base_case))

# Part A3: Searching a tree

def search_odd(a, b):
    """
    Operator function that searches for odd values within its inputs.

    Inputs
        a, b: integers or booleans
    Outputs
        True if either input is equal to True or odd, and False otherwise
    """

    # TODO: Your code here
    if type(a) == int and type(b) == int: #both are integers
        if a % 2 == 1 or b % 2 == 1:
            return True
        
    elif type(a) == bool and type(b) == bool: #both are booleans
        if a == True or b == True:
            return True
        
    elif type(a) == bool and type(b) == int: #first is boolean
        if a == True or b % 2 == 1:
            return True
        
    elif type(a) == int and type(b) == bool: #first is integer
        if a % 2 == 1 or b == True:
            return True
    return False


if __name__ == '__main__':
    # You can use this part for your own testing and debugging purposes.
    # Do not erase the pass statement below.
    pass
