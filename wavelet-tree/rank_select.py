import pickle, sys
sys.path.insert(0, '../bit-vector-rank/')
sys.path.insert(0, '../bit-vector-select/')
from build import wt

def main():

    options = sys.argv[1]
    wtpath = sys.argv[2]
    ipath = sys.argv[3]
    wavelet_tree = pickle.load(open(wtpath, 'rb'))
    if options == "rank":
        rs = wavelet_tree.rank
    elif options == "select":
        rs = wavelet_tree.select
    elif options == "access":
        with open(ipath, 'r') as f:
            for line in f:
                if line == '\n':
                    break
                i = line.strip()
                print(wavelet_tree.access(int(i)))
        exit()
    with open(ipath, 'r') as f:
        for line in f:
            if line == '\n':
                break
            c, i = line.strip().split('\t')
            print(rs(c, int(i)))

if __name__=="__main__":
    main()