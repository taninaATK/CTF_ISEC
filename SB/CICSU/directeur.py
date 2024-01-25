#Laptop CISCU
from hashlib import sha256

#moi
n=int("00c8621e6170bb1fbd02d7785e9883deab1c919cf888f54fe200e4f0670bfacfdc223b8f0ccb0b3bd8d3b3bda349a8420ed8d39c3ca108a59b44573871f56921ab3ba9fdd0c7138d902ec9956c263d3a96e8a19c0a2b16bc4f69f1854300a4e4369b8674b1cb6e3992feb41cf200a402fade9c1a07b324de5dc447e8b5ae8802cea69f8cad290ce5aa00c2c455b3f3eb8f5f1f13653b3484a5dc807f8204fa9045d82f70fcc6d4cac1cd0c08f0a197f45651ffd96644e3e9686aa1bf544d3c941348e9386d1d0841a8d3954d56df198e8d8195a077cd194008fac01d68e56deddc5b08316293e5ce46b080fa52fb16238153a35f9cc0a845ec69fe84025f5332ab",16)
e=0x2914a565838e4703a759868a9d4d0ce1000000003efbe01344850cfbef81
d=int("1b0463813242929aa7e8f5cc6e2d61ca3d0da642cd17f057c88508d3233b59801638297e970e5cef58e452f6bb527ea1b54659494946db006225338ddb904964c0f0f0f7961475ab55882f4fe3830e95d2099a0499934df6d12b9749fd71d040611f85a607e09824916706766d383385aff93c863115df2836a6138eda6a1b0c36f498ed753c0fb530c74996a9dcbf5db08b56706f8b3cbc1668e4ef490976c077cad2239ac3e3ae545c4c26b5e479803e0245a3525baac1cf23f1f4aad119fd251e8ac845423deaf24b6b86cf18207de23ebe1700740f3045b36ebae426144fce56f1a38a331c5be2536db024a23fa34c349b1015d5b5b75b1f965411fda8e9",16)

#directeur
n_dir = int("00bed6cdc8f142d61854b6bddc6f9eb36bbbf4e5dab77207240078293c384eb53d4e3a0b2f250d6dd1192448973b250d563517218c90a12c0447f5b31df37410d8a2e21573c0f05a8aa9924114708053b08878d3b53ccd35ba3516c02c3692d048ad46e98b7fbe13a99b4670fcc96dd51e7a04a3da93493ab5b5b0ff7ae77708d74f8c964112523fed59c1bdc949bfea248ff0a39285302b0292a6b8de23f98a920135cf1b5660e16eb4fddbb24b4312ef5c59f4a02a67dff2b28a6d1b0c3e3942c1736faa43a94f0995e04bda6c873a1cbaf6685424196abc6185d3e40fc1cc276fae72de0465d9748e6eb7e165b62800a53f2c67e4693cc92b37a9ee4bc449e9",16)
e_dir = 65537

# SHA-256 
HASH_ID = b'010\r\x06\t`\x86H\x01e\x03\x04\x02\x01\x05\x00\x04 ' 


def i2osp(x : int, k : int) -> bytes: 
    """ 
    Convert the integer x to a sequence of k bytes 
    """ 
    return x.to_bytes(k, byteorder='big') 

def os2ip(x : bytes) -> int: 
    """ 
    Convert the sequence of bytes to an integer 
    """ 
    return int.from_bytes(x, byteorder='big') 

def emsa_pkcs1_encode(M : bytes, k : int) -> bytes: 
    """ 
    Encode a message into k bytes for RSA signature 
    """ 
    h = sha256(M) 
    T = HASH_ID + h.digest() 
    if len(T) + 11 > k: 
        raise ValueError("Message Too Long") 
    PS = bytes([0xff] * (k - len(T) - 3)) 
    EM = bytes([0x00, 0x01]) + PS + bytes([0x00]) + T 
    return EM 

def emsa_pkcs1_decode(EM : bytes, k : int) -> bytes: 
    """ 
    Given an EMSA_PKCS1-encoded message, returns the Hash 
     
    >>> x = emsa_pkcs1_encode("toto", 128) 
    >>> emsa_pkcs1_decode(x, 128) == sha256("toto".encode()).digest() 
    True 
    """ 
    if len(EM) != k: 
        raise ValueError("Incorrect Size") 
    if EM[:2] != bytes([0x00, 0x01]): 
        raise ValueError("Incorrect Header") 
    i = 2 
    while EM[i] != 0: 
        if EM[i] != 0xff: 
            raise ValueError("Incorrect Filler") 
        i += 1 
        if i == k: 
            raise ValueError("Only Filler") 
    if i < 10: 
        raise ValueError("Not enough filler") 
    T = EM[i+1:] 
    if T[:len(HASH_ID)] != HASH_ID: 
        raise ValueError("Bad Hash ID") 
    H = T[len(HASH_ID):] 
    return H 

def key_length(n : int) -> int: 
    """ 
    key length in bytes 
    """ 
    return (n.bit_length() + 7) // 8 

def rsa_pkcs_sign(n : int, d : int, M : bytes): 
    """ 
    RSA Signature using PKCS#1 v1.5 encoding 
    """ 
    k = key_length(n) 
    EM = emsa_pkcs1_encode(M, k)
    m = os2ip(EM)
    s = pow(m, d, n)
    S = i2osp(s, k)
    return S

def rsa_pkcs_sign2(n, d, M):
    """
    RSA Signature using PKCS#1 v1.5 encoding
    """
    k = key_length(n)
    #EM = emsa_pkcs1_encode(M, k)
    m = os2ip(bytes.fromhex(M))
    s = pow(m, d, n)
    S = i2osp(s, k)
    return S.hex()

    
def rsa_pkcs_verify(n : int, e : int, M : bytes, S : bytes) -> bool: 
    """ 
    Verify RSA PKCS#1 v1.5 signatures 
    """ 
    k = key_length(n) 
    if len(S) != k: 
        raise ValueError("Bad length") 
    s = os2ip(S) 
    m = pow(s, e, n) 
    EM = i2osp(m, k) 
    H = emsa_pkcs1_decode(EM, k) 
    return (H == sha256(M).digest()) 
#print("============================")
#print(int("0a9e6bee97e1b0953b5bc0786272ef470b043e09b40bc8e9884f4920ff8d93b225528f8ed04effa6005b18c640b7f623bd4a4e9f07cf8f9b1c587f0559439e6a7e9a77ded85aa86bbecdc4a8d5c47fc86a6f72edec96bc74c199f8eb609891bcd153db0edd33efab85dec97ccdf9c05b2f53d958a7f31101158db1ca300084e6c923cd496e23e73d979af525d57e353ebfbf31354d96ebf39ba17cf0002be1fcca7e51e538880c4daa5c318b831939523a0fbe596550c96484b3e0eb685fa713ddff78e840ba718f0e933163ab15d236684ef4050faf4a38be2646727249fc7790dcb8591b3f3b4e68c450e097913256b21b88177ea4260f71a6ef5d7ddc59a4",16))
#print(int("7c0b5b17abb9442cbe6d83a014eba13f18904488c26b6b74ceac3cb7bfdd3f2161e60c9d59a940fbaa9cc7976764eeb9ff989cb0b046d25f840168b45f17232ed4071d12aef39572e367c5c50102fdb8771e1ebfe84484fd90a86321601036b778c06b9fff27abde731c6c00887c91d575305d7ec6b0cc44d341b089eb44e303fdcf62230c25e076bdab910246941ff01e6053ede3b68a4c77e1e28fee25757204bc2453ffa02db45d801e15dcc5331496cfd033ae84063795d25105b080e7d5017c077d8ee7af1987edb78d7484b6ab2e51e291d23154eeb7873144d14740c14a5a8335d2f225f76fdc70cc24016d358bdf0fa373bb7cffceb71ab71a72fcb2",16))
#print("============================")


msg="I, the lab director, hereby grant tanina permission to take the BiblioDrone-NG."
msg_bin = msg.encode('ascii')

M= emsa_pkcs1_encode(msg_bin, key_length(n_dir))
#print(key_length(n_dir))

x= b"a"
M_i = os2ip(M)
x_i = os2ip(x)

conf_i = (M_i*pow(x_i, e_dir)) % n_dir #conf = confusion
conf_hex = hex(conf_i)[2:]
print(conf_hex)
signee_hex = input("Donne moi signature hex\n")
signee_bytes = bytes.fromhex(signee_hex)
signee_i = os2ip(signee_bytes)
signee_i = signee_i*(pow(x_i, -1, n_dir)) %n_dir
signeevrai_bytes = i2osp(signee_i, key_length(n_dir))
print("Resultat est: "+signeevrai_bytes.hex())
res = rsa_pkcs_verify(n_dir, e_dir, msg_bin, signeevrai_bytes)
print(res)