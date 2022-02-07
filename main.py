import string, random
from matplotlib import pyplot as plt
import numpy as np
from des import *

def hamming_distance(a, b):
	return sum([(u != v) for u, v in zip(a, b)]) + abs(len(b) - len(a))

def hd_des_rounds(a, b):

	return [hamming_distance(u[0] + u[1], v[0] + v[1]) for u, v in zip(a, b)]

def rand_str(size, alphabet=[0,1]):
	return ''.join(map(str, [random.choice(alphabet) for i in range(size)]))


def hd_str(hd, src, alphabet=[0,1], skip=-1):
	src = string_to_bit_array(src)
	if skip == -1:
		skip = len(alphabet)

	pos = set(random.sample([i for i in range(len(src)) if i%skip != skip-1], hd))

	return bit_array_to_string([random.choice(alphabet) if i in pos else src[i] for i in range(len(src))])

def plot(data, title, xlabel, ylabel):
	data = np.array(data)
	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.boxplot(data)
	plt.show()


PLAIN_TEXT_LEN = 8
KEY_LEN = 8
ALPHABET = string.ascii_letters
des = des()


# a. 5 diff plain texts
src = rand_str(PLAIN_TEXT_LEN, ALPHABET)
key = rand_str(KEY_LEN, ALPHABET)


texts = set()
while len(texts) < 5:
	texts.add(hd_str(1, src))

_, src_rounds= des.encrypt(key, src)
text_rounds = [des.encrypt(key, text)[1] for text in texts]

hd_rounds = [hd_des_rounds(src_rounds, text_round) for text_round in text_rounds]

plot(hd_rounds, "5 different plain texts with hamming distance 1", "rounds", "hamming distance")


# b. 5 diff hamming distances
texts = set()
for hd in range(1, 6):
	texts.add(hd_str(hd, src, skip=8))

_, src_rounds= des.encrypt(key, src)
text_rounds = [des.encrypt(key, text)[1] for text in texts]

hd_rounds = [hd_des_rounds(src_rounds, text_round) for text_round in text_rounds]

plot(hd_rounds, "5 different hamming distances [1,2,3,4,5]", "rounds", "hamming distance")


# c. 5 different keys
keys = set()
while len(keys) < 5:
	keys.add(hd_str(1, key))



_, key_rounds = des.encrypt(key, src)
keys_rounds = [des.encrypt(k, src)[1] for k in keys]
hd_rounds = [hd_des_rounds(key_rounds, k_round) for k_round in keys_rounds]

plot(hd_rounds, "5 different keys with hamming distance 1", "rounds", "hamming distance")

