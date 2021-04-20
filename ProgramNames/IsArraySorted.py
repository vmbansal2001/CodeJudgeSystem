n = int(input())

a = []
for i in range(n):
    data = int(input())
    a.append(data)

prev = a[0]
flag = True
for i in range(1,n):
    if prev>a[i]:
        print("false")
        flag = False
        break
    else:
        prev = a[i]
    
if flag:
    print("true")