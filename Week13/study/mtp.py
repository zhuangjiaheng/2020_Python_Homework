import concurrent.futures
import urllib.request

URLS = ['http://www.buaa.edu.cn/',
        'http://www.baidu.com/',
        'http://sem.buaa.edu.cn/',
        'http://www.apple.cn/',
        'http://www.163.com/',
        'http://www.qq.com',
        'http://www.360.com']

# Retrieve a single page and report the URL and contents
def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()

# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
    #print(future_to_url)
    for future in concurrent.futures.as_completed(future_to_url):
        #print(future)
        url = future_to_url[future]

        # try:
        #     data = future.result()
        # except Exception as exc:
        #     print('%r generated an exception: %s' % (url, exc))
        # else:
        #     print('%r page is %d KB' % (url, (len(data)//8)//1024))