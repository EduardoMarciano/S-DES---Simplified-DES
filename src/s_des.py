from key_genaration import s_des_generation_keys

# S0 and S1 tables used for the S-DES substitution step
S0 = [["01", "00", "11", "10"],
      ["11", "10", "01", "00"],
      ["00", "10", "01", "11"],
      ["11", "01", "11", "10"]]

S1 = [["00", "01", "10", "11"],
      ["10", "00", "01", "11"],
      ["11", "00", "01", "00"],
      ["10", "01", "00", "11"]]

def binary_to_decimal(n):
    """Converts a binary string to its decimal equivalent."""
    decimal = 0
    for i, bit in enumerate(reversed(n)):
        decimal += int(bit) * (2 ** i) 
    return decimal

def exclusive_or(n0, n1):
    """Performs a bitwise exclusive OR operation between two binary bits."""
    if n0 == n1:
        return "0"
    else:
        return "1"

def IP(block):
    """Initial Permutation (IP) rearranges the input block in a specific arrange"""
    return [block[1], block[5], block[2], block[0], block[3], block[7], block[4], block[6]]

def FP(block):
    """Final Permutation (FP) is equivalent to the inverse function of IP"""
    return [block[3], block[0], block[2], block[4], block[6], block[1], block[7], block[5]]

def EP(key, block):
    """Expansion Permutation (EP) expands and XORs a 4-bit block with an 8-bit key"""
    return [exclusive_or(block[3], key[0]), exclusive_or(block[0], key[1]), exclusive_or(block[1], key[2]), exclusive_or(block[2], key[3]), 
            exclusive_or(block[1], key[4]), exclusive_or(block[2], key[5]), exclusive_or(block[3], key[6]), exclusive_or(block[0], key[7])]

def P_4(block):
    """Performs the P4 permutation on a 4-bit block."""
    return [block[1], block[3], block[2], block[0]]

def F(key, block):
    """F function applies EP, S-box substitutions, and P4 permutations to a 4-bit block."""
    block = EP(key, block)

    row_S0    = (binary_to_decimal(block[0] + block[3]))
    column_S0 = (binary_to_decimal(block[1] + block[2]))
    row_S1    = (binary_to_decimal(block[4] + block[7]))
    column_S1 = (binary_to_decimal(block[5] + block[6]))
    
    return P_4(S0[row_S0][column_S0] + S1[row_S1][column_S1])

def Fk(key, block):
    """Fk function applies XOR on the output of F with the left half of the block."""
    left = block[:4]
    right = block[4:]

    f_result = F(key, right)
    left_result = []
    for i in range(len(left)):
        left_result = left_result + [exclusive_or(left[i], f_result[i])]

    return left_result + right

def SW(block):
    """Switches the left and right halves of the block."""
    return block[4:] + block[:4]

# Original 10-bit key
key = ["1","0","1","0","0","0","0","0","1","0"]
# Original 8-bit block
block = ["1","1","0","1","0","1","1","1"]
# The two subkeys generated
k1, k2 = s_des_generation_keys(key)

cipher_text = FP(Fk(k2, SW(Fk(k1, IP(block)))))
plain_text = FP(Fk(k1, SW(Fk(k2, IP(cipher_text)))))

print(f'Key K1: {k1}, Key K2: {k2}')
print(f'Cipher Text: {cipher_text}')
if plain_text == block:
    print(f'Success! The decryption was successful, and the original block matches the decrypted plaintext.')
else:
    print(f'Error: The decryption failed. The original block does not match the decrypted plaintext.')
