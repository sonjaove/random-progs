class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def preorder_tree_walk(node):
    if node is None:
        return
    print(node.value)  # Visit the root
    preorder_tree_walk(node.left)  # Recur on left subtree
    preorder_tree_walk(node.right)  # Recur on right subtree
def postorder_tree_walk(node):
    if node is None:
        return
    postorder_tree_walk(node.left)  # Recur on left subtree
    postorder_tree_walk(node.right)  # Recur on right subtree
    print(node.value)  # Visit the root
def inorder_tree_walk(node):
    if node is None:
        return
    inorder_tree_walk(node.left)  # Recur on left subtree
    print(node.value)  # Visit the root
    inorder_tree_walk(node.right)  # Recur on right subtree

# Example tree:
#       A
#      / \
#     B   C
#    / \
#   D   E

root = Node('A')
root.left = Node('B')
root.right = Node('C')
root.left.left = Node('D')
root.left.right = Node('E')
root.left.left.right = Node('t')
root.left.right.left = Node('f')
root.right.right = Node('g')
# Perform preorder traversal
preorder_tree_walk(root)
print("-----")
# Perform postorder traversal
postorder_tree_walk(root)
print("-----")
# Perform inorder traversal
inorder_tree_walk(root)