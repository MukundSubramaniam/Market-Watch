from tkinter import *
import tkinter as tk
import random
import string
import lxml
import yfinance as yf
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from pandas import DataFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import style
from pyscreenshot import grab
import smtplib


################################################################################
def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb

def init(data):
    data.numRows = 15
    data.numBgLeft = []
    data.numBgRight = []
    data.timeCount = 0
    data.titleOn = False
    data.categories = False
    data.ticker = None
    data.industriesDict = {
    'Finance': set(['J P Morgan Chase & Co : JPM', 'Bank of America Corporation : BAC', 'Wells Fargo & Company: WFC', 'HSBC Holdings plc: HSBC', 'Citigroup Inc.: C', 'HDFC Bank Limited: HDB', 'Royal Bank Of Canada: RY', 'Toronto Dominion Bank (The): TD']), 
    'Technology': set(['Microsoft Corporation: MSFT', 'Apple Inc.: AAPL', 'Alphabet Inc.: GOOGL/GOOG', 'Facebook, Inc.: FB', 'Cisco Systems, Inc.: CSCO', 'Intel Corporation: INTC', 'Taiwan Semiconductor Manufacturing Company Ltd.: TSM', 'Oracle Corporation: ORCL']), 
    'Healthcare':set(['Johnson & Johnson: JNJ', 'Pfizer, Inc.: PFE', 'UnitedHealth Group Incorporated: UNH', 'Merck & Company, Inc.: MRK', 'Novartis AG: NVS', 'Abbott Laboratories: ABT', 'Medtronic plc: MDT', 'Novo Nordisk A/S: NVO;']), 
    'Transportation': set(['Union Pacific Corporation: UNP', 'United Parcel Service, Inc.: UPS', 'Canadian National Railway Company: CNI', 'CSX Corporation: CSX', 'Norfolk Souther Corporation: NSC', 'FedEx Corporation: FDX', 'Delta Air Lines, Inc.: DAL', 'Canadian Pacific Railway Limited: CP']), 
    'Basic Industries Companies': set(['Procter & Gamble Company (The): PG', 'Unilever PLC: UL', 'Unilever NV: UN', 'BHP Group Limited: BHP', 'Linde plc: LIN', 'Rio Tinto Plc: RIO', 'VALE S.A.: VALE', 'DuPont de Nemours, Inc.: DD']), 
    'Consumer Services': set(['Amazon.com, Inc.: AMZN', 'Walmart Inc.: WMT', 'Walt Disney Company (The): DIS', 'Home Depot, Inc. (The): HD', 'Comcast Corporation: CMCSA', 'Netflix, Inc.: NFLX', 'McDonalds Corporation: MCD', 'Costco Wholesale Corporation: COST']), 
    'Public Utilities': set(['Verizon Communications Inc.: VZ', 'AT&T Inc.: T', 'China Mobile (Hong Kong) Ltd.: CHL', 'NextEra Energy, Inc.: NEE', 'Duke Energy Corporation: DUK', 'T-Mobile US, Inc.: TMUS', 'Enterprise Products Partners L.P.: EPD', 'Dominion Energy, Inc.: D']), 
    'Miscellaneous': set(['Alibaba Group Holding Limited: BABA', 'Visa Inc.: V', 'Mastercard Incorporated: MA', 'PayPal Holdings, Inc.: PYPL', 'Accenture plc: ACN', 'Booking Holdings Inc.: BKNG', 'Fidelity National Information Services, Inc.: FIS', 'Worldpay, Inc.: WP'])}
    
    data.industryRows = 8
    data.industries = ['Finance', 'Technology', 'Healthcare', 'Transportation', 'Basic Industries Companies', 'Consumer Services', 'Public Utilities', 'Miscellaneous']
    data.companiesList = None
    data.text = ''
    data.ticker = None
    data.legalChar = string.ascii_letters + string.whitespace + string.punctuation
    data.legalChar2 = string.digits + string.punctuation
    data.legalChar3 = string.ascii_letters + string.punctuation
    data.companiesPage = False
    data.invalidTicker = False
    data.dates = ['5d','1mo','6mo','1y','5y','10y']
    data.searchBar = False
    data.previousPrice = None
    data.currentPrice = None
    data.stock = None
    data.printStock = False
    data.stockColor = 'white'
    data.change = '0.00'
    data.datesPage = False
    data.graphPage = False
    data.monteCarlo = False
    data.download = None
    data.timeLength = None
    data.timePeriod = None
    data.graphs = ['Market Close Prices', 'Market Volume', 'Market Daily Change', 'Monte Carlo Simulation']
    data.infoType = None
    data.count = 0
    data.count2 = 0
    data.prices = None
    data.datesList = None
    data.distBetweenPointX = None
    data.disBetweenPointY = None
    data.maxValue = None
    data.separationX = None
    data.simulations = None
    data.lastPrice = None
    data.saveGraph = False
    data.allYPoints = []
    data.allXPoints = []
    data.save = 'Save'
    data.track = False
    data.email = ''
    data.guessPrice = ''
    data.checkPrice = False
    data.ticker2 = ''
    data.instantPrice = None    

def mousePressed(event, data):
    for row in range(data.industryRows):
        if event.x > 50 and event.x < 750 and event.y > (180 + row * 50) and \
        event.y < (180 + (row + 1) * 50) and data.searchBar and not data.titleOn and not data.companiesPage and data.categories:
            data.categories = False
            data.companiesPage = True
            data.companiesList = list(data.industriesDict[data.industries[row]])
            
    for row in range(6):
        if data.datesPage and not data.graphPage and not data.printStock and event.x > 100 and event.x < 700 and event.y > 100 + 75*(row) and event.y < 100 + 75*(row + 1):
            if row == 0:
                data.separationX = 1
            if row == 1:
                data.separationX = 6
            if row == 2:
                data.separationX = 36
            if row == 3:
                data.separationX = 72
            if row == 4:
                data.separationX = 360
            if row == 5:
                data.separationX = 720

            data.timePeriod = data.dates[row]
            data.graphPage = True
            data.datesPage = False
            data.monteCarlo = False
            data.titleOn = False

    for row in range(3):
        if data.printStock and event.x > 175 and event.x < data.width - 175 and event.y > 225 + 75*(row) + 20 and event.y < 225 + 75*(row + 1):
            data.infoType = data.graphs[row]
            data.printStock = False
            data.datesPage = True

    if data.printStock and event.x > 175 and event.x < data.width - 175 and event.y > 225 + 75*(3) + 20 and event.y < 225 + 75*(3 + 1):
        data.monteCarlo = True  
            
    if data.graphPage and not data.printStock and not data.monteCarlo and event.x > 700 and event.y > 50 and event.x <750 and event.y < 100:
        data.saveGraph = True
        saveGraph(data)
    
    if not data.track and data.printStock and not data.monteCarlo and not data.graphPage and event.x > 175 and event.y > 175 and event.x < 625 and event.y < 225:
        data.printStock = False
        data.track = True

def saveGraph(data):
    im = grab(bbox=(350, 40, 1100, 600))
    im.save('/Users/mukundsubramaniam/Desktop/Market_Watch_Saved_Graphs/' + data.infoType + '.png', 'PNG')


def getStockInfo(data):
    
    data.stock = yf.Ticker(data.ticker)
    data.currentPrice = round(data.stock.info['regularMarketPrice'],2)
    if data.guessPrice != '' and data.ticker2 != '' and data.email != '' and float(data.guessPrice) == data.currentPrice:
        message = 'Your %s stock has reached %s!' %(data.ticker2, data.guessPrice)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('MarketWatchNotifications@gmail.com', 'TermProject112!')
        server.sendmail('MarketWatchNotifications@gmail.com', data.email, message)
        server.quit()
        
    if data.previousPrice == None:
        data.previousPrice = data.currentPrice
    
    if data.currentPrice > data.previousPrice:
        data.stockColor = 'green'
        data.change = ''
        data.change ='+' + str(round(abs(data.previousPrice - data.currentPrice),2))
        
    if data.previousPrice > data.currentPrice:
        data.stockColor = 'red'
        data.change = ''
        data.change ='-' + str(round(abs(data.previousPrice - data.currentPrice),2))
    data.previousPrice = data.currentPrice
    data.printStock = True

def keyPressed(event, data):
    data.invalidTicker = False
    if event.keysym == 'space':
        data.text = ''
        if data.titleOn:
            data.searchBar = True
            data.titleOn = False
            data.categories = True
            data.companiesPage = False
            data.printStock = False
            data.datesPage = False
            data.monteCarlo = False
            data.graphPage = False
            data.timePeriod = None
            data.infoType = None
            data.count = 0
            data.count2 = 0
            data.datesList = None
            data.prices = None
            data.distBetweenPointX = None
            data.maxValue = None
            data.distBetweenPointY = None
            data.download = None
            data.timeLength = None
            data.lastPrice = None
            data.save = 'Save'
            data.track = False
            data.email = ''
            data.checkPrice = False
        else:
            data.titleOn = True
            data.categories = False
            data.companiesPage = False
            data.printStock = False
            data.previousPrice = None
            data.currentPrice = None
            data.change = '0.00'
            data.stockColor = 'white'
            data.datesPage = False
            data.monteCarlo = False
            data.graphPage = False
            data.timePeriod = None
            data.infoType = None
            data.count = 0
            data.count2 = 0
            data.datesList = None
            data.prices = None
            data.distBetweenPointX = None
            data.maxValue = None
            data.distBetweenPointY = None
            data.lastPrice = None
            data.save = 'Save'
            data.track = False
            data.email = ''
            data.checkPrice = False
            
    if data.searchBar and event.char in data.legalChar:  
        data.text += event.char
    if event.keysym == 'BackSpace' and data.searchBar:
        data.text = data.text[:-1]
    if data.searchBar and event.keysym == 'Return':
        data.ticker = data.text
        data.text = ''
        try:
            getStockInfo(data)
            data.companiesPage = False
            data.categories = False
            data.searchBar = False
            data.titleOn = False
        except:
            data.invalidTicker = True
    
    if data.track and not data.checkPrice and not data.printStock and not data.monteCarlo and not data.searchBar and not data.graphPage and event.char in data.legalChar2:
        data.guessPrice += event.char

    if data.checkPrice and data.track and not data.printStock and not data.monteCarlo and not data.searchBar and not data.graphPage and event.keysym == 'Return':
        data.printStock = True
        data.track = False
        data.checkPrice = False
    
    if data.track and not data.checkPrice and not data.printStock and not data.monteCarlo and not data.searchBar and not data.graphPage and event.keysym == 'Return':
        data.ticker2 = data.ticker
        data.instantPrice = data.currentPrice
        data.checkPrice = True

    if data.track and not data.checkPrice and not data.printStock and not data.monteCarlo and not data.searchBar and not data.graphPage and event.keysym == 'BackSpace': 
        data.guessPrice = data.guessPrice[:-1]
    
    if data.checkPrice and data.track and not data.printStock and not data.monteCarlo and not data.searchBar and not data.graphPage and event.char in data.legalChar3:
        data.email += event.char
    
    if data.checkPrice and data.track and not data.printStock and not data.monteCarlo and not data.searchBar and not data.graphPage and event.keysym == 'BackSpace':
        data.email = data.email[:-1]

    if event.keysym == 'Escape' and not data.categories and data.companiesPage and not data.titleOn:
        
        data.categories = True
        data.companiesPage = False

    if event.keysym == 'Escape' and data.printStock and not data.categories and not data.companiesPage and not data.titleOn and not data.searchBar:
        data.printStock = False
        data.categories = True
        data.searchBar = True
        data.titleOn = False
        data.previousPrice = None
        data.currentPrice = None
        data.change = '0.00'
        data.stockColor = 'white'
    if event.keysym == 'Escape' and data.datesPage and not data.monteCarlo and not data.printStock and not data.categories and not data.companiesPage and not data.titleOn and not data.searchBar:
        data.datesPage = False
        data.printStock = True

    if event.keysym == 'Escape' and data.monteCarlo and not data.datesPage and not data.printStock and not data.categories and not data.companiesPage and not data.titleOn and not data.searchBar:
        data.printStock = True
        data.monteCarlo = False
        data.timePeriod = None
        data.count = 0
        data.count2 = 0
        data.datesList = None
        data.prices = None
        data.distBetweenPointX = None
        data.maxValue = None
        data.distBetweenPointY = None
        data.download = None
        data.timeLength = None
        data.lastPrice = None
        data.save = 'Save'
        
    if event.keysym == 'Escape' and data.graphPage and not data.monteCarlo and not data.datesPage and not data.printStock and not data.categories and not data.companiesPage and not data.titleOn and not data.searchBar:
        data.datesPage = True
        data.graphPage = False
        data.timePeriod = None
        data.count = 0
        data.count2 = 0
        data.datesList = None
        data.prices = None
        data.distBetweenPointX = None
        data.maxValue = None
        data.distBetweenPointY = None
        data.download = None
        data.timeLength = None
        data.lastPrice = None
        data.save = 'Save'
    
    if event.keysym == 'Escape' and data.track and not data.printStock and not data.monteCarlo and not data.datesPage and not data.graphPage:
        data.track = False
        data.printStock = True
        data.email = ''
        
def timerFired(data):
    data.timeCount += 1
    if data.timeCount % 15 == 0 and data.numBgLeft != [] and data.numBgRight != []:
        data.numBgLeft.insert(0,data.numBgLeft.pop())
        data.numBgRight.insert(0,data.numBgRight.pop())
    if len(data.numBgRight)!= data.numRows - 1 and len(data.numBgLeft) != data.numRows - 1:
        makeNumbers(data)
    if data.timeCount == 15:
        data.titleOn = True
    if data.timeCount % 10 == 0 and data.printStock:
        getStockInfo(data)

        
def makeNumbers(data):
    firstNum = round(random.uniform(0, 10000),4)
    secondNum = round(random.uniform(-5, 10),2)
    thirdNum = round(random.uniform(-50, 100),2)
    fourthNum = round(random.uniform(0, 10000),4)
    fifthNum = round(random.uniform(-5, 10),2)
    sixthNum = round(random.uniform(-50, 100),2)
    x1 = 350
    y1 = data.height//data.numRows
    x2 = 750
    y2 = data.height//data.numRows
    r = 10
    leftUpTriangle = ((x1, y1 - r),(x1 + r, y1 + r/2),(x1 - r, y1 + r/2))
    leftDownTriangle = ((x1, y1 + r),(x1 + r, y1 - r/2),(x1 - r, y1 - r/2))
    rightUpTriangle = ((x2, y2 - r),(x2 + r, y2 + r/2),(x2 - r, y2 + r/2))
    rightDownTriangle = ((x2, y2 + r),(x2 + r, y2 - r/2),(x2 - r, y2 - r/2))
    if secondNum < 0 or thirdNum < 0:
        colorLeft = 'red'
        triangleLeft = leftDownTriangle
    elif secondNum >= 0 and thirdNum >= 0:
        triangleLeft = leftUpTriangle
        colorLeft = 'green'
    data.numBgLeft.append((firstNum, secondNum, thirdNum, colorLeft, triangleLeft))
    if fourthNum < 0 or fifthNum < 0:
        colorRight = 'red'
        triangleRight = rightDownTriangle
    else:
        colorRight = 'green'
        triangleRight = rightUpTriangle
    data.numBgRight.append([fourthNum, fifthNum, sixthNum, colorRight, triangleRight])

def drawRightNumbers(canvas, data):
    count = 1
    for num in data.numBgLeft:
        canvas.create_text(75, count * data.height//data.numRows, text = \
        str(num[0]), fill = num[3], font = 'Courier 22')
        canvas.create_text(190, count * data.height//data.numRows, text = \
        str(num[1]), fill = num[3], font = 'Courier 22')
        canvas.create_text(275, count * data.height//data.numRows, text = \
        str(num[2]), fill = num[3], font = 'Courier 22')
        canvas.create_polygon((num[4][0][0],num[4][0][1] + (count - 1) * data.height//data.numRows),(num[4][1][0], num[4][1][1] + (count - 1) * data.height//data.numRows),(num[4][2][0], num[4][2][1] + (count - 1) * data.height//data.numRows), fill = num[3])
        count += 1

def drawLeftNumbers(canvas,data):
    count = 1
    for num in data.numBgRight:
        canvas.create_text(475, count * data.height//data.numRows, text = \
        str(num[0]), fill = num[3], font = 'Courier 22')
        canvas.create_text(590, count * data.height//data.numRows, text = \
        str(num[1]), fill = num[3], font = 'Courier 22')
        canvas.create_text(675, count * data.height//data.numRows, text = \
        str(num[2]), fill = num[3], font = 'Courier 22')
        canvas.create_polygon((num[4][0][0],num[4][0][1] + (count - 1) * data.height//data.numRows),(num[4][1][0], num[4][1][1] + (count - 1) * data.height//data.numRows),(num[4][2][0], num[4][2][1] + (count - 1) * data.height//data.numRows), fill = num[3])
        count += 1

def drawAppTitle(canvas, data):
    diff = 100
    canvas.create_rectangle(diff, diff, data.width - diff, data.height - diff, fill = _from_rgb((101,147,205)), outline = _from_rgb((29,41,81)), width = 15)
    canvas.create_text(data.width/2, data.height/3, text = 'Market Watch', fill = 'white', font= 'fixedsys 80 bold')
    canvas.create_text(data.width/2, data.height/3 + 75, text = 'Search company stocks and', fill = 'white', font= 'fixedsys 25 italic')
    canvas.create_text(data.width/2, data.height/3 + 110, text = 'visualize their performances!', fill = 'white', font= 'fixedsys 25 italic')

    canvas.create_text(data.width/2, 2* data.height/3 + 40, text = '(Click Spacebar to Continue and', fill = 'white', font= 'Courier 20 italic')
    canvas.create_text(data.width/2, 2* data.height/3 + 60, text = 'click again to return to Home Screen)', fill = 'white', font= 'Courier 20 italic')
    
def drawSearchBar(canvas, data):
    canvas.create_rectangle(120, 75, 680, 115, fill = 'white', outline = _from_rgb((0,128,255)), width = 3)
    canvas.create_text(130, 95, text = data.text, anchor = 'w', font = 'Courier 20', fill = 'black')
    canvas.create_text(data.width/2, 40, text = 'Type the Ticker Symbol of any company and click Enter', fill = 'white', font = 'fixedsys 30 bold')

def drawSearchIndustry(canvas, data):
    canvas.create_text(data.width/2, 150, text = 'Click on selected industries below and search', fill = 'white', font = 'fixedsys 30 bold')
    canvas.create_rectangle(50, 180, 750, 580, fill = 'white')
    for row in range(data.industryRows):
        if row % 2 == 0:
            color =_from_rgb((101,147,205))
        elif row % 2 == 1:
            color = _from_rgb((101,147,205))
        canvas.create_rectangle(50, 180 + row * 50, 750, 180 + (row + 1) * 50, fill = color, outline = _from_rgb((29,41,81)), width = 4)
        canvas.create_text(400, 205 + row * 50, text = data.industries[row], fill = 'white', font = 'Helvetica 25 bold')    

def drawCompaniesPage(canvas, data):
    canvas.create_rectangle(50, 180, 750, 580, fill = _from_rgb((15,82,186)))
    canvas.create_text(data.width/2, 150, text = 'Click ESC to go back to list of industries', fill = 'white', font = 'fixedsys 30 bold')
    for row in range(data.industryRows):
         canvas.create_text(400, 205 + row * 50, text = data.companiesList[row], fill = 'white', font = 'Verdana 20 bold')

def drawStock(canvas, data):
    canvas.create_rectangle(50, 50, data.width - 50, data.height - 50, fill = _from_rgb((101,147,205)), outline = _from_rgb((29,41,81)), width = 10)
    canvas.create_text(data.width/2, 100, text = str(round(data.currentPrice, 3))  + ' USD  ' + str(data.change),fill=  data.stockColor, font = 'Verdana 60 bold')
    
    canvas.create_text(data.width/2, 140, text = 'Live Market Price', font = 'Courier 30 bold')
    
    canvas.create_text(data.width/2, 27, text = 'Click on a Tool!', fill = 'white', font = 'Verdana 30 bold')
    canvas.create_rectangle(175, 175, data.width - 175, 225, fill = _from_rgb((29,41,81)))
    canvas.create_text(data.width/2, 200, text = 'Track', font = 'Verdana 25 bold', fill = 'white')

    for row in range(4):
        canvas.create_rectangle(175, 225 + 75*(row) + 20, data.width - 175, 225 + 75*(row + 1), fill = _from_rgb((29,41,81)))
        canvas.create_text(data.width/2, (535 + 150 * row)/2, text = data.graphs[row], font = 'Verdana 25 bold', fil = 'white')

def drawDatesPage(canvas, data):
    canvas.create_text(data.width/2, 30, text = 'Pick a Time Period', fill = 'white', font = 'Verdana 25 bold')
    canvas.create_text(data.width/2, 70, text = 'Click ESC to go back!', fill = 'white', font = 'fixedsys 30 bold')
    for row in range(6):
        canvas.create_rectangle(100,100 + 75*(row), 700, 100 + 75*(row + 1), fill = _from_rgb((101,147,205)), outline = _from_rgb((29,41,81)), width = 5)
        canvas.create_text(data.width/2, 65 + 75*(row+1), text = data.dates[row], fill = 'white', font = 'Verdana 25 bold')

def drawGraphPage(canvas, data):
    canvas.create_rectangle(50,50,data.width - 50, data.height - 50, fill = _from_rgb((101,147,205)))
    canvas.create_line(100, data.height - 100, 100,100, width = 7)
    canvas.create_line(100, data.height - 100, data.width - 100,data.height - 100, width = 7)
    canvas.create_text(data.width/2, 570, text = 'Click ESC to go back!', fill = 'white', font = 'fixedsys 30 bold')
    if data.count2 == 0:
        data.download = yf.download(data.ticker, period = data.timePeriod)
        ticker = data.download
        info = None
        
        if data.infoType == 'Market Close Prices':
            info = ticker.Close 
        if data.infoType == 'Market Volume':
            info = ticker.Volume
        if data.infoType == 'Market Daily Change':
            info = abs(ticker.Open - ticker.Close)
        data.datesList = info.index.tolist()
        data.prices = info.tolist()
        data.distBetweenPointX = 600/len(data.prices)
        data.maxValue = max(data.prices)
        data.distBetweenPointY = (data.height - 200)/data.maxValue

    for i in range(0, len(data.datesList), data.separationX):
        canvas.create_text(100 + (i)*data.distBetweenPointX,525,text = str(data.datesList[i].date()),font = 'Courier 15')
        canvas.create_line(100 + (i)*data.distBetweenPointX, 520, 100 + (i)*data.distBetweenPointX, 100, fill = 'black')

    for i in range(0,len(data.datesList)):
        if i == len(data.prices) - 1:
            break
        currentPrice = data.prices[i]
        nextPrice = data.prices[i+1]
        canvas.create_line(100 + (i)*data.distBetweenPointX, data.height - currentPrice * data.distBetweenPointY - 100, 100 + (i + 1)*data.distBetweenPointX, data.height - nextPrice * data.distBetweenPointY - 100, width = 3, fill = 'navy')
        
    for num in range(0,int(data.maxValue), math.ceil(data.maxValue/10)):
        canvas.create_text(80, 500 - num * data.distBetweenPointY, text = str(num), fill = 'black', font = 'Courier 15')
        canvas.create_line(90,500 - num * data.distBetweenPointY, 700, 500 - num * data.distBetweenPointY, fill = 'black')
        
    canvas.create_text(data.width/2, 25, text = data.infoType, fill = 'white', font = 'Verdana 30 bold')
    canvas.create_rectangle(700,50,750,100, fill = '', outline = 'white', width = 4)
    canvas.create_text(725, 75, text = data.save, font = 'Verdana 12 bold')
    data.count2 += 1

def drawMonteCarlo(canvas, data):
    if data.count == 0:        
        stock = yf.download(data.ticker, period = '1y')
        
        prices = stock.Close
        
        returns = prices.pct_change()
        data.lastPrice = prices[-1]
        trials = 1000
        days = 252
        data.simulations = pd.DataFrame()
        volatility = returns.std()
        
        for trial in range(trials):
        
            prediction = []
            
            price = data.lastPrice * (1 + np.random.normal(0, volatility))

            prediction.append(price)
        
            for day in range(days):
        
                price = prediction[day] * (1 + np.random.normal(0, volatility))
                
                prediction.append(price)
                data.allYPoints.append(price)
                data.allXPoints.append(day)
                
            data.simulations[trial] = prediction
        
        fig = plt.figure()
        
        fig.suptitle('Monte Carlo Simulation:' + data.ticker.upper())
        
        plt.plot(data.simulations)

        #line of best fit for monte carlo graphs (gives general trend) 
        (m, b) = np.polyfit(data.allXPoints, data.allYPoints, 1)

        yp = np.polyval([m, b], data.allXPoints)
        
        plt.plot(data.allXPoints, yp, color = 'black')
        plt.axhline(y = int(data.lastPrice), color = 'red', linestyle = '-')
        
        
        plt.xlabel('Day')
        plt.ylabel('Price')
        plt.show()
    data.monteCarlo = False

def drawTrack(canvas, data):
    
    canvas.create_rectangle(50, 50,data.width - 50, data.height - 50, fill = _from_rgb((101,147,205)))
    canvas.create_text(data.width/2, 20, text = 'Click ESC to go back!', fill = 'white', font = 'fixedsys 30 bold')
    canvas.create_rectangle(120, 225, 680, 265, fill = 'white', outline = _from_rgb((0,128,255)), width = 3)
    canvas.create_text(130, 245, text = data.guessPrice, anchor = 'w', font = 'Courier 20', fill = 'black')
    canvas.create_text(data.width/2, 170, text = 'Type the Stock Price (to 2 decimal places) at', fill = 'white', font = 'fixedsys 30 bold')
    canvas.create_text(data.width/2, 200, text = 'which you want to be alerted and click enter!', fill = 'white', font = 'fixedsys 30 bold')
    canvas.create_rectangle(120, 355, 680, 395, fill = 'white', outline = _from_rgb((0,128,255)), width = 3)
    canvas.create_text(130, 375, text = data.email, anchor = 'w', font = 'Courier 20', fill = 'black')
    canvas.create_text(data.width/2, 300, text = 'Type the email that you wish to be', fill = 'white', font = 'fixedsys 30 bold')
    canvas.create_text(data.width/2, 330, text = 'notified at and click enter!', fill = 'white', font = 'fixedsys 30 bold')


def redrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill = 'black')
    drawRightNumbers(canvas, data)
    drawLeftNumbers(canvas,data)
    if data.titleOn:
        drawAppTitle(canvas, data)
    if not data.titleOn and data.searchBar and data.timeCount > 15:
        drawSearchBar(canvas, data)
        if data.invalidTicker:
            canvas.create_text(265, 95, text = 'Invalid Ticker Entered', font = 'Courier 20 bold', fill = 'red')
        if data.categories:
            drawSearchIndustry(canvas, data)
        if not data.categories and data.companiesPage:
            drawCompaniesPage(canvas, data)
    if data.printStock and not data.companiesPage and not data.titleOn and not data.searchBar:
        drawStock(canvas, data)

    if data.datesPage and not data.printStock and not data.monteCarlo:
        drawDatesPage(canvas, data)

    if data.count == 0 and data.graphPage and not data.datesPage and not data.monteCarlo and not data.printStock and not data.titleOn and not data.searchBar and not data.companiesPage:
        drawGraphPage(canvas, data)

    if data.monteCarlo and not data.datesPage and not data.graphPage and data.printStock and not data.titleOn and not data.searchBar and not data.companiesPage:
        drawMonteCarlo(canvas, data)
    
    if data.saveGraph and data.graphPage and not data.monteCarlo and not data.datesPage and not data.printStock:
        data.save = 'Saved!'
        
    if data.track and not data.printStock and not data.monteCarlo and not data.graphPage:
        drawTrack(canvas, data)
    

####################################
# Citation: From 15112 website (https://www.cs.cmu.edu/~112/index.html)
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(800, 600)