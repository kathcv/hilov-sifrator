alphabet = "abcčćdđefghijklmnoprsštuvzž"
MOD = 27

convert_to_num = {char: idx for idx, char in enumerate(alphabet)}
convert_to_char = {idx: char for idx, char in enumerate(alphabet)}

def normalize_text(text):
    text = text.lower()
    result = ""

    for char in text:
        if char in convert_to_num:
            result += char
        else:
            print(f"Invalid character: {char}")
            return None

    return result;

def text_to_numbers(text):
    return [convert_to_num[char] for char in text]

def numbers_to_text(numbers):
    return ''.join(convert_to_char[num] for num in numbers)

def pad_text(text, block_size=4):
    if len(text) % block_size == 0:
        return text
    else:
        padding_length = block_size - (len(text) % block_size)
        padding = ''.join('ž' for i in range(padding_length))
        return text + padding
    
def enter_key_matrix():
    print ("Enter matrix key with dimension 4x4 for Hill Cipher:")

    key_matrix = []

    for i in range(4):
        while True:
            row_input = input(f"Enter row {i + 1} (separate numbers with space): ")
            row_values = row_input.strip().split()

            if len(row_values) != 4:
                print("Invalid input. Please enter exactly 4 integers.")
                continue
            try:
                row = [int(value) % MOD for value in row_values]
                key_matrix.append(row)
                break
            except ValueError:
                print("Invalid input. Please enter integers only.")

    return key_matrix
    
def display_matrix(matrix):
    print("Key Matrix:")
    size = len(matrix)
    print("+" + "----+" * size)
    for row in matrix:
        print("| " + " | ".join(f"{val:2}" for val in row) + " |")
        print("+" + "----+" * size)
    print()

def matrix_determinant(key_matrix, n):
    if n == 1:
        return key_matrix[0][0] % MOD
    
    if n == 2:
        return (key_matrix[0][0] * key_matrix[1][1] - key_matrix[0][1] * key_matrix[1][0]) % MOD
    
    det = 0
    sign = 1

    for col in range(n):
        minor = minor_matrix(key_matrix, 0, col)
        det += sign * key_matrix[0][col] * matrix_determinant(minor, n - 1)
        sign = -sign
    
    return det % MOD

def minor_matrix(matrix, row, col):
    return [ [matrix[i][j] for j in range(len(matrix)) if j != col] for i in range(len(matrix)) if i != row]

def nzd(key_matrix):
    determinant = matrix_determinant(key_matrix, 4)

    r1 = MOD
    r2 = determinant
    t1 = 0
    t2 = 1

    while r2 > 0:
        q = r1 //r2
        
        r = r1 - q * r2
        r1 = r2
        r2 = r

        t = t1 - q * t2
        t1 = t2
        t2 = t
    
    if r1 == 1:
        return t1 % MOD
    else:
        return None

def adjunct_matrix(matrix):
    size = len(matrix)
    adjunct = [[0] * size for _ in range(size)]

    for i in range(size):
        for j in range(size):
            minor = minor_matrix(matrix, i, j)
            sign = (-1) ** (i + j)
            adjunct[j][i] = (sign * matrix_determinant(minor, size - 1)) % MOD
            if adjunct[j][i] < 0:
                adjunct[j][i] += MOD

    return adjunct

def encode(text, key_matrix, block_size=4):
    numbers = text_to_numbers(text)

    cipher_text = ''

    for i in range(0, len(numbers), block_size):
        block = numbers[i:i+block_size]
        cipher_block = [0] * block_size

        for row in range(block_size):
            for col in range(block_size):
                cipher_block[row] += key_matrix[row][col] * block[col]
            cipher_block[row] %= MOD

        cipher_text += numbers_to_text(cipher_block)

    return cipher_text

def decode(cipher_text, key_matrix, block_size=4):
    inv_det = nzd(key_matrix)
    adj = adjunct_matrix(key_matrix)

    inv_key_matrix = [[(inv_det * adj[i][j]) % MOD for j in range(block_size)] for i in range(block_size)]
            
    decrypted_text = encode(cipher_text, inv_key_matrix, block_size)
    decrypted_text = decrypted_text.rstrip('ž')
    return decrypted_text