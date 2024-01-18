import argparse
from chrome_utils import open_chrome_with_designated_profile

parser = argparse.ArgumentParser()
parser.add_argument("-p", type=str)
parser.add_argument("-u", type=str)
args = parser.parse_args()

open_chrome_with_designated_profile(args.p, args.u)