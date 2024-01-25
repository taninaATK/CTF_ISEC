# All this is deduced from using "hint terminal" in atrium room 112
hashed_password = 0x
ring.<x> = GF(2)['x']
Q = ring(x**64 + x**4 + x**3 + x + 1)
qring.<x> = ring.quotient(Q)
tmp = qring(x^4 + x^3 + x + 1)
I = (tmp ** (-1))

#Checking the polynomial I and its field
#print(I)
#print(I.parent())

#fill de 0 sur la gauche pour pas avoir de soucis sur le polynôme
S_coeff = bin(hashed_password).zfill(64)[2:]
S = qring(0)
po = 63

for si in S_coeff :
    if(si != '0') :
        S = S + x ** po
    po -= 1
#
#Checking that S is in the qotient ring "qring"
print(S.parent())

#cf hints : P = I*S
P = I*S
password = ''

#Getting all the coefficient in a binary string
for c in P :
    password = str(c) + password
#print(password)

password = hex(int(password, 2))[2:]
print("Password is : ", password)