from bs4 import BeautifulSoup
import requests
from random import choice
import xlsxwriter

# Libraries required to limit the time taken by a request
import signal
from contextlib import contextmanager

class TimeoutException(Exception): pass


@contextmanager
def time_limit(seconds):
	def signal_handler(signum, frame):
		raise TimeoutException
	signal.signal(signal.SIGALRM, signal_handler)
	signal.alarm(seconds)
	try:
		yield
	finally:
		signal.alarm(0)


# BaseURL			= "https://finance.yahoo.com/quote/ACN/financials?p=ACN"
BSURL			= "https://finance.yahoo.com/quote/{0}/balance-sheet?p={0}"
ISURL			= "https://finance.yahoo.com/quote/{0}/financials?p={0}"
CFURL			= "https://finance.yahoo.com/quote/{0}/cash-flow?p={0}"

INFILE			= "../output/StockCodesNYSE.csv"

def getRequest(aurl):

	# user_agents 							= ['Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36','Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11','Opera/9.25 (Windows NT 5.1; U; en)','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)','Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)','Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1']
	# user_agent 							= choice(user_agents)
	user_agent 								= 'Mozzila/5.0'
	hdr 									= {'User-Agent':user_agent}

	print("Requesting website : "+aurl)
	while  True:
		try:
			try:
				with time_limit(300):
					req 	= requests.get(aurl,headers=hdr)
				break
			except TimeoutException:
				print('Request times out. Trying again...')
				continue
		except Exception as err:
			print('Error in request. Error :')
			print(err.message)
			continue
	
	return req

def getSoup(aurl):
	req 		= getRequest(aurl)
	content 	= req.content

	soup 		= BeautifulSoup(content,'html.parser')
	return soup


def getData(BaseURL,code,type):
	url 		= BaseURL.format(code)
	soup 		= getSoup(url)

	# Identifying the section containing data
	section		= soup.find('section',{'id':'quote-leaf-comp'})

	try:
		data 		= section.find_all('div')[-1]
	except AttributeError:
		print("Code not found : "+code)
		return
	except IndexError:
		print("Financials not found : "+code)
		return

	fields		= data.find_all('tr')

	file 		= open("../output/Financial Data/"+code+"-"+type+".csv",'w')

	for field in fields:
		columns	= field.find_all('td')
		for column in columns[:-1]:
			text= column.get_text()
			file.write(text + "|")
		file.write(columns[-1].get_text() + "\n")

	file.close()
	return


def getFinancialData(code):
	getData(BSURL,code,"BS")
	getData(ISURL,code,"IS")
	getData(CFURL,code,"CF")
	return


def begin_scrape():
	data 		= open(INFILE,'r').read()
	companies	= data.split('\n')

	for company in companies[:1]:
		code 	= company.split(',')[0]
		# name 	= company.split(',')[1]
		code 	= "ABB"
		getFinancialData(code)
	return

def temp_scrape():
	data 		= open("./StockCodesForReRun.txt",'r').read()
	codes 		= data.split('\n')

	for code in codes:
		getFinancialData(code)

	return

if __name__ == "__main__":
	# begin_scrape()
	temp_scrape()
	print("Done")