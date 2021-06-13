import argparse, sys
from create_json import generate_json
from update_json import update_json

def main(argv):
    parser=argparse.ArgumentParser()
    parser.add_argument('--operation', '-o', help='Operation type: CREATE or UPDATE')
    parser.add_argument('--id', '-i', help='Steam user id')
    parser.add_argument('--filename', '-f', help='Name of the json file.')

    args = parser.parse_args()
    if(args.operation == None or args.operation.upper() not in ("CREATE, UPDATE")):
        raise Exception("--operation argument CREATE or UPDATE must be provided.")

    if(args.filename == None):
        raise Exception("--filename argument must be provided.")

    if(args.operation.upper() == "CREATE"):
        if(args.id == None):
            raise Exception("--id argument must be provided in CREATE operation")
        else:
            generate_json(args.id, args.filename)

    if(args.operation.upper() == "UPDATE"):
        update_json(args.filename)

if __name__ == "__main__":
    main(sys.argv[1:])