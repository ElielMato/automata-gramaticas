phrase = str(input("Ingrese una frase:"))
num = int(input("Ingrese un numero:"))

def encrypt(phrase, num):
    phrase = phrase.lower()
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    key_encrypted = ""
    for i in phrase:
        if i in alphabet:
            key_encrypted += alphabet[(alphabet.index(i) + num) % 26]
        else:
            key_encrypted += i
    return key_encrypted

print(encrypt(phrase, num))