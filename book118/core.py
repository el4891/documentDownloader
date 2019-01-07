import re
import json
import os
import shutil
from spider import getHTML, makeURL
from pdf import makePDF


class book118:
    def __init__(self, pid):
        self.pid = str(pid)
        self.pdfInfo = {}
        self.domain = ''
        self.index = -1
        self.total = 0
        self.imgList = []
        self.imgFileList = []

    def getPDF(self):
        # 获取需要的信息
        self.__getPdfInfo()
        print(self.pdfInfo)
        #　获得所有图片的地址
        while self.index != self.total:
            if len(self.imgList) == 0 and ('Img' not in self.pdfInfo.keys()):
                index = 0 if self.index < 0 else self.index
                url = self.__getNextPageUrl2(index)

            else:
                url = self.__getNextPageUrl(
                    self.imgList[-1]
                    if len(self.imgList) != 0 else self.pdfInfo['Img']
                )

            self.__getNextPage(url)
        # 下载图片
        self.__getIMG()
        # 生成pdf
        makePDF(self.imgFileList, 'book118.pdf')

    def __getPdfInfo(self):
        url = makeURL('https://max.book118.com/index.php?',
                      {
                          'g': 'Home',
                          'm': 'View',
                          'a': 'viewUrl',
                          'cid': str(self.pid),
                          'flag': '1'
                      })
        viewPage = getHTML(url)
        self.domain = re.findall(r'//(.*?)\..*', viewPage)[0]
        rawHTML = getHTML('https:' + viewPage)
        res = re.findall(
            r'<input type="hidden" id="(.*?)" value="(.*?)".*?/>', rawHTML)
        for lst in res:
            self.pdfInfo[lst[0]] = lst[1]

    def __getNextPageUrl(self, imgUrl):
        url = makeURL('https://' + self.domain + '.book118.com/pdf/GetNextPage/?', {
            'f': self.pdfInfo['Url'],
            'img': imgUrl,
            'isMobile': 'false',
            'isNet': 'True',
            'readLimit': self.pdfInfo['ReadLimit'],
            'furl': self.pdfInfo['Furl']
        })
        return url

    def __getNextPageUrl2(self, sn):
        #https://view81.book118.com/PW/GetPage?f=dXAxNC0yLmJvb2sxMTguY29tLjgwXDQyOTc2OTUtNWI3YWEzNjBkOWM1Yi5wZGY=&img=&isMobile=false&readLimit=bJM31kWS6BrgH4xjKQL_0w==&sn=0&furl=o4j9ZG7fK95dS7wYrAN0MnYqzG1T0OIsJHGIUe54h13R6@kUibFpZKrUNkicV2NR2IH2y_3vZEuikVjZUp3Iz3Ry@u8Hmx60CGT0PLL@bUDLLuOuNvZ7Rw==
        #https://view81.book118.com/PW/GetPage?f=dXAxNC0yLmJvb2sxMTguY29tLjgwXDQyOTc2OTUtNWI3YWEzNjBkOWM1Yi5wZGY=&img=7o@o7xcocmktXwDypvIH900SNkQEw@wGz0AI70EEqtK00nqcPXaQeneYOQjm2CKp58hjmw1sezY=&isMobile=false&readLimit=bJM31kWS6BrgH4xjKQL_0w==&sn=1&furl=o4j9ZG7fK95dS7wYrAN0MnYqzG1T0OIsJHGIUe54h13R6@kUibFpZKrUNkicV2NR2IH2y_3vZEuikVjZUp3Iz3Ry@u8Hmx60CGT0PLL@bUDLLuOuNvZ7Rw==
        url = makeURL('https://' + self.domain + '.book118.com/PW/GetPage?', {
            'f': self.pdfInfo['Url'],
            'isMobile': 'false',
            'isNet': 'True',
            'sn' : str(sn),
            'readLimit': self.pdfInfo['ReadLimit'],
            'furl': self.pdfInfo['Furl']
        })
        return url


    def __getNextPage(self, url):
        print('url  ' + url)
        try:
            result = getHTML(url)
        except:
            result = getHTML(url)
        
        res = json.loads(result)

        if self.total == 0:
            self.total = res['PageCount']
        self.index = res['PageIndex']
        self.imgList.append(res['NextPage'])

        print(self.index, '/', self.total, 'url finish', res['NextPage'])

        return res

    def __getIMG(self):
        if os.path.exists('./temp'):
            shutil.rmtree('./temp')
        os.makedirs('./temp')

        for (idx, img) in enumerate(self.imgList):
            url = makeURL('http://' + self.domain + '.book118.com/img/?', {'img': img})
            try:
                res = getHTML(url, byte=True)
            except:
                res = getHTML(url, byte=True)
            with open('./temp/' + str(idx + 1) + '.jpg', 'wb') as f:
                f.write(res)
            print(idx + 1, '/', self.total,
                  'download finish', str(idx + 1) + '.jpg')
            self.imgFileList.append('./temp/' + str(idx + 1) + '.jpg')
        # ?img=Hs92T42xAvsP_ycWPqjcj8Iw69WUDaxvq4HtxAb3Zl3WYzxX1hdIsZzydhmmGAtm
        pass


if __name__ == '__main__':
    #pdf = book118(115219794)
    pdf = book118(137343582)
    pdf.getPDF()
