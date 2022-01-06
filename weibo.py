import requests
import json
import csv

cookie = 'SINAGLOBAL=284897497755.91376.1627967437436; UOR=,,cn.bing.com; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Whw1g.O01Dy6077gxgRY7OO5JpX5KMhUgL.FoMNe0zcSh.c1K52dJLoIf2LxKML1hnLBo2LxK-L1K5L1heLxKqL12zL12eLxK.L1-BLBKzLxKqL1h.L1h2LxKnL1hzL1h.LxKML1-2L1hBLxKqLBo2LBKBLxK-L1-eL1hqt; ALF=1673009596; SSOLoginState=1641473597; SCF=Aq49zmrpUeEmto6i-aOvvoVFwXLfplallC16lCY94XAO00A3UhYjhOlyId9MKTL88TgqfSkacf6zg1PJKANK74c.; SUB=_2A25M0pZtDeRhGeFJ6FAX9CfKwjyIHXVvqYClrDV8PUNbmtB-LVLekW9NfDiLcghJtTS9vJUe-ao41Qpo_t4EatFY; XSRF-TOKEN=k6Z_jfSkhSBsUWrtbWdFDo5I; _s_tentry=weibo.com; Apache=8184822414519.981.1641473606040; ULV=1641473606046:3:2:2:8184822414519.981.1641473606040:1641346748217; WBPSESS=rYNQzU_IFPODcwQFuyDXxuiMj4p1Tv3-Ozf3eitmw5R33n-JKRo5BzWUdLXT1SZxZvet8a2vJfBk5Lih-kqNaQLCw4VBeq8NMbZ7D6yuSBkihFkjDlkIXOxNslZgpFK_XoEpurXddVKtN7V_MZf1cQ=='

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
    'cookie': cookie
}

longtext_url = "https://weibo.com/ajax/statuses/longtext?id="

title = ['text', 'date', 'reposts_count', 'comments_count', 'attitudes_count']
ls = []
for page in range(1, 11):
    url = 'https://weibo.com/ajax/profile/searchblog?uid=1974576991&page=' + str(page) + '&feature=0&q=中国制造'
    r = requests.get(url, headers=headers)
    data = json.loads(r.text)['data']['list']
    for item in data:
        text = item['text_raw']
        id = item['mblogid']
        date = item['created_at']
        reposts_count = item['reposts_count']
        comments_count = item['comments_count']
        attitude_count = item['attitudes_count']
        r = requests.get(longtext_url + id, headers=headers)
        longtext = json.loads(r.text)
        if longtext['data']:
            text = longtext['data']['longTextContent']
        text = ''.join(text.split()).strip()
        info = [text, date, reposts_count, comments_count, attitude_count]
        ls.append(info)
        print(info)
with open('data/weibo.csv', 'w', encoding='utf-8', newline='') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(title)
    csv_writer.writerows(ls)