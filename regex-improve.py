import lib
from lib import extra_char_class, general
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d",
                        help="target directory")
    parser.add_argument("-n",
                        help="name of regex offense")
    args = parser.parse_args()

    if args.n == 'extra_char_class':
        operator_instance = lib.extra_char_class.FileOperatorExtraCharClass()

    # adjust the source code using
    # general loop + operator_instance
    # from above
    lib.general.walk_replace(rootdir=args.d,
                             operator_instance=operator_instance)
