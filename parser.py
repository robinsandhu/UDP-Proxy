

def parse(address, data, origin):
    if origin == "client":
        print("[{}] {}".format(origin.center(8, " "), data[:50].hex()))
    elif origin == "server":
        print("[{}] {}".format(origin.center(8, " "), data[:50].hex()))