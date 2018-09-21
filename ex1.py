b = {}
c = {}
i = 1
for x in range(0,10):
    for y in range(0, 10):
        for z in range(0, 10):
            for a in range(0, 10):
                if x + y+z+a == 10:
                    aa = '{}{}{}{}'.format(x,y,z,a)
                    c[i]=aa
                    # b.append(aa)
                    # print(x,y,z,a)
                    i+=1
                elif x!=y!=z!=a and x+y+z+a == 10:
                    aa = '{}{}{}{}'.format(x,y,z,a)
                    b[i]=aa

# print(aa, len(aa), i)
print(c, b)
