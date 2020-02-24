import json
import argparse
import math

def loadWords():
    with open("words_dictionary.json", "r") as f:
        english_dict = json.load(f)

    return english_dict

def isEnglishText(dictionary, ciphertext):
    txt = ciphertext.split()
    counter = 0

    for x in txt:
        if x in dictionary and len(x) > 1:
            counter = counter + 1

    if counter > 2:
        return True
    else:
        return False

def ceasarChipher(alphabet, ciphertext, dictionary):

    print("---------------CEASAR CIPHER---------------")
    for key in range(len(alphabet)):

        decoded = ""

        for ch in ciphertext:
            if ch in alphabet:
                num = alphabet.find(ch)
                num = num - key

                if num < 0:
                    num = num + len(alphabet)

                decoded = decoded + alphabet[num]

            else:
                decoded = decoded + ch


        if isEnglishText(dictionary, decoded) == True:
            print("Key %s: %s" % (key,decoded))


def vigenereCipher(alphabet, ciphertext, keys, dictionary):

    decoded = ""
    check = False
    z = 0

    for i in range(len(ciphertext)):
        if ciphertext[i] in alphabet:
            num = alphabet.find(ciphertext[i])
            num = num - keys[z%len(keys)]

            if num < 0:
                num = num + len(alphabet)

            decoded = decoded + alphabet[num]
            z = z + 1

        else:
            decoded = decoded + ciphertext[i]

    if isEnglishText(dictionary,decoded) == True:
        check = True
        print("Keys " + str(keys) + " " + str(decoded))

    return check


def vigenere2keys(alphabet, ciphertext, dictionary):

    counter = 0
    print("---------------VIGENERE CIPHER 2 KEYS---------------")
    for i in range(len(alphabet)):
        for j in range(len(alphabet)):
            check = vigenereCipher(alphabet, ciphertext,[i,j], dictionary)
            if check == True:
                counter = counter + 1

    if counter == 0:
        print("No results found!")

def vigenere3keys(alphabet, ciphertext, dictionary):

    counter = 0
    print("---------------VIGENERE CIPHER 3 KEYS---------------")
    for i in range(len(alphabet)):
        for j in range(len(alphabet)):
            for k in range(len(alphabet)):
                check = vigenereCipher(alphabet, ciphertext, [i, j, k], dictionary)
                if check == True:
                    counter = counter + 1

    if counter == 0:
        print("No results found!")

def vigenere4keys(alphabet, ciphertext, dictionary):
    counter = 0
    print("---------------VIGENERE CIPHER 4 KEYS---------------")
    for i in range(len(alphabet)):
        for j in range(len(alphabet)):
            for k in range(len(alphabet)):
                for z in range(len(alphabet)):
                    check = vigenereCipher(alphabet, ciphertext, [i, j, k, z], dictionary)
                    if check == True:
                        counter = counter + 1

    if counter == 0:
        print("No results found!")

def bruteForceVigenere(alphabet, ciphertext, dictionary):

    vigenere2keys(alphabet, ciphertext, dictionary)
    vigenere3keys(alphabet,ciphertext,dictionary)
    vigenere4keys(alphabet,ciphertext,dictionary)



def transpositionCipher(ciphertext):


    for key in range(len(ciphertext)):
        # The number of "columns" in our transposition grid:
        numOfColumns = math.ceil(len(ciphertext) / (key+1))
        # The number of "rows" in our grid will need:
        numOfRows = key+1
        # The number of "shaded boxes" in the last "column" of the grid:
        numOfShadedBoxes = (numOfColumns * numOfRows) - len(ciphertext)

        # Each string in plaintext represents a column in the grid.
        plaintext = [''] * int(numOfColumns)

        # The col and row variables point to where in the grid the next
        # character in the encrypted message will go.
        col = 0
        row = 0

        for symbol in ciphertext:
            plaintext[col] += symbol
            col += 1 # point to next column

            # If there are no more columns OR we're at a shaded box, go back to
            # the first column and the next row.
            if (col == numOfColumns) or (col == numOfColumns - 1 and row >= numOfRows - numOfShadedBoxes):
                col = 0
                row += 1

        print(''.join(plaintext))




def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--cipher', dest='cipher', choices=['ceasar', 'vigenere2k', 'vigenere3k', 'vigenere4k', 'all'], required=True)
    parser.add_argument('-a','--alphabet', dest = 'alphabet', required=True)
    parser.add_argument('-ciphertext','--ciphertext', dest='ciphertext', required=True)

    args = parser.parse_args()

    fmt = args.cipher
    alpha = args.alphabet
    ciphertext = args.ciphertext

    dictionary = loadWords()

    if fmt == 'ceasar':
        ceasarChipher(alpha,ciphertext, dictionary)

    elif fmt == 'vigenere2k':
        vigenere2keys(alpha,ciphertext,dictionary)

    elif fmt == 'vigenere3k':
        vigenere3keys(alpha,ciphertext,dictionary)

    elif fmt == 'vigenere4k':
        vigenere4keys(alpha,ciphertext,dictionary)

    elif fmt == 'all':
        ceasarChipher(alpha, ciphertext, dictionary)
        bruteForceVigenere(alpha,ciphertext,dictionary)

if __name__ == "__main__":
    main()