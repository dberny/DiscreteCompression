from binarytree import Node as ImportedNode
from binarytree.exceptions import NodeTypeError
from binarytree.exceptions import NodeNotFoundError
from operator import itemgetter


def huffmanTree(input):
    tree = Node('-', 0)
    print(getNodePosition(tree, '-'))
    treePositions = dict()
    for c in input:
        tree = updateTree(tree, c)
        print(tree)
    print(tree)
    return tree


def updateTree(tree, letter):
    letterPos = getNodePosition(tree, letter)
    if letterPos > 0:  # case where the letter is already in the tree
        print('adding repeated', letter)
        tree[letterPos].count += 1
        print(tree[letterPos].count)
        balanceTree(tree, tree[letterPos])
        updateValues(tree)
        return tree
    elif (tree.value == '-'):  # case where the tree is empty
        # subtree = Node(1, None, left=tree, right=Node(letter, 1))
        subtree = Node(1, None, left=Node(letter, 1), right=tree)
        return subtree
    else:  # case where we are adding a new letter to the tree
        print('add new letter ', letter)
        nullPos = getNodePosition(tree, '-')
        subtree = Node(1, None, left=Node(letter, 1), right=tree[nullPos])
        tree[nullPos] = subtree
        balanceTree(tree, tree[nullPos].left)
        # print(treePositions)
        updateValues(tree)
        return tree


def balanceTree(tree, node):
    nodeValue = node.count
    print(nodeValue)
    originalPosition = getNodePosition(tree, node.value)
    while node.parent is not None:
        nodeValue = updateValues(node)
        indices = getListofIndices(tree)
        nodeIndex = indices.index(originalPosition)
        print('balance on ', node.value)
        print(indices, nodeIndex)
        print('indices up to value', node.value, indices[:nodeIndex])
        print(tree)
        count = 0
        # for i in indices[:nodeIndex]:
        while count < nodeIndex:
            # print(i, tree[i].value)
            print('count', count)
            print('tree index', indices[count])
            if tree[indices[count]].count is not None:
                if tree[indices[count]].count < nodeValue:
                    print(indices[count], tree[indices[count]].value)
                    swapNode = tree[indices[count]]
                    tree[indices[count]] = node
                    tree[originalPosition] = swapNode
                    count = 100000
            else:
                if tree[indices[count]].value < nodeValue:
                    swapNode = tree[indices[count]]
                    tree[indices[count]] = node
                    tree[originalPosition] = swapNode
                    count = 100000
            count += 1
        originalPosition = (originalPosition-1)//2
        # if (originalPosition < 0):
        #     originalPosition = 0
        node = node.parent


def getListofIndices(tree):
    numNodes = len(tree.inorder)
    indices = []
    i = 0
    while numNodes > 0:
        try:
            if tree[i] is not None:
                indices.append(i)
                numNodes -= 1
        except NodeNotFoundError:
            pass
        i += 1
    return indices


def getNodePosition(tree, nodeValue):
    indices = getListofIndices(tree)
    for i in indices:
        if (tree[i].value == nodeValue):
            return i
    return -2


def updateValues(tree):
    if tree.left is None and tree.right is None:
        if tree.count is not None:
            return tree.count
        return tree.value
    elif tree.left is None:
        if tree.count is not None:
            tree.count = updateValues(tree.right)
            return tree.count
        else:
            tree.value = updateValues(tree.right)
            return tree.value
    elif tree.right is None:
        if tree.count is not None:
            tree.count = updateValues(tree.left)
            return tree.count
        else:
            tree.value = updateValues(tree.left)
            return tree.value
    else:
        if tree.count is not None:
            tree.count = updateValues(tree.left) + updateValues(tree.right)
            return tree.count
        else:
            tree.value = updateValues(tree.left) + updateValues(tree.right)
            return tree.value


def printEncodedMessage(message):
    output = ''
    for bits in message:
        output += bits + ' '
    print('Encoded message: ', output)


def encodeMessage(input, codes):
    coded = []
    for c in input:
        coded.append(codes[c])
    return coded


def getCodes(input, tree):
    paths = dict()
    getPaths(tree, '', paths)
    return paths


def getPaths(tree, path, pathsDict):
    if isLeaf(tree):
        pathsDict[tree.value] = path
    if tree.left is not None:
        getPaths(tree.left, path + '0', pathsDict)
    if tree.right is not None:
        getPaths(tree.right, path + '1', pathsDict)


def isLeaf(tree):
    if (tree.left is None) and (tree.right is None):
        return True
    return False


class Node(ImportedNode):
    def __init__(self, value, count, left=None, right=None, parent=None):
        self.value = value
        self.count = count
        self.left = left
        self.right = right
        self.parent = parent

    def __setattr__(self, attr, obj):
        if attr == 'left':
            if obj is not None and not isinstance(obj, Node):
                raise NodeTypeError(
                    'left child must be a Node instance')
            if obj is not None:
                obj.parent = self
        elif attr == 'right':
            if obj is not None and not isinstance(obj, Node):
                raise NodeTypeError(
                    'right child must be a Node instance')
            if obj is not None:
                obj.parent = self
        object.__setattr__(self, attr, obj)


if __name__ == "__main__":
    message = 'sausage'
    print('Original message: ', message)
    tree = (huffmanTree(message))
    codes = getCodes(message, tree)
    encodedMessage = encodeMessage(message, codes)
    printEncodedMessage(encodedMessage)
