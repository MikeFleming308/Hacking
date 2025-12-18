
numList = []
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
regoList = []

print(alphabet)

# Create a list of numerical chars as strings (1,000). Three digits each, padded with zeroes.
for i in range(0, 1000):
    j = str(i)
    if len(j) == 1:
        k = "00" + j
    elif len(j) == 2:
        k = "0" + j
    else: 
        k = j
    numList.append(k)

for i in "A":  # Using "AB" resticts the list to 1,352,000. "ABC" = 2,028,000
    # "A" produces 676,000 rego codes (000AAA to 999AZZ)
    # "AB" produces 1,352,000 rego codes (Each additional letter creates another 676,000 rego codes)
    # "ABCDEFGHIJKLMNOPQRSTUVWXYZ" = 17,576,000 rego codes ( 000AAA to 999ZZZ)


    p1 = i
    for j in alphabet:
        p2 = j
        for k in alphabet:
            p3 = " " + p1 + p2 + k
            for l in numList:
                rego = l + p3
                regoList.append(rego)


print('numList: ', numList[0], numList[-1], len(numList))
print('regoList: ', regoList[0], regoList[-1], len(regoList))

