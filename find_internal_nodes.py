from collections import deque

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.children = []


def create_tree(L):
    nodes = [TreeNode(i) for i in range(len(L))]
    root = None
    for i, val in enumerate(L):
        if val == -1:
            root = nodes[i]
        else:
            nodes[val].children.append(nodes[i])
    return root


def find_internal_nodes_num(tree):
    root = create_tree(tree)
    num_nodes_dfs = count_internal_nodes_bfs(root)
    return num_nodes_dfs


def count_internal_nodes(node):
    if not node.children:
        return 0
    count = 1  # if it has children, it's an internal node
    for child in node.children:
        count += count_internal_nodes(child)
    return count


def count_internal_nodes_bfs(root):
    if not root:
        return 0
    count = 0
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if len(node.children) > 0:
            count += 1
        queue.extend(node.children)
    return count


if __name__ == '__main__':
    # my_tree = [4, 4, 1, 5, -1, 4, 5]
    my_tree = [15, 2, 15, 4, 5, -1, 5, 5, 7, 6, 3, 10, 3, 9, 1, 6]
    print(f'Total internal nodes in the tree: {find_internal_nodes_num(my_tree)}')
    print(f'But we don\'t need any BFS in this case, see the next line: ')
    internal_nodes = len(set(my_tree)) - 1
    print(f'time complexity solution (O(N)): {internal_nodes}')
