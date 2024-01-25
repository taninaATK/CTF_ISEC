from binascii import hexlify, unhexlify
import codecs

n = 0x00be0866259770b85939e51befe3d7cc80afb08b044c9bd892a1bbbcda848207cdbfc2137d54ccab8658019c2f689443d442a955bbc25652ab8a7bbd106ee7a0ee53b6b9b54d151692784e43821c508772c392919ea509d5784d0784866e19527a4bc7c0feca7ac210d43de3401f16b4a9bd270f986a394f8ace0ff3cdb4169fda0c4eab2de6b70ec0202822fe1a88aecacf14bab6e67c9d7b41c091a18bb8ec60c536718a543777bc65064fb11580b4b0fa5a7293abb512f67980100909cc793bd1d1cfd77f6c758b8f34b69d58d7337f13108948fce90ddf7d711e6074a194dddb4ef704238046f1408a711a15960c6bb49ed279a83bfd63ad123e02bac50e07

"""
    Noms des membres histoire de pas oublier
    1 = diane
    2 = kelsey
"""

e1 = 0x5265a7bbd0a045ec9bbcbbcb6ad26b07000000003efbe01344850cfbef81
e2 = 0x7e72bff39c08801c94338dedd78b5833000000003efbe01344850cfbef81

c1 = 0x522ed9d55cab443c9fee7c58e0e00fa6a0fb5d61063e9777ef28247413356d0945100d2b7f3855df7d14f83d4077e463071c27fa8e143a11160443708f8d5e1affab7490fc2019a2d608a6ea56872259564a712b42bae4cfca936613047a857fefa79aa00d97440aee1a5ff49fce9aeb3dc5d45faf4f07a33c33b6961feca17c82f5bbe10d2b0c5d771d3e719608b76b60c67a3b3d13ffdab1d8b4ef687fd10ac3183ad4671a892e9bdd73e56e323c1d5ff55bb7e61ef0e9cb49cff4f62a3c2b68a9a4c6cf8b2dceda4e41170130cdf429fd875e0ea8f7e533fe6dbe25b96e8fd0a9035e5661c35a499b4cdeab26301b6fad151988e82d385337c2938c76edf5
c2 = 0x61f50e5d78b46c2ec6dcf469dbabeb009aab7ce7dd4c037ac424d98ff8dbdf47a898b9f3b5349c7bad95c10fac0c6dbb26614049f4a201e358a2a939eecd7bae8c34090add9c80a2d2378f32dbfcd85ae693f08741616241105aa786916c93a7804d669a6e17039755f4c4d9c6e9938420e029083a458d3cbb1c756326330ff4ceeca0a1dd626b46deed8d72717e636907b91163f6e169504bc26c4639afac5872fbed63adc51f179c1420727cc2fcca3457763b075773488f3c1ee88072b34ce4d786976d545b55c0760c37ec0e60fcb00bd0867375afb3ad0b3841a120c532561150fbf4da30f01717fddb234b53675e9b6ab15719d3f1282595b105ad4135

#Extended Euclidean Algorithm
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


g, u, v = egcd(e1, e2)

m = pow(c1, u, n)*pow(c2, v, n) % n
m_bytes = m.to_bytes((m.bit_length() + 7) // 8, 'big')
# you can see the password here
#print("c :", m_bytes)
# find the end of the padding
padding_index = m_bytes.find(b'\x00', 2)
password_start_index = padding_index + 1
password = m_bytes[password_start_index:].decode('utf-8')
print("password: ", password)