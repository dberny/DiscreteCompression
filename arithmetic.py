#
# This code has functions that use arithmetic compresstion
#

def char_dict(s):
    charDict = {}
    for char in s:
        # print(i)
        if char in charDict:
            charDict[char] = charDict[char] + 1
        else:
            charDict[char] = 1

    for key in charDict:
        charDict[key] = charDict[key] / len(s)
    # charDict["len"] = len(s)
    return charDict

def in_Line(cdict, p, Acode):
    Adict = {}
    range = p - Acode
    top = Acode
    for key in cdict:
        Adict[key] = top #* p
        top = top + (cdict[key] * range)
    return Adict



def A_Compress(s):
    charDict = char_dict(s)
    p = 1*10**9
    artcode = 0
    artDict = in_Line(charDict,p,artcode)
    for char in s:
        range = p - artcode
        artcode = artDict[char]
        #range = p - artcode
        p = artcode + charDict[char] * range
        artDict = in_Line(charDict, p, artcode)
        # print(char)
        # print('work code p adict ')
        # print(artcode)
        # print("roof top")
        # print(p)
        # print(artDict)
    return artcode



def main():
    test = 'hello world! its a nice day today.'
    test_dict = char_dict(test)
    print(test_dict)
    adict = in_Line(test_dict, 1, 0)
    print(adict)
    code = A_Compress(test)
    print(code)
    # A_Compress(test)

if __name__ ==  '__main__':
    main()
