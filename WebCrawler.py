from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib import parse
import urllib
import re
from bs4 import BeautifulSoup

class LinkParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
       
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    newUrl = parse.urljoin(self.baseUrl, value)
                    self.links = self.links + [newUrl]

    def getLinks(self, url):
        self.links = []
        self.baseUrl = url
        response = urlopen(url)
        if response.getheader('Content-Type')=='text/html':
            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")
            self.feed(htmlString)
            return htmlString, self.links
        else:
            return "",[]

def spider(url, word, maxPages):      
    pagesToVisit = [url]
    numberVisited = 0
    foundWord = False
    while numberVisited < maxPages and pagesToVisit != [] and not foundWord:
        numberVisited = numberVisited +1
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]
        try:
            print(numberVisited, "Visiting:", url)
            parser = LinkParser()
            data, links = parser.getLinks(url)
            #print("****************************Printing URLs*******************************")
            i=0
            #while i<len(links):
            #    print(links[i])
            #    i+=1
            if data.find(word)>-1:
                foundWord = True
                pagesToVisit = pagesToVisit + links
                print(" **Success!**")
        except:
            print(" **Failed!**")
    if foundWord:
        print("The word", word, "was found at", url)
        soup=BeautifulSoup(data, 'lxml')
        vData=soup.text
        vData=re.sub('[ \t]+' , ' ', vData)
        vData=vData.split("\n")
        for i in range(len(vData)):
            if word in vData[i]:
                print(vData[i])
        


        
        
        #for i in range(len(result)):
         #   if word in result[i]:
          #     print(result[i])
            
    else:
        print("Word never found")
    return links   

def main():
    vLinks=[]
    vLinks=spider("http://thinkingmachines.in", "VIVO-Brazil", 1000)
    print("\n")
    print("\n")
    print("\n")
    print("\n")
    print("************************Printing URLs**************************")
    print(vLinks)
    print("\n")
    print("\n")
    print("\n")
    print("\n")
    for i in range(len(vLinks)):
        print(vLinks[i])
        spider(vLinks[i], "College", 1000)

main()