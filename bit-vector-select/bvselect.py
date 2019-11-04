from bitarray import bitarray
import math, sys
sys.path.insert(0, '../utils/')
sys.path.insert(0, '../bit-vector-rank/')
from total_size import total_size
from bvrank import rank_support

class select_support:

    def __init__(self, rs):
        self.rs = rs

    def select1(self, i):
        return self.__select__(i, 0, self.rs.rank1)

    def select0(self, i):
        return self.__select__(i, 1, self.rs.rank0)

    def __select__(self, i, digit, rank_func):
        left, right = 0, self.rs.n
        while left != right:
            middle = left + (right - left) // 2
            rank_m = rank_func(middle)
            if rank_m == i:
                while self.rs.bvec[middle-1] == digit:
                    middle -= 1
                return middle
            if rank_m > i:
                right = middle
            else:
                left = middle +1
        if rank_func(left) == i:
            return left
        else:
            return 0   

    def overhead(self):
        return self.rs.overhead()

def main():
    bvec = bitarray('1001011101001010')
    r = rank_support(bvec)
    s = select_support(r)
    print("input: 1001011101001010")
    print("select1(8) = {}".format(s.select1(8)))
    print("select0(8) = {}".format(s.select0(8)))
    print("overhead: {} bytes".format(s.overhead()))

if __name__=="__main__":
    main()