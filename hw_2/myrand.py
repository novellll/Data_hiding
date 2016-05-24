from math import seed, sample, gauss, choice


# get a size of unique random values in a list
def random_walk(sed, im_size, msg_size):
    seed(sed+1)
    return sample(xrange(im_size), msg_size);

# get a number of random values 0,1 or -1,1 with bool check
def rand_sequece(sed, n, nonzero):
    seed(sed)
    if nonzero:
        return [choice((-1,1)) for x in xrange(n)]
    else:
        return [choice((0,1)) for x in xrange(n)]

# get Gauss distrbution in range[-5,5]
def getGaussSeq(sed,n, mean, var, bound):
    seed(sed)
    gausslist = []
    while len(gausslist) < n:
        num = round(gauss(mean, var))
        if(num <= bound and num >= -bound):
            gausslist.append(int(num))
    return gausslist

def analyzeGauss(gausslist):
    a = [0]*11
    for i in gausslist:
        a[i+5] += 1;
    return a
