import json

dic = dict()
with open('data/id_slug_page.json') as f:
    dic = json.load(f)
count = 0
test_dict = dict()
for key, value in dic.items():
    test_dict[key] = value
    count += 1
    if count == 50:
        break
with open('data/test_id_slug.json', 'w') as f:
    json.dump(test_dict, f)