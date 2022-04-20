import sys
import json

def parse_order_details(raw_data):
    return json.load(raw_data)

if __name__ == "__main__":

    print("Reading order details...")

    order_details = parse_order_details(sys.argv[1])

    print(order_details)