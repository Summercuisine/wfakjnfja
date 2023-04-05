import requests
import json
import re

# 定义一个匹配中文字符的正则表达式


# 读取代理列表
with open('proxy_list.json', 'r') as f:
    proxies = json.load(f)

# 目标网址
url = "https://bbs.125.la/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1"

# 携带的参数
params = {
    "formhash": "3c7af791",
    "submit": "1",
    "targerurl": "/thread-14765645-1-1.html",
    "todaysay": "精易模块V11.0.5 发布【2023.03.01】",
    "qdxq": "nu"
}

# 携带的 Cookies
cookies = {
    "lDlk_ecc9_saltkey": "CoUsEYs1",
    "lDlk_ecc9_lastvisit": "1679640141",
    "lDlk_ecc9_client_created": "1679644247",
    "lDlk_ecc9_client_token": "8F3AAF37546B0B81EB3A155EA208ED56",
    "lDlk_ecc9_auth": "c402J8xyms68ukj9EB84DvYQaJG8zxcjmV50NQAB9gJPq5k4qPSogHa%2Fn5vC2KPl4CWI%2BF8%2BbZlE8jOrHw89djh4PDs",
    "lDlk_ecc9_connect_login": "1",
    "lDlk_ecc9_connect_is_bind": "1",
    "lDlk_ecc9_connect_uin": "8F3AAF37546B0B81EB3A155EA208ED56",
    "lDlk_ecc9_nofavfid": "1",
    "lDlk_ecc9_smile": "4D1",
    "Hm_lvt_c6927066ad2f2806b262f20b26fabff4": "1680438705,1680492432,1680534807,1680599877",
    "Hm_lpvt_c6927066ad2f2806b262f20b26fabff4": "1680599877",
    "lDlk_ecc9_sid": "b706Xs",
    "lDlk_ecc9_lip": "39.130.112.86%2C1680599879",
    "lDlk_ecc9_ulastactivity": "1c02uipdgwYI8eKF%2FVdc543o83soT3Gk1%2B0sG0CPpcEULPmYsTpj",
    "Hm_lvt_fa32dadde3745af309b587b38d20ea1d": "1680438708,1680492434,1680534808,1680599880",
    "lDlk_ecc9_sendmail": "1",
    "lDlk_ecc9_st_p": "657500%7C1680599930%7Cbf6be41c4613e3992a8f29a75e5c278c",
    "lDlk_ecc9_visitedfid": "27D98D125D81D100D226D168D204D99D147",
    "lDlk_ecc9_viewid": "tid_14769585",
    "lDlk_ecc9_lastact": "1680599931%09home.php%09spacecp",
    "lDlk_ecc9_lastcheckfeed": "657500%7C1680599931",
    "Hm_lpvt_fa32dadde3745af309b587b38d20ea1d": "1680599932"
}

# 发送 POST 请求，完成签到

# 判断是否签到成功
def pushMessage(NEIR):

    url = 'http://www.pushplus.plus/send?token=a30fcda032c2411aa530f86ca8368af6&title=精易签到&content='+NEIR+'&template=html'
    print("推送内容", url)
    resp = requests.post(url)
    if resp.json()["code"] == 200:
        print('推送消息提醒成功！')
    else:
        print('推送消息提醒失败！')

timeout = 10
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

for proxy_url in proxies:
    # 使用当前代理发送请求
    try:
        response = requests.post(url, params=params, headers=headers, cookies=cookies,timeout=timeout, proxies={'http':proxy_url, 'https':proxy_url})
        print('完成'+response.text)
        # 定义一个匹配中文字符的正则表达式
        zh_pattern = re.compile(r'[\u4e00-\u9fa5]+')
        # 提取中文字符
        match_results = zh_pattern.findall(response.text)
        # 将中文字符连在一起
        result = ''.join(match_results)
        # 将结果转换为字符串类型
        result_str = str(result)
        # 输出结果
        print(result_str)

        pushMessage(result_str)
        break
    except Exception as e:
        print(f"代理 {proxy_url} 出现异常：{e}")
        continue
else:
    print("所有代理均不可用，签到失败。")
