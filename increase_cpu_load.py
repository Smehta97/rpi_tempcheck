import argparse

def fib(n):
    if n == 1:
        return 1
    elif n == 2:
        return 1
    else:
         return fib(n-1) + fib(n-2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int)
    args = parser.parse_args()
    if args.n:
        print(fib(args.n))
    else:
        print('Usage: -n sum high-ish integer')