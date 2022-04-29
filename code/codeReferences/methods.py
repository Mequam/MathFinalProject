#this file contains misclanious methods seperated for convinecnce
#each method is inteanded as a standalone functioning THING
from random import random as randf
import vector as v

def genRandPoints(x,y,n=64):
	#glorious array syntax :)
	ret_val = []
	for i in range(0,n):
		ret_val.append(v.Vector([randf()*x,randf()*y]))
	return ret_val
if __name__ == '__main__':
	for point in genRandPoints(10,10,100):
		print(point)
