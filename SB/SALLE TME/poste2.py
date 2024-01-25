import gmpy2
import random
from sympy import randprime

def find_generator(p, factors):
    phi = p - 1
    #Search randomly a generator 1000 times, if not found, we change p
    for i in range(1000):
        g = random.randint(2, phi-1)
        if all(pow(g, (phi // q), p) != 1 for q in factors):
            return g
    return 0

a = input("Give the value of a")
a = int(a, 16)
b = a + 2**1950
q = input("Give the value of q")
q = int(q, 16)

#Range of r for p to be in a<=p<b
r_start_interval = (a-1) // (2*q)
r_end_interval = (b-1) // (2*q)

print("Val a: ", a)
print("Val q: ", q)
i = 1
g = 0

while (g == 0):
    p = 0
    #loop until we find p and r prime such that p = 2*q*r + 1 => (p-1) = 2*q*r 
    while(not gmpy2.is_prime(p, 25)):
        #print("Try number ", i)
        r = randprime(r_start_interval, r_end_interval)
        p = r * q * 2 + 1
        #i += 1
    print("Val p: ", p)
    g = find_generator(p, [2, r, q])

print("r :", r)
print("g: ", g)