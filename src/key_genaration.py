def P_10(key):
    """
    Performs the P10 permutation on a 10-bit key.
    """
    return [key[2], key[4], key[1], key[6], key[3], key[9], key[0], key[8], key[7], key[5]]

def circular_left_shift(key):
    """
    Performs a circular left shift (LS-1) on both halves of a 10-bit key.
    """
    left  = key[:len(key)//2]
    right = key[len(key)//2:]

    left = left[1:] + left[:1]
    right = right[1:] + right[:1]

    return left+right

def P_8(key):
    """
    Performs the P8 permutation on a 10-bit key.
    """
    return [key[5], key[2], key[6], key[3], key[7], key[4], key[9], key[8]]

def s_des_generation_keys(key):
    """
    Generates the K1 and K2 keys for the S-DES encryption algorithm.
    """
    key_P10 = P_10(key)
    key_P10 = circular_left_shift(key_P10)
    k1 = P_8(key_P10)

    key_P10 = circular_left_shift(key_P10)
    key_P10 = circular_left_shift(key_P10)
    k2 = P_8(key_P10)

    return k1, k2
