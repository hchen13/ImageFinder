import argparse

from core import *


FLAGS = None


def main():
    go(FLAGS.keyword, FLAGS.dir, FLAGS.limit)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dir',
        type=str,
        default='./',
        help='Root directory where a folder named after the keyword will be created, which will contain all the downloaded images'
    )
    parser.add_argument(
        '--keyword',
        type=str,
        default='',
        help="The keyword for searching the web"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=1,
        help='The maximum number of images to be downloaded'
    )
    FLAGS, unparsed = parser.parse_known_args()
    main()
    browser.close()