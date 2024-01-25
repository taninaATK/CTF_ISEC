import gmpy2
import random

a = input("Give the value of a")
a = int(a, 16)
b = a + 2**1950
q = input("Give the value of q")
q = int(q, 16)
print("Val a: ", a)
print("Val q: ", q)
# ici on trouve p
if (a - 1) % q != 0:
    a += q - ((a - 1) % q)
while a < b:
    if gmpy2.is_prime(a, 20):
        break
    a += q
else:
    print("No prime p found in the given range.")
    a = None

print("p : ", a)
# puis ensuite on cherche g en mode random un peu
def find_primitive_root(p, q):
    while True:
        x = random.randint(2, p-1)
        g = pow(x, (p-1) // q, p)
        if g == 1:
            continue
        else:
            return g

print("g: ",find_primitive_root(a, q))