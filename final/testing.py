a = []

a.append([])

a[0].append(1)

a[0].append(250)

a[0].append(3)

a[0].append(100)




a.append([])

a[1].append(4)
a[1].append(5)
a[1].append(6)

a.append([])

'''
for x in range (len(a[1])):
	print(a[1][x])

print(len(a[2]))
'''

a[0].remove(250)

for x in range (len(a[0])):
	print(a[0][x])

print('after cleaning first list')

a[0] = []

for x in range (len(a[0])):
	print(a[0][x])

print('print second list')

for x in range (len(a[1])):
	print(a[1][x])

print('add some value after clean')

a[0].append(1)

a[0].append(250)

a[0].append(3)

a[0].append(100)

print('now print first list')

for x in range (len(a[0])):
	print(a[0][x])

	