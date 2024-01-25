def newton_cubic_root2(n):
    if n == 0:
        return 0
    x = n
    y = (2 * x + n // (x * x)) // 3
    while y < x:
        x = y
        y = (2 * x + n // (x * x)) // 3
    return x

def extended_gcd(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0

def chinese_remainder_theorem(remainders, moduli):
    n = len(remainders)
    N = 1
    for i in range(n):
        N *= moduli[i]

    x = 0
    for i in range(n):
        Mi = N // moduli[i]
        _, Mi_inv, _ = extended_gcd(Mi, moduli[i])
        Mi_inv = Mi_inv % moduli[i]  # Calculate the modular inverse
        x += remainders[i] * Mi * Mi_inv

    return x % N

# find the modulos here : http://certificate.fyicenter.com/2145_FYIcenter_Public_Private_Key_Decoder_and_Viewer.html#Result
# and replace here
# i don't want discord to hate me
pub_keys_modulos = [int("c5c3815a03bf5a21c49210ebb14435ff88e9f6ca17796c043179b5c565dc7e9980f77a8f517311b02b53652959d5b4c666d0bcc201b42113b4b5a5ab682a59e210c6e60f969df9859c7205ea1b9a3242f8272995dec67614d903d58616ec37de6978ca9b6df3570d79c598c2c5a31dfaccbf6f5d6171b6886c79f00e208aac71ba9ed600f83fdb55ce18960efc220a31267b645f10eea1d26544570030e0145c162c86cf51274c0be5d9221899677511e4e6130509e5d8bceded8e3597d087a149cedd429b0ccde2ebdb11115a1b113a5b0cf737dea4db1e13ccfcc60deb76af6953af8cce9b80015802b210b57415941b0c5ee6465482a4f99f548022bb8887", 16), 
                    int("a0f44c79dc9bcb2f385a2fb8d5249aee05bb794f98f7a8fdbedc13db826117b3ba0b6311ae62feab430e4a5a2dd4fdb71228f5ddba08a84eb6d1a0b5c8f45f3e096a1efc9f732eb8cdf3527001d815d6e212496c848b7f08cbf4f80e9614b7a353a0a63d6cc8c00c82238870595f450f699fe60bae182db7865139e92d84085fd84f770a1325442fe0ccc26daf40703f5ec4d871047b7999e5e6b2c3b3beae62ca4c44f00f685d80b9bbef467caeffd4c4e53f27e70cfbeef54a3bc43e66a56ee3957bfedc3e734f52b50400e660404f812330cd679f32dad1924f7d1cd2d0411e042d02bf3b482cbfc81017e333eca7b468c21662c599088a4e4391754c9c01", 16),
                    int("d65df76d22dfc0f55041725bc3354eb58bae0717d8819f6dca7dc747f5448254848404a8e45f72ae7e95370e95bf56fff74edae5bc74afff6c4d82f49947a254abe87f93442510237adad625c8c9da20618e0b0013040eacc96ad8d76f1ddb35e43810be18f0c073200ccdf17977b4ac4d49625e29cec1ec3463033737c710a7873e940ea64b50ce98d644d42fabc970d6e12fb13b09756938876b9e7f64bcd33afdb25219e1c6c1d51c2e60873a4ea6d46b1a9fb1eeaf64d9ad8a40a88a9d9ea6f42929071f7e01a234490bc728564bdf726aa0a49362b4d3096583ff3d5278a374c2327a6a0ae35d2d3b513cbae12366502cdaa09da0ef249128ba903c88c9", 16)]

# give the hex you find in the books (cf : MISE À JOUR IMPORTANTE)
encrypted_passwords_hex = [
    "2bbc6abbc1a3857ef94cd0e36170feb258b7c197702a6b8b68220dcb35d3b691e9d62d853dc0c4faf95ba04a2be3a2fb9146d0037eefb933543a13fde5d549016d01b7784efa61c3ba68e6f0685c6a272dcbc4aea9ea60225f0607887537949c8e847c7d568a9af065de3cf9552fd2e23ec6b2227d0eda2f4fc12e5bc67574ab9f306e144ebba838988be1b93e876bbe7b145267c199f8e419d044a1cd2263f1e75637c4d933cbb50dd905cbdb99d58df0aa5ac6c086efd5eca701f0a5a14b5af86bd32d629b33196b70c7a963c4037156d9e1bea92b7b3944236ba220a7588fb92c1e456844f7745dd1043c7891192efd1bf6de52f2a3a82fb1ec1a3a3281de",
    "0ae47756bbf870107cf5dae6ee8bef466c1f15216603a1248c4717b593a85d216f0265adbb17a47bef1074ab88c492a4c8c10a243db3d50fe78502168ac2400f2bd6490afb277da1e5080d2c9e787466796127d3af6dd85cc15307c2ead99b4ac71969a87eef2c6c57da81e4801cb746bb574874a13aa83cf0d51b295a83a18b650b2a7ea216a49202baef19d9e9949db8fd1a64602b39a8af373817f2a7678a128484f4cda8baee529586c404aaa46a43cc81ef528f8702461d7441a6012cd8b4a1b3464a969cc491939e1fff84d6be1304c07f9a39aba25a0941a9cbbc23219763111908370ee4a314857b8f162b8515256f2ce674aaa9ce47b7720f499a99",
    "49844d92078a4abd7ec8fed5d89b07a348d785376ecb96e06813290e6d18d594c956ac2a18982ee8dadc14ba72aaec85aafade1e8d58546ebcd4da033b78f6d7598a21460da52d93ffec4c1f36838b1298827b2bb0cc54f9af64760fea2685f483fcbdfa6f7b2b8a43012639f12afea0114fa7cbbfc23cda328a4544427992ef1a0efc95cf3e28079580ee08cc44c896b869696ac466db9a1ea248d8ce0cdeb9b8cfc2069ba432a0fe07fd480804b93ade5e2a9093ae48ddb8eb205d27ddb2f2dea7b60d06fd410eadf5e59261a27553d1e50a8393dc67abdeecab6022342963ca7628953d331190346ced7db59003d25192824a61ee0d04cae053549499bd48"
]
# Convert hex to integers
encrypted_passwords_int = [int(hex_string, 16) for hex_string in encrypted_passwords_hex]
# find the m^3 mod N (you get m^3)
m_cubed = chinese_remainder_theorem(encrypted_passwords_int, pub_keys_modulos)
# do the cubic root to get (m_cubed)^(1/3)
m = newton_cubic_root2(m_cubed)
# transform to bytes
m_bytes = m.to_bytes((m.bit_length() + 7) // 8, 'big')
# you can see the password here
print("c :", m_bytes)
# find the end of the padding
padding_index = m_bytes.find(b'\x00', 2)
password_start_index = padding_index + 1
password = m_bytes[password_start_index:].decode('utf-8')
print("password: ", password)