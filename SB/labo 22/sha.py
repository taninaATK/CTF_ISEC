from hashlib import sha256
import codecs

def key_expansion(seed : bytes) -> bytes:
    """
    Renvoie 256 bits pseudo-aléatoires à partir de seed
    """
    state = seed
    output = b''
    for i in range(8):
        state = sha256(state).digest()
        output += state[:4]
    return output

"""
    Doc UGLIX => SEED SUR 16 BITS = 4 OCTETS DONC ON FORCE BRUTE CA
"""

seed = 0x0000
goal = 'af11a260875629b708243ecaebb3dc6c'

while(seed <= 0xffff) :
    seed2 = hex(seed)
    seed2 = seed2[2:].zfill(4)
    key_material = key_expansion(codecs.decode(seed2, 'hex_codec'))
    K = key_material[0:16]
    IV = key_material[16:32]
    if(IV.hex() == goal) :
        print(K.hex(), "\n")
        break
    seed +=1