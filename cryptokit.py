import json
import argparse
import math
import hashlib

def loadWords():
    with open("words_dictionary.json", "r") as f:
        english_dict = json.load(f)

    return english_dict

def loadPasswords():
    with open("commonpass.txt","r") as f:
        passwords = f.readlines()

    return passwords

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


def bruteForceHash(hashfunc, digest, passwords):
    if hashfunc == 'md5':
        for pwd in passwords:
            dgst = hashlib.md5(pwd)
            if dgst.hexdigest() == digest:
                print("Password found: " + pwd + " for digest " + digest)
                return





def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--cipher', dest='cipher', choices=['ceasar', 'vigenere2k', 'vigenere3k', 'vigenere4k', 'all'], required=False)
    parser.add_argument('-a','--alphabet', dest = 'alphabet', required=False)
    parser.add_argument('-ciphertext','--ciphertext', dest='ciphertext', required=False)
    parser.add_argument('-hash', '--hash', dest='hashfunc', choices=['md5','sha1'])
    parser.add_argument('-dgst','--digest', dest='digest')
    args = parser.parse_args()

    fmt = args.cipher
    alpha = args.alphabet
    ciphertext = args.ciphertext
    hashfunc = args.hashfunc
    digest = args.digest

    dictionary = loadWords()
    mostCommonPasswords = loadPasswords()

    if fmt != None:
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

    elif hashfunc != None and digest != None:
        if hashfunc == 'md5':
            bruteForceHash(hashfunc, digest, mostCommonPasswords)

        elif hashfunc == 'sha1':
            bruteForceHash(hashfunc,digest, mostCommonPasswords)

        else:
            print("Hash function not supported!")

    else:
        print("No arguments provided")



if __name__ == "__main__":
    main()