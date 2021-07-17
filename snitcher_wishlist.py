import argparse, sys
import time
from snitcher import Snitcher

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', '-i', help='Steam user id', required=True)
    parser.add_argument('--filename', '-f', help='Name of the json file.', required=True)
    parser.add_argument('--threads', '-t', help='Number or threads to use, default 10.', default=10)
    parser.add_argument('--repository', '-r', help='File with game urls.', default='repository.csv')

    args = parser.parse_args()
    snitcher = Snitcher(args.id, args.filename, int(args.threads), args.repository)
    snitcher.generate_json()

if __name__ == "__main__":
    start_time = time.time()
    main(sys.argv[1:])
    print("\n--- %s seconds ---" % (time.time() - start_time))