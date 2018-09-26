def e1():
    b = {}
    c = {}
    i = 1
    for x in range(1, 10):
        for y in range(1, 10):
            for z in range(1, 10):
                for a in range(1, 10):
                    aa = '{}{}{}{}'.format(x, y, z, a)
                    if x+y+z+a == 10:
                        c[i] = aa
                        i += 1
                    if x != y and x+y+z+a == 10:
                        b[i] = aa
                        i += 1
    print(c, b)



