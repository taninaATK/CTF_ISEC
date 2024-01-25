import rsa

# Generate RSA keys with specified public exponent
(pubkey, privkey) = rsa.newkeys(2048, e=304571393049442706679267329)

# Print public and private keys
print("Public key: ", pubkey)
print("Private key: ", privkey)