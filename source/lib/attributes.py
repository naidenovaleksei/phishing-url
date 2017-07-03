# -*- coding: UTF-8 -*-

def getWhois(url):
    import whoisparser as wp
    rawResponse = getWhoisRawData(url)
    params = wp.getParams(rawResponse)
    return params


def getPageRank(url):
    cmd = "perl page_rank.pl " + url    
    return startExternProgram(cmd)[:-1]

# second one
# url = 'http://pr-cy.ru/a/' + 'www.' + url
# import requests
# r = requests.get(url)
# content = r.content.decode()
# pos = content.find('PageRank: ') + len('PageRank: ')
# pr_line = content[pos:pos + 1] if pos >= 0 else -1
# return pr_line

def getPageRankExt(url):
    pr = getPageRank(url)
    exist = '0' if (pr in ['-1', '']) else '1'
    return pr, exist


def getDotsCount(url):
    import re
    url = getDomainName(url)
    arr = re.findall("\.", url)
    return str(len(arr) + 1)


def getUseHttps(url):
    if url == '':
        return 'False'
    if url.startswith("https://"):
        return 'True'
    if url.startswith("http://"):
        return 'False'
    if url.startswith("www."):
        url = url[len("www."):]
    url = 'www.' + getDomainName(url)
    import http.client
    import socket, ssl
    try:
        #conn = http.client.HTTPSConnection(url, timeout = 10)
        #conn.request("HEAD", "/")
        #res = conn.getresponse()
        import socket, ssl

        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = True
        context.load_default_certs()

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = context.wrap_socket(s, server_hostname=url)
        ssl_sock.settimeout(5)
        ssl_sock.connect((url, 443))
        ssl_sock.settimeout(None)
        return 'True'
    except Exception:
        return 'False'


def getWhoisRawData(url):
    url = url[len("http://"):] if url.startswith("http://") else url[len("https://"):]
    cmd = "whois.exe " + url
    return startExternProgram(cmd, islog=True)


def getDomainName(url):
    if type(url) != str:
		return url
    if url.startswith("http://"):
        url = url[len("http://"):]
    elif url.startswith("https://"):
        url = url[len("https://"):]

    if url.startswith("www."):
        url = url[len("www."):]
    pos = url.find("/")
    if pos >= 0:
        url = url[:pos]
    return url


def getDomain(url):
    return url
    pos = url.find('/', 9)
    url = url[:pos]
    if url.startswith('http'):
        return url
    elif url.startswith('www'):
        return 'http://' + url
    else:
        return 'http://www.' + url


def startExternProgram(cmd, islog=False, decoding="utf-8"):
    import subprocess
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.universal_newlines = True
    try:
        stdoutdata, stderrdata = p.communicate(timeout=10)
        errorCode = p.returncode
    except subprocess.SubprocessError:
        p.kill()
        return 'subprocess.SubprocessError\n'
    if islog:
        with open("whois_whitelist_3K_5K.log", "ab") as f:
            f.write(("FFFFFFF: " + cmd + "\n").encode())
            f.write(stdoutdata)

    return stdoutdata.decode("utf-8", "ignore")

def getParams(argv):
    fname = argv[1] if len(argv) > 1 else "input.txt"
    begin = int(argv[2]) if len(argv) > 2 else 0
    end = int(argv[3]) if len(argv) > 3 else 0xFFFFFFFF
    safe = '1' if (len(argv) > 4) and (argv[4].lower() == "safe") else '0'
    return fname, begin, end, safe


def removeEnter(line):
    if (line[-1] == '\n') or (line[-1] == '\t'):
        line = line[: -1]
    return line


def getUrlType(url):
    import re
    domainName = getDomainName(url)
    if re.match(".*[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}.*", domainName):
        return "1"
    elif re.match(".*Ox[\d]{1,3}\.Ox[\d]{1,3}\.Ox[\d]{1,3}\.Ox[\d]{1,3}.*", domainName):
        return "1"
    companyNamesArray = ["paypal","facebook","aol","google", "apple","ebay","yahoo","microsoft",
						 "dropbox","hotmail","blizzard","mastercard","amazon","visa","steam","walmart"]
    for name in companyNamesArray:
        if getIsIncludeWord(url, name) == "True":
            if getIsIncludeWord(domainName, name) == "True":
                if domainName[-len(name+".com"):] == name+".com":
                    return "4"
                else:
                    return "3"
            else:
                return "2"

    return "4"


def getIsIncludeWord(str, word):
    if str.lower().find(word) > -1:
        return "True"
    else:
        return "False"


def getElapsedMonths(regDateStr):
    #14.04.2013
    #2013.04
    # regYear = int(regDateStr[:4])
    #regMonth = int(regDateStr[5:7])
    if regDateStr == '':
        return '?'
    import datetime
    now = datetime.datetime.now()
    nowMonthCount = (now.year - 1990) * 12 + (now.month - 1)
    regYear = int(regDateStr[6:10])
    regMonth = int(regDateStr[3:5])
    regMonthCount = (regYear - 1990) * 12 + (regMonth - 1)
    return str(nowMonthCount - regMonthCount)


def mygetattr(line):
    #URL+	DOMAIN NAME	Registration date	info	Page Rank+	ID+	Безопасный
    #http://www.sakengua.com.ar/ClaraChambliss/dropbox/proposal/	AR.whois-servers.net	14.04.2013	False	0	2	False
    array = line.split("\t")
    url = array[0]
    regDate = array[2]
    safe = removeEnter(array[6])

    urlType = getUrlType(url)
    includeLogin = getIsIncludeWord(url, "login")
    includeSecure = getIsIncludeWord(url, "secure")
    includeUpdate = getIsIncludeWord(url, "update")
    includeAccount = getIsIncludeWord(url, "account")
    useHttps = getUseHttps(url)
    dotsCount = getDotsCount(url)
    workMonths = getElapsedMonths(regDate)
    pageRank = array[4]
    pageRankExist = "False" if pageRank == "" else "True"
    if pageRank == "":
        pageRank = "?"

    return url+'\t'+urlType+'\t'+includeLogin+'\t'+\
           includeSecure+'\t'+includeUpdate+'\t'+\
           includeAccount+'\t'+useHttps+'\t'+dotsCount+'\t'+\
           workMonths+'\t'+pageRank+'\t'+pageRankExist+'\t'+safe


if __name__ == '__main__':
    # import sys
    # fname, begin, end, _ = getParams(sys.argv)
    # # 3001	http://p3plcpnl0922.prod.phx3.secureserver.net/~cpshutter/wp-content/languages/image/update/	-1
    # import whoisparser
    # print('\t'.join(["ID", "URL", "workMonths" "safe"]))
    # with open(fname) as f:
    #     for line in f:
    #         inarray = line.split(';')
    #         attr = [0]*4
    #         attr[0] = inarray[0]
    #         attr[1] = inarray[1]
    #         attr[2] = whoisparser.getWorkTimeInMonth(inarray[3])
    #         attr[3] = "False"
    #         print('\t'.join(attr))


    import sys
    fname, begin, end, _ = getParams(sys.argv)
    # 3001	21cineplex.com	5
    import whoisparser
    print('\t'.join(["ID", "URL", "template", "includeLogin","includeSecure","includeUpdate",\
           "includeAccount","useHttps","dotsCount",\
            "pageRank","pageRankExist", "safe"]))
    with open(fname) as f:
        for line in f:
            inarray = line.split('\t')
            attr = [0]*12
            attr[0] = inarray[0]
            attr[1] = inarray[1]
            url = attr[1]
            attr[2] = getUrlType(url)
            attr[3] = getIsIncludeWord(url, "login")
            attr[4] = getIsIncludeWord(url, "secure")
            attr[5] = getIsIncludeWord(url, "update")
            attr[6] = getIsIncludeWord(url, "account")
            attr[7] = getUseHttps(url)
            attr[8] = getDotsCount(url)
            attr[9] = removeEnter(inarray[2])
            attr[10] = "True"
            if  attr[9] == '-1':
                attr[9] = ''
                attr[10] = 'False'
            attr[11] = 'True'
            print('\t'.join(attr))



# import sys
# fname, begin, end, _ = getParams(sys.argv)
#
# print('\t'.join(["ID", "URL", "template", "includeLogin","includeSecure","includeUpdate",\
#        "includeAccount","useHttps","dotsCount",\
#        "workMonths","pageRank","pageRankExist", "safe"]))
# counter = -1
# with open(fname) as f:
#     for line in f:
#         counter = counter + 1
#         if (counter >= begin) and (counter < end):
#             print('\t'.join([str(counter), mygetattr(line)]))
