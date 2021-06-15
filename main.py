import argparse, sys
from create_json import generate_json
from update_json import update_json
from merge_json import merge_json
import time

def main(argv):
    parser=argparse.ArgumentParser()
    parser.add_argument('--operation', '-o', help='Operation type: CREATE, UPDATE or MERGE.')
    parser.add_argument('--id', '-i', help='Steam user id')
    parser.add_argument('--filename', '-f', help='Name of the json file.')
    parser.add_argument('--json1', '-j1', help='Name of the json to add new entries.')
    parser.add_argument('--json2', '-j2', help='Name of the json with the new entries.')
    parser.add_argument('--threads', '-t', help='Number or threads to use, default 10.')

    args = parser.parse_args()
    if(args.operation == None or args.operation.upper() not in ("CREATE", "UPDATE", "MERGE")):
        raise Exception("--operation argument CREATE, UPDATE or MERGE must be provided.")

    if(args.filename == None):
        raise Exception("--filename argument must be provided.")

    if(args.threads == None):
        args.threads = 10

    if(args.operation.upper() == "CREATE"):
        if(args.id == None):
            raise Exception("--id argument must be provided in CREATE operation.")
        else:
            generate_json(args.id, args.filename, args.threads)

    if(args.operation.upper() == "UPDATE"):
        update_json(args.filename, args.threads)

    if(args.operation.upper() == "MERGE"):
        if(args.json1 == None or args.json2 == None):
            raise Exception("--json1 and --json2 arguments must be provided in MERGE operation.")
        else:
            merge_json(args.json1, args.json2, args.filename)

if __name__ == "__main__":
    start_time = time.time()
    main(sys.argv[1:])
    print("\n--- %s seconds ---" % (time.time() - start_time))