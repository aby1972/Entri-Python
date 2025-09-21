l=[50,40,30,20,10]
c=len(l)
j=0
m=0
print(l)
for i in range(c-1,-1,-1):
    m=l[c-1]
    l.pop()
    l.insert(j,m)
    j+=1
print(l)