from math import gcd #for gcd function (or easily implementable to avoid import)
import random #for random elements drawing in RecoverPrimeFactors

def failFunction():
	print("Prime factors not found")

def outputPrimes(a, n):
	p = gcd(a, n)
	q = int(n // p)
	if p > q:
		p, q = q, p
	print("Found factors p and q")
	print("p = {0}".format(str(p)))
	print("q = {0}".format(str(q)))
	return p,q


def RecoverPrimeFactors(n, e, d):
	"""The following algorithm recovers the prime factor
		s of a modulus, given the public and private
		exponents.
		Function call: RecoverPrimeFactors(n, e, d)
		Input: 	n: modulus
				e: public exponent
				d: private exponent
		Output: (p, q): prime factors of modulus"""

	k = d * e - 1
	if k % 2 == 1:
		failFunction()
		return 0, 0
	else:
		t = 0
		r = k
		while(r % 2 == 0):
			r = int(r // 2)
			t += 1
		for i in range(1, 101):
			g = random.randint(0, n) # random g in [0, n-1]
			y = pow(g, r, n)
			if y == 1 or y == n - 1:
				continue
			else:
				for j in range(1, t): # j \in [1, t-1]
					x = pow(y, 2, n)
					if x == 1:
						p, q = outputPrimes(y - 1, n)
						return p, q
					elif x == n - 1:
						continue
					y = x
					x = pow(y, 2, n)
					if  x == 1:
						p, q = outputPrimes(y - 1, n)
						return p, q

N = 0x00c8621e6170bb1fbd02d7785e9883deab1c919cf888f54fe200e4f0670bfacfdc223b8f0ccb0b3bd8d3b3bda349a8420ed8d39c3ca108a59b44573871f56921ab3ba9fdd0c7138d902ec9956c263d3a96e8a19c0a2b16bc4f69f1854300a4e4369b8674b1cb6e3992feb41cf200a402fade9c1a07b324de5dc447e8b5ae8802cea69f8cad290ce5aa00c2c455b3f3eb8f5f1f13653b3484a5dc807f8204fa9045d82f70fcc6d4cac1cd0c08f0a197f45651ffd96644e3e9686aa1bf544d3c941348e9386d1d0841a8d3954d56df198e8d8195a077cd194008fac01d68e56deddc5b08316293e5ce46b080fa52fb16238153a35f9cc0a845ec69fe84025f5332ab
e1 = 0x00ff4232729a756f36d228e822a2eb2d9d0000000000003efbe01344850cfbef81
d1 = 0x6047ce49f1a7f2739ecf14bbd35b23db20e8c9ce5e6743d33adc029cfbd7797a2e83c7685cf48396621d2fd2610bcfd51de5511605c75f40b96ae65f1d9213888c11d81792137a410282d882c5d0c984081fa2bb95e6a53dcf832b98c6f5295c770c8c7b03fb007e6c8ce6ccb2d811aec53154393a4d3042fdb30a3c3616e903a1dc84c60db84448e25c47fdd0615b36caa767a46ae69ee0d560e2d00cc179fc8e1a82bde5628d06c352dd891e423009da01f92a241ad4ff5fa7041651d45c72524ce97f91019005e8ce307a91705ccdc57ecc848814af9b7506991b45dc522cbb4fb3425a3657b3bfbb9338fda594831a2ff510d983b16fdf7cb0b5c2ae6819
e2 = 0x2914a565838e4703a759868a9d4d0ce1000000003efbe01344850cfbef81
print("e1 : ", e1)
print("d1 : ", d1)

random.seed(42)
p, q =  RecoverPrimeFactors(N, e1, d1)

print("p = ", p)
print("q = ", q)
print("e2 = ", e2)
print("d2 =", pow(e2, -1, (p-1)*(q-1)))