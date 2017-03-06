# Theodore Chu
# March 5, 2017
# For the USC Lab on Non-Democratic Politics under the direction of Erin Baggott Carter and Brett Logan Carter
# Scrapes Seychelles's The Nation
# Prints all sections
# Encodes in UTF-8

# Waits 5-10 minutes every 100 pages to avoid crashing the archive
# No articles are published on Sundays and on public holidays
# Entering dates requires search term, so scraping must be done by results #

import math  # this lets you do math
import io   # allows encoding in utf-8
import time  # this lets you slow down your scraper so you don't crash the website =/
import random  # this lets you draw random numbers.
import datetime  # this lets you create a list of dates
from selenium import webdriver  # the rest of these let you create your scraper

# prompt for start date
# prompt for end date
# name the file out
# load first date
# get the number of results
# go to the first page on the first date
# get all links from the first page on the first date
# go to each article from first page on first date. print to file
# repeat for all links on first date (while loop)
# repeat for all dates until the last date (while loop)

# url = http://www.nation.sc/news/archive.html?view=archive&start=0

startTime = time.time()

class SeychellesNation(object):
    def __init__(self):

        directory = input("Enter Directory: (ex: C:/Users/Theodore/Desktop/Programming/Scraping/SeychellesNation/). Press Enter for example:")
        if directory == "":
            directory = "C:/Users/Theodore/Desktop/Programming/Scraping/SeychellesNation/"

        self.__startResult = int(input("Enter Start Result. Choose a multiple of 20. Enter \"0\" if starting from beginning: "))
        self.__endResult = int(input("Enter End Result. Choose a multiple of 20: "))
        fileOutName = input("Enter file out name. Please omit \".txt\" (ex: syt0-1000.txt):")
        self.__fileOut = io.open(directory + fileOutName + ".txt", "a", encoding="utf-8")
        self.__pageCounter = 0
        self.__driver = webdriver.Firefox()

    def addResults(self):
        self.__startResult += 20
        return self.__startResult

    def getStartResults(self):
        return self.__startResult

    def getEndResults(self):
        return self.__endResult

    def loadResultsPage(self, resultsPageNum):
        if resultsPageNum > 1:
            print("Results " + str(self.__startResult - 20) + " to " + str(self.__startResult) + " done")
        resultsPage = "http://www.nation.sc/news/archive.html?view=archive&start=" + str(self.__startResult)
        print(resultsPage)
        print("Printing results " + str(self.__startResult) + " to " + str(self.__startResult + 20))
        time.sleep(random.uniform(3, 10))
        self.__driver.get(resultsPage)

    def getNumberOfResultsPages(self):
        resultsdiv = self.__driver.find_element_by_class_name('row.g-searchpage-form')
        resultsText = resultsdiv.find_element_by_tag_name("p")
        results = resultsText.text
        print('Results:', results)
        results = results.split(' resultados.')[0]
        results = results.split(' ')[(len(results.split(' ')) - 1)]
        results = int(results)
        resultPages = math.ceil(results / 20)
        print('Result pages:', resultPages)
        time.sleep(random.uniform(2, 10))
        return resultPages

    def getSubLinks(self):
        div = self.__driver.find_element_by_id("result")
        linkdata = div.find_elements_by_tag_name("p")
        linksList = []
        for data in linkdata:
            try:
                link = data.find_element_by_css_selector("a").get_attribute("href")
                print(link)
                linksList.append(link)
                time.sleep(random.uniform(1, 3))
            except Exception as e:
                print("Error in getting sublinks")
                print(e)
        print("Sublinks:", linksList)
        print("Loading sublinks done", end="\n\n")
        time.sleep(random.uniform(5, 10))
        return linksList

    def printFullPageText(self, linksList):  # I'm exploring different ways to write into the file: print(text, file=filename), f.write, utf-8
        for url in linksList:
            try:
                self.__driver.get(url)
                print(url)
                time.sleep(random.uniform(1, 10))
                content = self.__driver.find_element_by_class_name("detail-news")

                # Print title
                title = content.find_element_by_tag_name("h2")
                titleText = title.text
                print(titleText)
                print(titleText, file=self.__fileOut)

                # Print date
                date = content.find_element_by_tag_name("em")
                dateText = date.text
                print(dateText)
                print(dateText, file=self.__fileOut)

                # Print the story in the article

                storydata = content.find_elements_by_tag_name("p")
                for story in storydata:
                    storyText = story.text
                    print(storyText)
                    print(storyText, file=self.__fileOut)

                self.__pageCounter += 1
                print("Article", self.__pageCounter, "printed")
                print("\n\n************************************\n\n")
                print("\n\n************************************\n\n", file=self.__fileOut)
                if self.__pageCounter % 100 == 0:
                    print("Current time:", datetime.datetime.now().time())
                    print("Sleeping. . .")
                    time.sleep(random.uniform(300, 600))
            except Exception as e:
                print("Error in printing full page")
                print(str(e))

    # There is no need to add months
    def startDateAddMonth(self):
        if self.__startDate.month < 12:
            self.__startDate = datetime.datetime.strptime(str(self.__startDate.year) + str(self.__startDate.month + 1), "%Y%m")
        else:
            self.__startDate = datetime.datetime.strptime(str(self.__startDate.year + 1) + "01", "%Y%m")
        return self.__startDate

    def closeFile(self):
        self.__fileOut.close()


# Main loop
def main():

    syt = SeychellesNation()
    startResults = syt.getStartResults()
    endResults = syt.getEndResults()

    n = 1
    while startResults <= endResults: # An inequality can be used here to determine number of results and number of results pages
        print('\n#################################### Page ' + str(n) + " ####################################\n")
        try:
            syt.loadResultsPage(n)
            linksList = syt.getSubLinks()
        except Exception as e:  # need exceptions to be more specific
            print("Error in getting next page. There are possibly no more pages.")
            print(e)
            break
        syt.printFullPageText(linksList)
        startResults = syt.addResults()
        n += 1
    syt.closeFile()



main()

totElapsedTime = time.time() - startTime
print("Total elapsed time: ", totElapsedTime)
print("Current time:", datetime.datetime.now().time())
