import os
from pitd import PITD

if __name__ == "__main__":
    PITD(os.getcwd(), (800, 600)).run()
