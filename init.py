from tkinter import *
import tkinter as tk

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