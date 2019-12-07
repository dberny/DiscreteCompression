from binarytree import Node as ImportedNode
from binarytree.exceptions import NodeTypeError
from operator import itemgetter


def huffmanTree(input):
    '''
    Takes the input and builds the tree based on likelihood of each character
    appearing.
    '''
    counts = buildDict(input)
    createdTrees = dict()
    pairs = sorted(counts.items(), key=itemgetter(1))
    tree = None
    while len(pairs) > 1:
        tree = combineLetters(pairs, createdTrees)
    return tree


def buildDict(input):
    '''
    Counts how often each character appears in input
    '''
    counts = dict()
    for c in input:
        counts[c] = counts.get(c, 0) + 1
    return counts


def combineLetters(pairs, createdTrees):
    letters = pairs[0][0]+pairs[1][0]
    firstTree = createdTrees.get(pairs[0][0], Node(pairs[0][0]))
    secondTree = createdTrees.get(pairs[1][0], Node(pairs[1][0]))
    sum = pairs[0][1]+pairs[1][1]

    tree = Node(sum, left=firstTree, right=secondTree)
    createdTrees[letters] = tree

    pairs.append((letters, sum))
    pairs.remove(pairs[1])
    pairs.remove(pairs[0])
    pairs.sort(key=itemgetter(1))
    return tree


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
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __setattr__(self, attr, obj):
        if attr == 'left':
            if obj is not None and not isinstance(obj, Node):
                raise NodeTypeError(
                    'left child must be a Node instance')
        elif attr == 'right':
            if obj is not None and not isinstance(obj, Node):
                raise NodeTypeError(
                    'right child must be a Node instance')
        object.__setattr__(self, attr, obj)


if __name__ == "__main__":
    message = 'racecar'
    print('Original message: ', message)
    tree = (huffmanTree(message))
    print(tree)
    codes = getCodes(message, tree)
    encodedMessage = encodeMessage(message, codes)
    printEncodedMessage(encodedMessage)
