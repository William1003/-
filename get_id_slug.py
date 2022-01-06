from bs4 import BeautifulSoup
import requests
import json
import logging

# logger = logging.getLogger('logger')
# logger.setLevel(logging.DEBUG)
# sh = logging.StreamHandler()
# sh.setLevel(logging.DEBUG)
# fmt = logging.Formatter(fmt="%(asctime)s - %(levelname)-9s - %(filename)-8s : %(lineno)s line - %(message)s")
# sh.setFormatter(fmt)
# logger.addHandler(sh)

# url = "https://gallery.autodesk.com/projects/search?profileName=gallery&query=&filters[0][]=asset_types&filters[0][]=3D+Models&filters[0][]=三维模型&sort=popularity&page=0&page_size=20&facetQuery="
# r = requests.get(url)
# respond = json.loads(r.text)
# hit_ls = respond['hits']['hit']
# id_slug_dict = dict()
# for item in hit_ls:
#     id_slug_dict[item['id']] = item['fields']['slug']
# with open('data/id_slug_page.json', 'w') as f:
#     json.dump(id_slug_dict, f)

with open('data/temp.html', encoding='utf-8') as f:
    source_code = f.read()
    f.close()
soup = BeautifulSoup(source_code, 'html.parser')
a_list = soup.find_all('a', attrs={'class': 'project-viewer-link'})
url_list = []
for a in a_list:
    url_list.append('https://gallery.autodesk.com' + a.attrs['project-link'])
with open('data/project_url.json', 'w', encoding='utf-8') as f:
    json.dump(url_list, f)