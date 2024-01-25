flags = [
            '785b08f2cc9279d9ec63bbe0e7a9437cc71f1523e21e8a6ebab24b9e03c4f77d',
            '17fc028d76b9e6a8f0dee80b451b36b2b2d679bec0bb8e15bb742ae206105491',
            'dceefa0f7904151718d3a5e9b926387352aac8cdee5145a5bf3e1f2476c9887a',
            'ce706d374b38790e5f2ea50c64a941027e599259cc36abcc3451b7e86f1f719b',
            '0f41bae3325725af2c7daf3bbccfc3698aa2df1dc393a140a87b471bc3c7d0c2',
            '46fc0da9fc4cde879c475bd27eb9c299c7d99d736ea21ddfa06b449ce7c89d15',
            'e2bde338539610d10dd02f9f6cf0fef831c5070f9f578af8c984bdab7aa06026',
            '759cd273a2cf1fc916839ecb51167c81aee11b74ce2e5ef59be8302ecee6bafa',
            'ff2bebb2c9e27d1ebd71bffa9a9db7f978193bd429756430d7530358c6074313',
            'bcba922d648ef0bf3e655cabbd137e9823b953e72438612576c57f0d764287e6',
            'f700ca549660553b2d6f0af571fb3c8ccc8325503e8589544cdc7d0a9e72ae42',
            '7de33e41c0aaacecd9a5cf3ce923c4b7cfab825aee81ae825bef005722ebc7e2',
            '8c5206de1f277bd5e56231c4018a53df65b659211abd09fae20ceed32b494257',
            '132db77dd0865bbf2c1074a2d01301b98b11212a4d3c8d3b006ecb30fe34bfda',
            'f1d92c93eab8f60f348c3509390de264cdd27236071c60409cba1e11f9239583',
            '705bb8ce44640204eaece022212b06d21583b134e88d4f8c34290df0c48bf058',
            'd5e668386fb55d21691e977b19243511c227d99fb7bc4cff6503f1c1e2a4af8f',
            '09f6f41754cbc4bdf999b57afcc18b89d00d97a2b1bfdf03c3eda5885f2531df'
        ]

#Cf la doc sur le security engine, 2 parties trouvées dans le batiment ATRIUM

p = (2**64) - 59;

F = GF(p);
P = F['x'];

A = [];
B = [];

for f in flags :
    # A = [(x0, R(x0)), ..., (xn, f(xn))]
    A.append((ZZ('0x' + f[0:16]), ZZ('0x' + f[16:32])));
    B.append((ZZ('0x' + f[0:16]), ZZ('0x' + f[32:49])));
#
# Ici R est bien de degré 8
R = P.lagrange_polynomial(A[0:9])
#print(R)

#Ici S est bien de degré 16
S = P.lagrange_polynomial(B[0:17])
#print(S)

print()
print("R0 = ", hex(R[0])[2:])
print("S0 = ", hex(S[0])[2:])