import requests, bs4, urllib, re, string

#####################################################
# Bs4 Web Scraping Demo Code
#####################################################

# Extracts html file from url and converts it into an article
def makeArticle(htmlFile):
    bigHeadersList = htmlFile.find_all('h1')
    bigHeadersText = [bigHeader.get_text() for bigHeader in bigHeadersList]
    smallHeadersList = htmlFile.find_all('h2')
    smallHeadersText = [smallHeader.get_text() for smallHeader in smallHeadersList]
    paragraphsList = htmlFile.find_all('p')
    paragraphsText = [paragraph.get_text() for paragraph in paragraphsList]
    divsList = htmlFile.find_all('div')
    divsText = []
    for div in divsList:
        if div.get('class') == ['zn-body__paragraph']:
            divsText.append(div.get_text())

    bigHeaders = ' '.join(bigHeadersText)
    smallHeaders = ' '.join(smallHeadersText)
    paragraphs = ' '.join(paragraphsText)
    specialText = ' '.join(divsText)

    article = bigHeaders + smallHeaders + paragraphs + specialText
    return article

# Extracts news article and gives back raw words of article in a variable
def extractAndStripArticle(url):
    request = requests.get(url)
    soup = bs4.BeautifulSoup(request.text, 'html.parser')

    article = makeArticle(soup)
    # punctuation removal strategy with re.sub method acquired from
    # https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-
    # from-a-string
    strippedArticle = re.sub(r'[^\w\s]','',article).lower() 

    return strippedArticle

def scrape112Website(url):
    website = requests.get(url)
    return website.text

if __name__ == "__main__":
    url = "https://www.cnn.com/2020/03/20/entertainment/jimmy-fallon-jennifer-garner-tonight-show-video-trnd/?hpt=ob_blogfooterold"
    url2 = "http://www.kosbie.net/cmu/spring-17/15-112/syllabus.html"
    print(extractAndStripArticle(url))
    #print(scrape112Website(url2))


