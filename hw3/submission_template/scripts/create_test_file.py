with open("../data/test.csv", "w") as f:
    for i in range(10000):
        if i%2==0:
            f.write("fake\n")
        else:
            f.write("potus\n")