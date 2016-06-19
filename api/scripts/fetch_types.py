import json
import yaml
import sys


def main():
    raw = open(sys.argv[1]).read()
    data = json.loads(raw)

    pk = 1
    parsed = []
    for row in data:
        name = row['compNameForWeb'].encode("utf-8")
        parsed.append({
            "model": "api.product",
            "pk": pk,
            "fields": {
                "category": row['categoryName'].encode("utf-8"),
                "name": row['compNameForWeb'].encode("utf-8"),
                "apple_id": row['componentID'],
                "identifier": name.lower().replace(" ", ""),
            }
        })
        pk += 1

    content = yaml.dump(parsed, default_flow_style=False)
    open("../fixtures/products.yaml", "w").write(content)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s <products JSON file>" % sys.argv[0]
        sys.exit(1)

    main()
