q = open('resources/winequality.txt')

index = []

for line in q:
    if line[len(line) - 2:len(line) - 1] == '7':
        index.append(line)

print(index)
