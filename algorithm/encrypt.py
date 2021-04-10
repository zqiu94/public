CHARACTERS_IN_ALPHABET = 26

def encrypt(orig_massage, shift_amount):
    """
    Encrypt string plaintext using a Caesar cipher by shift_amount
    :param plaintext: the string to encrypt
    :param shift_amount: an integer between 0 and 25
    :return: the ciphertext string, with each character shifted by shift_amount.

    >>> encrypt("hello", 1)
    'ifmmp'
    >>> encrypt("secret", 18)
    'kwujwl'
    """
    if not (0 < shift_amount < CHARACTERS_IN_ALPHABET):
        shift_amount = 1
    shifted_letters = ""
    orig_massage = orig_massage.lower()
    for letter in orig_massage:
        letter_num = ord(letter)
        if 96 < letter_num < 123:
            letter_between_0_and_25 = letter_num - ord('a')
            letter_between_0_and_25_shifted = (letter_between_0_and_25 + shift_amount) % 26
            shifted_letter = chr(letter_between_0_and_25_shifted + ord('a'))
            shifted_letters += shifted_letter
        else:
            shifted_letters += letter
    return shifted_letters
    # print(f"Encrypted message: {shifted_letters}")

def decrypt(ciphertext, shift_amount):
    """
    Decrypts string ciphertext using a Caesar cipher when the original shift was shift_amount
    Assumption: ciphertext will be in lowercase
    :param ciphertext: the string to decrypt
    :param shift_amount: an integer between 0 and 25
    :return: the decrypted string

    >>> decrypt("ifmmp", 1)
    'hello'
    >>> decrypt('kwujwl', 18)
    'secret'
    """
    decrypted_letters = ""
    if not (0 < shift_amount < CHARACTERS_IN_ALPHABET):
        shift_amount = 1
    for letter in ciphertext:
        letter_num = ord(letter)
        if 96 < letter_num < 123:
            letter_between_0_and_25 = letter_num - ord('a')
            letter_between_0_and_25_shifted = (letter_between_0_and_25 - shift_amount) % 26
            decrypted_letter = chr(letter_between_0_and_25_shifted + ord('a'))
            decrypted_letters += decrypted_letter
        else:
            decrypted_letters += letter

    return decrypted_letters


if __name__ == "__main__":
    print(encrypt("hello", 1))
    print(encrypt("secret", 18))
    print(decrypt(encrypt("hello", 25), 25))  # should print "hello"
    print(decrypt(encrypt("secret", 7), 7))  # should print "secret"

    # orig_massage = input("Please type the original massage!")
    # shift_amount = int(input("Please type the amount you want to shift"))
    # print(encrypt(orig_massage, shift_amount))
