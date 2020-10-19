def Generator(n=100):
    import random
    output = "{} \n".format(n)
    for i in range(n-1):
        output += "{} \n".format(int(random.uniform(1,n*10)))
    output += "{}".format(int(random.uniform(1, n * 10)))
    return output