from PIL import Image
from random import choice, seed, randint

ALPHA = 6
C = 30
SN = 62
img_size = 512
lena_img = "Lena_Gray.tiff"
monkey_img = "Baboon_Gray.tiff"
save_img = "result.tiff"
secret_list = list()

		char *arg[] = {"ls", "-al\n",0};
seed((1,))
def printArgument(se, loc, rate):
	print "ALPHA: %d\tSpread number: %d " %(ALPHA, C)
	print "Secret data len: %d \nSecret data:" %SN, se 
	print "Generate random location : %d, w: %d h: %d" \
		%(loc, loc//img_size, loc%img_size)
	print "Correct Rate: %.4f" %(rate)
	
def getRandLoc():
	ri = randint(0, img_size**2- C * SN)

	return ri


def hide(img, se, pn, nimg, loc):
	hid_len = len(pn)
	for i in xrange(loc, loc + hid_len):
		w = i // img_size
		h = i % img_size
		val = img.getpixel((w, h)) + se[i - loc] * pn[i-loc] * ALPHA
		nimg.putpixel((w, h), val)
	nimg.save(save_img)

def getrdlist(n):
	rl = [choice((1, -1)) for x in xrange(n)]
	return rl

def expandList(l):
	el = list()
	for index in xrange(len(l)):
		for x in xrange(C):
			el.append(l[index])
	return el

def solveImg(img, exp_se, pn, se, loc):
	info = list()
	hid_len = len(pn)
	mysum, count = 0, 0
	for i in xrange(loc, loc + hid_len):
		w = i // img_size
		h = i % img_size
		mysum += img.getpixel((w, h)) * pn[i - loc] 
		if (i-loc + 1) % C == 0 :
			if mysum > 0:
				info.append(1)
			else:
				info.append(-1)
			mysum = 0
	return checkRate(info, se)


				
def checkRate(info, se):
	correct = 0.0
	for i in xrange(len(info)):
		if se[i] == info[i]:
			correct += 1
	rate =  correct * 100 / len(info)
	return rate


if __name__ == '__main__':
	se = getrdlist(SN)
	exp_se = expandList(se)
	pn = getrdlist(SN * C)
	loc = getRandLoc()
	img = Image.open(monkey_img)
	nimg = img.copy()
	hide(img, exp_se, pn, nimg, loc)
	h_img = Image.open(save_img)
	rate = solveImg(h_img, exp_se, pn, se, loc)
	printArgument(se, loc, rate)
