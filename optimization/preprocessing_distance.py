import pickle

f = open("../data/distance.csv", mode='r')
csv = f.readlines()
data = csv[1:]
distance = []
for row in data:
    d = row[:-1].split(',')[1:]
    try:
        d = list(map(float, d))
        distance.append(d)
    except:
        print(d)
print(distance)
f.close()

f = open("../data/distance", mode="wb")
pickle.dump(distance, f)
f.close()
