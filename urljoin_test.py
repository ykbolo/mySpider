from urllib.parse import urljoin

print(urljoin("http://www.asite.com/folder/currentpage.html?id=1",
              "?id=2"))
