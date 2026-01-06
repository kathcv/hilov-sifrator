import hill_cipher as hc

def main():
    print("HILL CIPHER ENCODER/DECODER\n\n")

    while True:
        key_matrix = hc.enter_key_matrix()
        inv = hc.nzd(key_matrix)
            
        if inv is None:
            print("The key matrix is not valid. The determinant and modulus are not coprime.\n" \
            "Please enter a valid key matrix.\n\n")
        else:
            break

    hc.display_matrix(key_matrix)

    while True:
        print("Available operations:")
        print("1. Encode text")
        print("2. Decode text")
        print("3. Change key matrix")
        print("4. Exit")

        operation = input("\nSelect operation: ").strip().lower()

        if operation == '1':
            while True:
                plaintext = input("Enter plaintext to be encrypted: ")
                normalized = hc.normalize_text(plaintext)
                if normalized is not None:
                    break

            pad_plaintext = hc.pad_text(normalized)
            cipher_text = hc.encode(pad_plaintext, key_matrix)
            print(f"Cipher Text: {repr(cipher_text)}")
        elif operation == '2':
            while True:
                cipher_text = input("Enter cipher text to be decrypted: ")

                if (len(cipher_text) % 4) != 0:
                    print("Invalid cipher text length. It must be a divisible by 4.")
                    continue

                normalized = hc.normalize_text(cipher_text)
                if normalized is not None:
                    break
                
            decrypted_text = hc.decode(normalized, key_matrix)
            print(f"Decrypted Text: {repr(decrypted_text)}")
        elif operation == '3':
            while True:
                key_matrix = hc.enter_key_matrix()
                inv = hc.nzd(key_matrix)
            
                if inv is None:
                    print("The key matrix is not valid. The determinant and modulus are not coprime.\n" \
                            "Please enter a valid key matrix.\n\n")
                else:    
                    break
            
            hc.display_matrix(key_matrix)
        elif operation == '4':
            print("Exiting the program.")
            return
        else:
            print("Invalid operation selected. Please choose '1', '2', '3', or '4'.")

main()