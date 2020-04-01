from urllib.request import urlparse
url = "http://eng.suda.edu.cn/suda_news/sdyw/202002/0c620fb0-aad7-4168-a3a4-a7c07442df98.html?id=002#545"
# 域名
domain = urlparse(url).scheme+'://'+urlparse(url).netloc+urlparse(url).path
# 协议

print(domain)
