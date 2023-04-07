import requests
from bs4 import BeautifulSoup
url = "https://www.eyuyan.la"
headers = {
    'authority': 'www.eyuyan.la',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'cookie': '54zb_2132_saltkey=i3c63gkc; 54zb_2132_lastvisit=1680878243; Hm_lvt_0b828ea81dacd6ebdc42a2a37fc91951=1680881844; 54zb_2132_sid=yh5xg8; 54zb_2132_lastact=1680882370%09index.php%09; Hm_lpvt_0b828ea81dacd6ebdc42a2a37fc91951=1680882370',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62'
}
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')
titles = []
dates = []
items = soup.select('div.right_list li')
for item in items:
    title = item.select_one('a')
    date = item.select_one('span.new')
    if title is not None:
        titles.append(title.text)
    if date is not None:
        dates.append(date.text)

if len(titles) != len(dates):
    print('Error: the number of titles and dates does not match.')
else:
    new_records = []
    for i in range(len(titles)):
        title = titles[i].strip()
        date = dates[i].strip()
        new_records.append(f'{date} - {title}')
    with open('record.txt', 'r+', encoding='utf-8') as f:
        old_records = f.read().split('\n')
        if new_records == old_records:
            print('No change found.')
        else:
            old_records_all = '\n'.join(old_records)
            f.seek(0)
            f.truncate()
            f.write('\n'.join(new_records))
            added_records = list(set(new_records) - set(old_records))
            removed_records = list(set(old_records) - set(new_records))
            for record in added_records:
                print(f'  + {record}')
            for record in removed_records:
                print(f'  - {record}')
            added_records_str = '\n'.join(added_records)
            removed_records_str = '\n'.join(removed_records)
            old_records_all_str = str(old_records_all)
            new_records_str = '\n'.join(new_records)
            content = f"变更记录：\n  新增：{added_records_str}\n  移除：{removed_records_str}\n旧的所有记录：\n{old_records_all_str}\n新的所有记录：\n{new_records_str}"
            token = 'a30fcda032c2411aa530f86ca8368af6'
            title = '精益源码内容有变化'
            url = 'https://www.pushplus.plus/send'
            params = {
                'token': token,
                'title': title,
                'content': content
            }
            response = requests.post(url, data=params)
            print(response.text)
