import datetime
import sys
import time

import yaml
import requests
import json


def main():
    # Parse input
    n = len(sys.argv)
    availability = {}
    requests_list = []
    if n != 2:
        print("Only input has to be a YAML config file")
        input("Enter to exit")
        return
    yaml_data = yaml.YAMLObject
    with open(sys.argv[1], "r") as stream:
        try:
            yaml_data = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print("Error loading YAML config file")
            input("Enter to exit")
            return
    data: dict
    for data in yaml_data:
        request = {
            "name": data.get("name"),
            "method": data.get("method", "GET"),
            "url": data.get("url"),
            "headers": data.get("headers"),
            "body": json.loads(data.get("body")) if data.get("body") else "",
            "domain": data.get("url").split("/")[2]
        }
        requests_list.append(request)
        availability[request["domain"]] = [0, 0]

    # Check endpoints
    while True:
        for request in requests_list:
            response = requests.Response
            timeout = 2
            if request["method"] == "GET":
                response = requests.get(request["url"], headers=request["headers"], timeout=timeout)
            elif request["method"] == "POST":
                response = requests.post(request["url"], data=request["body"], headers=request["headers"],
                                         timeout=timeout)

            if response.ok and response.elapsed < datetime.timedelta(milliseconds=500):
                availability[request["domain"]][0] += 1
                availability[request["domain"]][1] += 1
            else:
                availability[request["domain"]][0] += 1
        log(availability)
        time.sleep(15 - time.time() % 15)


def log(availability):
    for domain, stats in availability.items():
        print(f"{domain} has {100 * (stats[1] / stats[0]):.0f}% availability percentage")


if __name__ == '__main__':
    main()
