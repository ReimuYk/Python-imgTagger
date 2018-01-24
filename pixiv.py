import requests,re
s = requests.Session()

def getTags(PID):
    url = r'https://www.pixiv.net/member_illust.php?mode=medium&illust_id='+PID
    html = s.get(url).text
    rTag = r'tags.+ul'
    tagContainer = re.findall(rTag, html)[0]
    r2 = r'text">(.+?)</a'
    tags = re.findall(r2, tagContainer)
    return tags

def pixivLogin():
    # init parameter
    baseUrl = "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index"  
    LoginUrl = "https://accounts.pixiv.net/api/login?lang=zh"  
    firstPageUrl = 'http://www.pixiv.net/member_illust.php?id=7210261&type=all'  
    loginHeader = {    
    'Host': "accounts.pixiv.net",    
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",    
    'Referer': "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index",  
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",  
    'Connection': "keep-alive"  
    }    
    return_to = "http://www.pixiv.net/"    
    pixiv_id = '513639514@qq.com'
    password = 'chinuomi'  
    postKey = []
    # get postKey
    loginHtml = s.get(baseUrl)  
    pattern = re.compile('<input type="hidden".*?value="(.*?)">', re.S)  
    result = re.search(pattern, loginHtml.text)  
    postKey = result.group(1)
    # login
    loginData = {"pixiv_id": pixiv_id, "password": password, 'post_key': postKey, 'return_to': return_to}   
    s.post(LoginUrl, data = loginData, headers = loginHeader)

pixivLogin()
