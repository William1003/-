import multiprocessing

from selenium import webdriver
import json
from selenium.webdriver.chrome.options import Options
import logging
import requests
from tqdm import tqdm

logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
fmt = logging.Formatter(fmt="%(asctime)s - %(levelname)-9s - %(filename)-8s : %(lineno)s line - %(message)s")
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(fmt)
logger.addHandler(sh)
logfile = 'log/get_download_url.log'
fh = logging.FileHandler(logfile, mode='a')
fh.setLevel(logging.DEBUG)
fh.setFormatter(fmt)
logger.addHandler(fh)


available_port = {'9527': True, '9528': True, '9529': True, '9530': True}

download_urls = dict()

headers = {'cookie': 'neon_lng=zh-Hans; adsk_ccpa_guid=1b1dead1-9e26-4967-bab6-5e9c87523310; AMCVS_6DC7655351E5696B0A490D44@AdobeOrg=1; OPTOUTMULTI_REF=6bc8aedb-3f88-4f75-a40d-9aad00914c24; OPTOUTMULTI_TYPE=P; s_ecid=MCMID|81385808566981209830170501947158096701; s_ppvl=oxygen%3Aauthentication%3Alogon%3Alogin%20failed,100,197,1007,1920,1007,1920,1080,1,P; s_ppv=oxygen%3Aauthentication%3Alogon%3Alogin%20failed,100,100,1007,1920,1007,1920,1080,1,P; s_vnum=1672912062301&vn=1; s_cc=true; _sp_id.cd78=b6616605-aaf8-446d-9a67-f2635ab4cdfe.1641376059.1.1641376064.1641376059.18dbf825-620a-4714-8025-c84e51c10d9f; cl-token=Skdo/BMVqlSxIxBqizA9BJoMHrilWCDrv6QgXqK4L3JCThUzOBF4lmDqM/ry5U/UV0p1zXaO3chCD6674guHXw==; cl-flags=cl-kmsi-enabled:1|cl-token-enabled:1; identity-sso=GP54JWJ8DHUU; s_dlv=1641376064502; AMCV_6DC7655351E5696B0A490D44@AdobeOrg=1585540135|MCIDTS|18998|MCMID|81385808566981209830170501947158096701|MCAAMLH-1641980864|11|MCAAMB-1641980864|RKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y|MCOPTOUT-1641383264s|NONE|MCAID|NONE|MCSYNCSOP|411-19005|MCCIDH|-1968766871|vVersion|4.4.0; _ga=GA1.3.1148096373.1641390455; _gid=GA1.3.404872968.1641390455; _ga=GA1.2.1148096373.1641390455; _gid=GA1.2.404872968.1641390455; gallery_sso_synergy=eff60bb0-5f19-4a2b-94f0-0144d1e1e10d; gallery_fe_session=bfcefe5b82aaf561dd020ecca0ae140a; AKN_UP_micro-prd=R1A1NEpXSjhESFVVOjFjZGVkYzA2N2Y5YmZiNDAwNzBjMjgzMzdiNzBkYzkx; AWSALB=5oowORoba+3ARFYU+j0ZMXWRKVYIDWt74PyHdMjyluKevdE/isWedZzaYeW9DSypmEdL8btcPbfg2HBnjLwVMQgGWEXUaEPXGXzrRSyXVyyqBjkwU8HrC2L6ut6e; AWSALBCORS=5oowORoba+3ARFYU+j0ZMXWRKVYIDWt74PyHdMjyluKevdE/isWedZzaYeW9DSypmEdL8btcPbfg2HBnjLwVMQgGWEXUaEPXGXzrRSyXVyyqBjkwU8HrC2L6ut6e; _exchange_gallery_session=WVpIQ3E3K1JCV0J2NThLTlFZdVE3L0RnTmhqYmhtMmpTSTJuR0JPYnlEVGcvOWMxaEZJSVhiNjVsZ1RadnczVmZ6Q3JYRFlybXlNdXhkOFZ5TlZFUmJoUGREWXpmNytwVEJjeGxlL0RrQlVkTFJFZkNoNyt1T3hPMnZQd1MrbHFwSnlGeEp6aG5Tczc5OURLbXRZSER2dFphWDVLYnNqQVFraDVNdXJBb3FLTG5uYTA0djlYWlhyaVZmUGNUSksxU0R3Y05oWXh5NkZZKzlLS1hETVQzdUo0ckxwMHZUZG9OTXdHOEdvZ0xaWExrdU8wZWFVWmM2Zi9kTGhxR0ZQcHNnUTZRUVBLczhSQnhqUHhVRUdUY3JrZFBtbTh4a3hvUlQwQ2t1SjA2RnBvaU1uZnM3VE4yQ2xHWERjZFV5RzJKTHQrM3NLVEluZDFnTWJlUWRmK0dtS3JtckpuQUl0WlZyR25qeGd0a1ZrdkZreEE1dnplbFk2cFloazJrakd6Qmo1V0dDdUx0Q2hIbEJJQjRpWjBKczc4ZVFsYTNBeTNYRDNQQ2t5My8zRGVDbURsUmt1RlZNZDFCQVZscjVtU1hiOXdvclJqM1NGQ09GV215RkR0aWVDOE9tSFFsaExKQjFuMjQ2WFBJZkpwc1BHMzVOYVhoY3duNWtLWWhxN1A0eUZtUFByWWNHeUVuQm1NcWdQaVBleUpHczl0UE5XMVN4YTlNc2JwamQ5Uy9HdDB0STYvYjBDM3JRM1d2Z1JzQTBCVERYSDdISU40K0xPaUVSdHVqRXNjemtEWEd0bGZWYlZUQ0kxQ3FXQXNEcnFiY1dCUmZvcEQ1Z3ZRUFhVUUgxWXNwSnpPU1dlUGJmT2o1dHZvalNoNTZIVUYzeUZSNGtBRktjQlpHaW80TjFhV200UlE0ZVdxbDRUbk9HbWVpUElGL2ZUSmQ0aUNkWC9xY054cDE3dUZldzRlN2xybm9jaDhLQVJxQjdVSDNkZGJXbW5zYzdNZE96aE9HTVphUnpqMll1UndETDh5TEZ3YnE3RG43L1UrNWF0b1ZZNkpJbCt2NjVEeHRBaTIyeXpWY0FNTEZZSG54dkZTRmE1WXc2aUlPSHdvNUFLcHZybWFkSEZEVUtlUS93aDg0eVdxNzhTQTAyTVlTM0dwWlBqQWRRTlIyVVU4bXgvang2aG4tLTN2QWlyMlFsQ3dHY2t4dEI1eklZOEE9PQ==--4881192e43e4fa107cdf3e64c08abefcb4bd82e7; _gat_UA-7938776-36=1; OPTOUTMULTI=0:0|c9:0|c1:0|c8:0|c7:0; ADSK_GDPR_OPT_LENGTH=Sat, 05 Feb 2022 02:49:05 GMT; utag_main=v_id:017e29a246c80002970df438038105073005006b00bd0$_sn:5$_ss:0$_st:1641439145499$vapi_domain:autodesk.com$optoutbackup:undefined;exp-1649152051497$ses_id:1641435130777;exp-session$_pn:24;exp-session; _gat=1',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}


def download(project_url, port):
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:" + port)
    browser = webdriver.Chrome(options=options)
    project_id = project_url.split('/')[4]
    url_list = []
    browser.get(project_url)
    li_list = browser.find_elements_by_class_name('file-item')
    if not li_list:
        logger.warning('Can not download Project {}'.format(project_id))
        available_port[port] = True
        exit(0)

    for li in li_list:
        assetId = li.get_attribute('data-id')
        assetProjectId = li.get_attribute('data-project_id')
        assetTitle = li.get_attribute('data-file-name')
        assetToken = li.get_attribute('data-token')
        assetUrl = li.get_attribute('data-asset-url')
        assetIsWipModel = li.get_attribute('data-is-wip-model')
        assetWipModelDownloadUrl = li.get_attribute('data-wip-model-download-url')
        if not assetId or not assetProjectId or not assetTitle or not assetToken or not assetUrl or not assetIsWipModel or not assetWipModelDownloadUrl:
            logger.warning('Can not download Project {}'.format(project_id))
            available_port[port] = True
            exit(0)
        download_url = 'https://gallery.autodesk.com/downloads/downModelFile?assetId={}&assetProjectId={}&assetTitle={}' \
                           '&assetToken={}&assetUrl={}&assetIsWipModel={}&assetWipModelDownloadUrl={}'.format(assetId, assetProjectId,
                                                                                                            assetTitle, assetToken, assetUrl, assetIsWipModel, assetWipModelDownloadUrl)
        if download_url:
            url_list.append(download_url)
            r = requests.get(download_url, headers=headers, stream=True)
            if r.status_code == 200:
                with open('models/' + assetTitle, 'wb') as f:
                    f.write(r.content)
                logger.info('Successfully download Project {}'.format(project_id))
            else:
                logger.warning('Can not download Project {}'.format(project_id))
    download_urls[project_id] = url_list

    with open('data/download_urls.json', 'a', encoding='utf-8') as f:
        json.dump(download_urls, f)
        f.close()
    available_port[port] = True


if __name__ == '__main__':
    with open('data/project_url.json', 'r', encoding='utf-8') as f:
        project_urls = json.load(f)
    pool = multiprocessing.Pool(processes=4)
    for project_url in tqdm(project_urls[44:]):
        port = ""
        for key, value in available_port.items():
            if value:
                port = key
                break
        pool.apply_async(download, args=(project_url, port, ))

