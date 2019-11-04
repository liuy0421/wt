from bitarray import bitarray
import math, sys
sys.path.insert(0, '../utils/')
from total_size import total_size

class rank_support:

    def __init__(self, bvec):
        self.bvec, self.n = bvec, len(bvec)
        self.s = max(1, math.ceil(math.log(self.n, 2)**2/2))
        self.b = max(1, math.ceil(math.log(self.n, 2)/2))
        self.p = math.ceil(math.log(self.b+1, 2))
        self.numberOfRs = math.ceil(self.n/self.s)
        self.bPerS = math.ceil(self.s/self.b)
        self.numberofBs = self.numberOfRs*self.bPerS
        self.bitsPerS = math.ceil(math.log(self.n, 2))
        self.bitsPerB = math.ceil(math.log(self.s, 2))
        self.Rs = [bitarray('0'*self.bitsPerS) for x in range(self.numberOfRs)]
        self.Rb = [bitarray('0'*self.bitsPerB) for x in range(self.numberofBs)]
        self.Rp = dict()
        # initialize Rs
        for i in range(self.n):
            block = i // self.s
            if self.bvec[i] and block+1 < self.numberOfRs:
                for j in range(block+1, self.numberOfRs):
                    self.__increment__(self.Rs[j], self.bitsPerS-1)
        # initialize Rb
        for i in [x for x in range(self.n) if x % self.s == 0]:
            b0 = i // self.s * self.bPerS 
            for j in range(self.bPerS-1): 
                self.Rb[b0+j+1] = self.Rb[b0+j].copy() # copy over 
                for bit in self.bvec[i+j*self.b:i+(j+1)*self.b]:
                    if bit:
                        self.__increment__(self.Rb[b0+j+1], self.bitsPerB-1)
        # initialize Rp
        for i in range(2**self.b+1):
            num = i
            num_vec = bitarray('0'*self.b)
            for j in range(self.b):
                num_vec[self.b-1-j] = num % 2
                num //= 2
            self.Rp[num_vec.to01()] = [bitarray('0'*self.p) for x in range(self.b)]
            for j in range(self.b):
                if num_vec[j]:
                    for k in range(j, self.b):
                        self.__increment__(self.Rp[num_vec.to01()][k], self.p-1)
            
    def overhead(self):
        size_Rs = total_size(self.Rs)
        size_Rb = total_size(self.Rb)
        size_Rp = total_size(self.Rp)
        return size_Rs + size_Rb + size_Rp

    def __rank1__(self, i):
        rs_i = i // self.s
        rb_i = rs_i * self.bPerS + (i % self.s) // self.b
        bi = rb_i % self.bPerS
        rp_i = self.bvec[rs_i*self.s+bi*self.b : \
                         min((rs_i+1)*self.s, rs_i*self.s+(bi+1)*self.b)]
        rp_j = i % self.s % self.b
        while len(rp_i) < self.b:
            rp_i.insert(len(rp_i), False)
        return self.Rs[rs_i], self.Rb[rb_i], self.Rp[rp_i.to01()][rp_j]
        
    def rank1(self, i):
        i = i-1
        rs, rb, rp = self.__rank1__(i)
        return self.__vec2int__(rs) + \
               self.__vec2int__(rb) + \
               self.__vec2int__(rp)

    def rank0(self,i):
        return i - self.rank1(i)

    # increment without worrying about overflow
    def __increment__(self, bvec, i):
        bvec[i] = not bvec[i]
        if not bvec[i]:
            self.__increment__(bvec, i-1)

    def __vec2int__(self, bvec):
        num = 0
        for i in range(len(bvec)):
            num *= 2
            if bvec[i]:
                num += 1
        return num

def main():
    bvec = bitarray('1001011101001010')
    r = rank_support(bvec)
    print("input: 1001011101001010")
    print("rank1(8) = {}".format(r.rank1(8)))
    print("rank0(8) = {}".format(r.rank0(8)))
    print("overhead: {} bytes".format(r.overhead()))

if __name__=="__main__":
    main()