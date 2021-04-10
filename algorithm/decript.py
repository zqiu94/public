def decrypt(ciphertext):
    print(f"\nDecrypting {ciphertext}...")
    for i in range(5):
        decrypted_letters = ""
        for letter in ciphertext:
            letter_num = ord(letter)
            if 96 < letter_num < 123:
                letter_between_0_and_25 = letter_num - ord('a')
                letter_between_0_and_25_shifted = (letter_between_0_and_25 - i - 1) % 26
                decrypted_letter = chr(letter_between_0_and_25_shifted + ord('a'))
                decrypted_letters += decrypted_letter
            else:
                decrypted_letters += letter
        # return decrypted_letters
        print(decrypted_letters)



decrypt("itgcvlqd")
decrypt("fbjxtrj")
decrypt("tcxlsr")
