
def getParams(rawResponse):
    lineArray = rawResponse.split("\n")
    createMarkArray = ["creation date:", "domain registration date:",
                       "created on:", "creatin date:", "creatn date:", "created:",
                       "registered:"]
    noinfoMarkArray = ["no entries found", "no info", "blacklist", "no whois", "invalid query", "incorrect domain name"]
    infoMarkArray = ["registrant"]
    whoisServerMark = "Connecting to "

    whoisServerName = ''
    creationDateLine = ''
    okinfo = ''

    if len(lineArray) < 20:
        okinfo = '0'
    for line in lineArray:
        if line.startswith(whoisServerMark):
            whoisServerName = line[len(whoisServerMark): line.find("...")]
        for mark in createMarkArray:
            if line.lower().find(mark) != -1:
                creationDateLine = line[len(mark): -1]
        for mark in noinfoMarkArray:
            if line.lower().find(mark) != -1:
                okinfo = '0'
        for mark in infoMarkArray:
            if line.lower().find(mark) != -1:
                okinfo = '1'
    regDateStr = parseDateTime(creationDateLine)
    return whoisServerName, regDateStr, okinfo, getWorkTimeInMonth(regDateStr)

def getWorkTimeInMonth(regDateStr):
    if regDateStr == '' or regDateStr == '?':
        return ''
    import datetime
    now = datetime.datetime.now()
    nowMonthCount = (now.year - 1990) * 12 + (now.month - 1)
    regYear = int(regDateStr[:4])
    regMonth = int(regDateStr[5:7])
    regMonthCount = (regYear - 1990) * 12 + (regMonth - 1)
    return str(nowMonthCount - regMonthCount)

def getMonth(str):
    import re
    str = str.lower()
    if len(re.findall("jan", str)) > 0:
        return '01'
    if len(re.findall("feb", str)) > 0:
        return '02'
    if len(re.findall("mar", str)) > 0:
        return '03'
    if len(re.findall("apr", str)) > 0:
        return '04'
    if len(re.findall("may", str)) > 0:
        return '05'
    if len(re.findall("jun", str)) > 0:
        return '06'
    if len(re.findall("jul", str)) > 0:
        return '07'
    if len(re.findall("aug", str)) > 0:
        return '08'
    if len(re.findall("sep", str)) > 0:
        return '09'
    if len(re.findall("oct", str)) > 0:
        return '10'
    if len(re.findall("nov", str)) > 0:
        return '11'
    if len(re.findall("dec", str)) > 0:
        return '12'
    return '?'


def parseDateTime(dateTime):
    import re
    if dateTime == '?':
        return dateTime
    if re.search("[\d]{4}-[\d]{2}-[\d]{2}", dateTime):
        dateTime = re.findall("[\d]{4}-[\d]{2}-[\d]{2}", dateTime)[0]
        dateTime = dateTime[:4] + "/" + dateTime[5:7] + "/" + dateTime[8:10]
        return dateTime
    if re.search("UTC", dateTime):
        # ' 25 Aug 2003 03:21:59:000   UTC'
        arr = re.findall("[^ ]+", dateTime)
        year = arr[2]
        date = arr[0]
        month = getMonth(dateTime)
        dateTime = year + "/" + month + "/" + date
        return dateTime
    if re.search("[\d]{4}\.[\d]{2}\.[\d]{2}", dateTime):
        dateTime = re.findall("[\d]{4}\.[\d]{2}\.[\d]{2}", dateTime)[0]
        dateTime = dateTime[:4] + "/" + dateTime[5:7] + "/" + dateTime[8:10]
        return dateTime
    if re.search("GMT", dateTime):
        # ' Wed Feb 05 20:54:08 GMT 2003'
        arr = re.findall("[^ ]+", dateTime)
        year = arr[5]
        date = arr[2]
        month = getMonth(dateTime)
        dateTime = year + "/" + month + "/" + date
        return dateTime
    if re.search("[\d]{4}/[\d]{2}/[\d]{2}", dateTime):
        dateTime = re.findall("[\d]{4}/[\d]{2}/[\d]{2}", dateTime)[0]
        return dateTime
    if re.search("[\d]{6}", dateTime):
        dateTime = re.findall("[\d]+", dateTime)[0]
        dateTime = dateTime[:4] + "/" + dateTime[4:6] + "/" + dateTime[6:8]
        return dateTime
    if re.search("[\d]{2}-[\w]{3}-[\d]{4}", dateTime.lower()):
        # '03-Oct-1999'
        dateTime = re.findall("[\d]{2}-[\w]{3}-[\d]{4}", dateTime)[0]
        arr = dateTime.split("-")
        year = arr[2]
        date = arr[0]
        month = getMonth(dateTime)
        dateTime = year + "/" + month + "/" + date
        return dateTime
    if re.search("[\d]{2}/[\d]{2}/[\d]{4}", dateTime):
        # 'egistered: 12/02/2015'
        dateTime = re.findall("[\d]{2}/[\d]{2}/[\d]{4}", dateTime)[0]
        arr = dateTime.split("/")
        dateTime = arr[2] + "/" + arr[1] + "/" + arr[0]
        return dateTime
    if re.search("[\d]{2}\.[\d]{2}\.[\d]{4}", dateTime):
        # '      07.08.2015 12:21:09''
        dateTime = re.findall("[\d]{2}\.[\d]{2}\.[\d]{4}", dateTime)[0]
        arr = dateTime.split(".")
        dateTime = arr[2] + "/" + arr[1] + "/" + arr[0]
        return dateTime
    return dateTime

