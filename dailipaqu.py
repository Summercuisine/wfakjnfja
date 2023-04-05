import requests
from bs4 import BeautifulSoup
import threading
import json
def pushMessage(zhu,NEIR):

    url = 'http://www.pushplus.plus/send?token=a30fcda032c2411aa530f86ca8368af6&title='+zhu+'&content=代理'+NEIR+'代理&template=html'
    print("推送内容", url)
    resp = requests.post(url)
    if resp.json()["code"] == 200:
        print('推送消息提醒成功！')
    else:
        print('推送消息提醒失败！')

# 构造请求 URL 和 Headers
url_template = 'https://www.kuaidaili.com/free/intr/{}/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

# 构造代理服务器认证信息
proxy_user = 'your_proxy_username'
proxy_pass = 'your_proxy_password'
proxy_auth = requests.auth.HTTPProxyAuth(proxy_user, proxy_pass)

# 存储可用的代理服务器列表
proxy_list = []

def test_proxy(proxy_url):
    """
    验证代理服务器是否可用
    """
    # 设置请求 URL 和 Headers
    target_url = 'https://www.baidu.com'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

    # 构造 POST 请求
    post_data = {'key': 'value'}

    # 使用代理服务器发送请求，并检查响应结果是否成功
    try:
        response = requests.post(target_url, headers=headers, proxies={'https': proxy_url}, auth=proxy_auth, data=post_data, timeout=10, verify=False)
        if response.status_code == 200:
            print('代理服务器可用：', proxy_url)
            lock.acquire()
            proxy_list.append(proxy_url)
            lock.release()
        else:
            print('代理服务器不可用：', proxy_url)
    except Exception as e:
        print('验证代理服务器 ({0}) 可用性时出错：{1}'.format(proxy_url, str(e)))

def crawl_proxy(page_num):
    """
    爬取指定页数的 IP 和端口号列表，并验证代理服务器可用性
    """
    url = url_template.format(page_num)

    # 发送 GET 请求并获取 HTML 响应内容
    response = requests.get(url, headers=headers)
    html_content = response.text

    # 使用 BeautifulSoup 解析 HTML 内容
    soup = BeautifulSoup(html_content, 'html.parser')

    # 解析 HTML 表格中的 IP 和端口号信息
    ip_list = []
    port_list = []
    for tr in soup.select('#list table tbody tr'):
        # 检查是否存在 IP 和端口号列
        if len(tr.select('td')) < 2:
            continue

        # 获取 IP 和端口号值，并添加到列表中
        ip = tr.select('td')[0].string.strip()
        port = tr.select('td')[1].string.strip()
        ip_list.append(ip)
        port_list.append(port)

    # 并发验证代理服务器是否可用
    threads = []
    for i in range(len(ip_list)):
        proxy_host = ip_list[i]
        proxy_port = port_list[i]

        # 构造代理服务器的 URL
        proxy_url = 'http://{0}:{1}'.format(proxy_host, proxy_port)

        # 创建线程并启动
        t = threading.Thread(target=test_proxy, args=(proxy_url,))
        threads.append(t)
        t.start()

    # 等待所有线程运行结束
    for t in threads:
        t.join()

# 添加锁，防止多个线程同时修改 proxy_list
lock = threading.Lock()

# 爬取前 10 页 IP 代理服务器列表，并验证其可用性
for i in range(1, 6):
    print('正在爬取第 {} 页...'.format(i))
    crawl_proxy(i)

# 将可用的代理服务器列表以 json 格式保存到文件中
with open('proxy_list.json', 'w') as f:
    json.dump(proxy_list, f)

print('所有代理服务器验证完毕，可用的代理服务器数量为：', len(proxy_list))
pushMessage('代理获取成功', '所有代理服务器验证完毕，可用的代理服务器数量为：'+str(len(proxy_list)))
