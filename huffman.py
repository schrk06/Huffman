from algo_py import bintree
from algo_py import heap


###############################################################################
## COMPRESSION

def build_frequency_list(dataIN):
    """
    Builds a tuple list of the character frequencies in the input.
    """
    unique_items = []
    for item in dataIN:
        is_unique = True
        index = 0
        while is_unique and index < len(unique_items):
            if unique_items[index] == item:
                is_unique = False
            index += 1
        if is_unique:
            unique_items.append(item)
    freq_list = []
    for char in unique_items:
        freq = 0
        for c in dataIN:
            if c == char:
                freq += 1

        freq_list.append((freq,char))

    return freq_list


def build_Huffman_tree(inputList):
    """
    Processes the frequency list into a Huffman tree according to the algorithm.
    """
    pq = heap.Heap()
    for (freq, char) in inputList:
        pq.push((freq, bintree.BinTree(char,None,None)))

    while len(pq.elts) > 2:
        (right_freq, right_tree) = pq.pop()
        (left_freq, left_tree) = pq.pop()
        new_tree = bintree.BinTree(None, left_tree, right_tree)
        pq.push((left_freq + right_freq, new_tree))

    (freq, tree) = pq.pop()
    return tree


def __binairerepresentation(huffmanTree, tab, str):
    """
        Une procédure qui permet de modifier le parametre tab initialement vide en une liste de couples contenant un char et sa représentation binaire dans l'arbre
        huffmanTree: BinTree
        tab: liste vide initialement mais qui aura cette structure (huffmanTree.key, string)
        str: une string qui n'est utilse que pour la recursion

    """
    if (huffmanTree.left != None):
        left = str + "0"
        __binairerepresentation(huffmanTree.left, tab, left)

    if (huffmanTree.right != None):
        right = str + "1"
        __binairerepresentation(huffmanTree.right, tab, right)

    else:
        tab.append((huffmanTree.key, str))


def encode_data(huffmanTree, dataIN):
    """
    Encodes the input string to its binary string representation.
    """
    tab = []
    __binairerepresentation(huffmanTree, tab, "")
    result = ""
    for l in dataIN:
       for a in tab:
          if (l == a[0]):
            result += a[1]
    return result


def __fromchartobyte(char):
    """
        fonction qui prend en paramètre un caractère et qui donne sa représentation en code ascii en chaine de caractères
    """
    value= ord(char)
    result = ""
    while value != 0:
        result = str(value % 2) + result
        value = value // 2
    for i in range(8-len(result)):
        result = "0" + result
    return result

def __frombytetochar(byte):
    """

    :param byte: une representation en code ascci du caractère, sous forme de chaine de caracteres contenant uniquement des "0" et des "1"
    :return: un char
    """
    char_value = 0
    for i in range(8):
        char_value += int(byte[i]) * (2**(7-i))
    return chr(char_value)


def __EncodeHuffman(huffmanTree, result):
    """
      Fonction récursive qui fait en sorte de retranscrire chaque caractère présent dans le huffmantree en binaire, et anjoutant avant le codage un 1, mais aussi un 0 à chaque niveau de l'arbre, on utilisera une liste initialement vide pour stocker ce code
    """
    if (huffmanTree.left != None and huffmanTree.right != None):
        result.append("0")
        __EncodeHuffman(huffmanTree.left, result)
        __EncodeHuffman(huffmanTree.right, result)

    else:
        result.append("1")
        result.append(__fromchartobyte(huffmanTree.key))




def encode_tree(huffmanTree):
    """
    Encodes a huffman tree to its binary representation using a preOrder traversal:
        * each leaf key is encoded into its binary representation on 8 bits preceded by '1'
        * each time we go left we add a '0' to the result
    """
    binaire = []
    result = ""
    __EncodeHuffman(huffmanTree, binaire)

    for i in binaire:
      result += i

    return result


def to_binary(dataIN):
    """
    Compresses a string containing binary code to its real binary value.
    """
    a = 0
    b = 0
    c = ""
    d = 0
    f=len(dataIN)

    for i in range(f + 1):
        if (a > 7):
            c += chr(b)
            a = 0
            b = 0

        if (i != f):
            if (a == 0 and (i + 8) > f):
                e = f - (i + 8)
                a = -e
                d = -e
            if (dataIN[i] == "1"):
                b += 2**(7 - a)

            a += 1

    return (c, d)


def compress(dataIn):
    """
    The main function that makes the whole compression process.
    """
    
    tavla = build_frequency_list(dataIn)
    sejra = build_Huffman_tree(tavla)
    malouma = encode_data(sejra, dataIn)
    tina = encode_tree(sejra)
    return (to_binary(malouma), to_binary(tina))

    
################################################################################
## DECOMPRESSION

def decode_data(huffmanTree, dataIN):
    """
    Decode a string using the corresponding huffman tree into something more readable.
    """
    tab = []
    __binairerepresentation(huffmanTree, tab, "")
    r = ""
    a=""
    for i in dataIN:
        a += i
        for char in tab:
          if (a == char[1]):
            r += char[0]
            a = ""

    return r


def __decodetree (dataIN,tree,bitlist):
    """
    fonction auxiliaire qui permet de passer de la retranscription binaire vers un arbre, elle est récursive
    :param dataIN: la chaine de caractères qui représente l'arbre
    :param bitlist: une liste contenant un seul élément, cet élément représente "l'avancement dans la dataIN, j'étais contraint d'utiliser une liste au lieu d'un simple entier, car si on utilise un simple entier on perdera sa valeur après chaque récursion, alors que la liste elle applique le changement même en dehors de la récursion 
    :return: un bintree
    """
    if bitlist[0] < len(dataIN):
        if dataIN[bitlist[0]] == '0':
            tree = bintree.BinTree(None, None, None)
            bitlist[0] += 1
            tree.left = __decodetree(dataIN, tree.left, bitlist)
            tree.right = __decodetree(dataIN, tree.right, bitlist)
        else:
            bitlist[0] += 1
            byte = ""
            for i in range (8):
                byte += dataIN[bitlist[0]]
                bitlist[0] += 1
            tree = bintree.BinTree(__frombytetochar(byte), None, None)
        return tree


    
def decode_tree(dataIN):
    """
    Decodes a huffman tree from its binary representation:
        * a '0' means we add a new internal node and go to its left node
        * a '1' means the next 8 values are the encoded character of the current leaf         
    """
    bitlist = []
    bitlist.append(0)
    T = __decodetree(dataIN, bintree.BinTree(None, None, None), bitlist)
    return T


def from_binary(dataIN, align):
    """
    Retrieve a string containing binary code from its real binary value (inverse of :func:`toBinary`).
    """
    result = ""
    for i in range(len(dataIN) -1 ):
        result += __fromchartobyte(dataIN[i])
    anegar = __fromchartobyte(dataIN[len(dataIN) - 1])
    for j in range(align , 8 ):
        result += anegar[j]
    return result


def decompress(data, dataAlign, tree, treeAlign):
    """
    The whole decompression process.
    """
    A = from_binary(data, dataAlign)
    B = from_binary(tree, treeAlign)
    C = decode_tree(B)
    return decode_data(C, A)
