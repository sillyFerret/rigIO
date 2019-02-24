class PowTwo:
    """Class to implement an iterator
    of powers of two"""

    def __init__(self, max = 0):
        self.max = max

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n <= self.max:
            result = 2 ** self.n
            self.n += 1
            return result
        else:
            raise StopIteration

    def __len__(self):
        for i in self.__iter__():
            pass
        return self.n

    def __contains__(self, value):
        for i in self.__iter__():
            if value == i:
                return True
        return False

if __name__ == '__main__':
    a = PowTwo(4)
    for i in a:
        print(i)
    print(16 in a)
