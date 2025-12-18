# Creates a list of 'vehicle rego number' - Qld format. The use of 3 numerical digits 
# and 3 alphabetic char returns 17,576,000 variations. Script currently restricted to
# alphabetic char starting with A or B. This rstiction produces 1,352,000 rego numbers

numList = []
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
regoList = []

for i in range(0, 1000):
    j = str(i)
    if len(j) == 1:
        k = "00" + j
    elif len(j) == 2:
        k = "0" + j
    else: 
        k = j
    numList.append(k)

for i in "AB":  # Using only the first 2 letters here resticts the list to 1,352,000 rego numbers
    p1 = i
    for j in alphabet:
        p2 = j
        for k in alphabet:
            p3 = " " + p1 + p2 + k
            for l in numList:
                rego = l + p3
                regoList.append(rego)
