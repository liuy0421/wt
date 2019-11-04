import sys, math, pickle
from bitarray import bitarray
import numpy as np
sys.path.insert(0, '../bit-vector-select/')
sys.path.insert(0, '../bit-vector-rank/')
from bvrank import rank_support
from bvselect import select_support

class wt:

    def __init__(self, input_string):
        self.input_string = input_string
        self.n = len(self.input_string)
        alphabet = list(set(input_string))
        alphabet.sort()
        self.Sigma_size = len(alphabet)
        self.Sigma = dict()
        self.binary = dict()
        self.l = math.ceil(math.log(self.Sigma_size, 2))
        # initialize mappings
        for i in range(self.Sigma_size):
            num = i
            num_vec = bitarray('0'*self.l)
            for j in range(self.l):
                num_vec[self.l-1-j] = num % 2
                num //= 2
            self.Sigma[alphabet[i]] = num_vec
            self.binary[num_vec.to01()] = i
        self.bvs = []
        to_process = [input_string]
        # initializing levels in the wavelet tree
        for level in range(self.l):
            next_level = []
            for item in to_process:
                if item != []:
                    bv = bitarray(''.join([self.Sigma[x].to01()[level] for x in item]))
                    r = rank_support(bv)
                    self.bvs.append((r, select_support(r)))
                else: 
                    self.bvs.append(None)
                if level < self.l-1: 
                    left = [x for x in item if not self.Sigma[x][level]]
                    right = [x for x in item if self.Sigma[x][level]]
                    next_level.append(left)
                    next_level.append(right)
            to_process = next_level

    def access(self, i):
        if i >= self.n:
            sys.exit("invalid index")
        return self.input_string[i]

    def select(self, c, i):
        return self.__select__(self.Sigma[c], i, 0, 0)

    def __select__(self, c, i, level, bv_index):
        r, s = self.bvs[bv_index]
        if level == self.l-1:
            if c[level]:
                return s.select1(i)
            else:
                return s.select0(i)
        if c[level]:
            target = self.__select__(c, i, level+1, 2*bv_index+2)
        else:
            target = self.__select__(c, i, level+1, 2*bv_index+1)
        if c[level]:
            return s.select1(target)
        else:
            return s.select0(target)

    def rank(self, c, i):
        return self.__rank__(self.Sigma[c], i, 0, 0)

    def __rank__(self, c, i, level, bv_index):
        r, s = self.bvs[bv_index]
        if c[level]:
            cumsum = r.rank1(i)
            target = 2*bv_index+2
        else:
            cumsum = r.rank0(i)
            target = 2*bv_index+1
        if level == self.l-1:
            return cumsum
        return self.__rank__(c, cumsum, level+1, target)

def main():
    if len(sys.argv) != 3:
        sys.exit('wrong number of arguments')
    else:
        inpath = sys.argv[1]
        outpath = sys.argv[2]
    with open(inpath, 'r') as f:
        input_string = f.readline().strip().replace(' ', '_')
    wavelet_tree = wt(input_string)
    pickle.dump(wavelet_tree, open(outpath, 'wb'))

if __name__=="__main__":
    main()