def test():
    aa=['a','b','c','d','a','a','a']
    for i in aa:
        if i=="a":
            aa.remove(i)
            print(aa)
    print(aa)

if __name__ == '__main__':
    test()