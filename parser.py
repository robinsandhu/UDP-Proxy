

def parse(address, data):
    if address == "127.0.0.1":
        print("[{}] {}".format(address.center(15, " "), data[:50].hex()))
    