import glob

codeFile= "../output/StockCodesNYSE.csv"
outFile	= "../output/Formatted/combined.csv"

def formatData(file):
	data 	= open(file,'r').read()
	records = data.split('\n')

	result	= []
	n 		= 0
	# temp= ['']

	for record in reversed(records):
		if record=="":
			continue
		if len(record.split('|'))==1:
			result[-1][3+n] = record
			n -= 1
		else:
			result.append(['','','','']+[record])
			n 	= 0
			# temp=['']

	return result


if __name__ == "__main__":
	outfile	= open(outFile,'w')
	data	= open(codeFile,'r').read()
	records = data.split('\n')
	prevCode= None
	for record in records:
		parts	= record.split(',',1)
		code 	= parts[0]
		if code==prevCode:
			continue
		else:
			prevCode = code
		company	= parts[1]
		files	= glob.glob("../output/Financial Data/"+code+"-*.csv")
		if len(files) > 0:
			for file in files:
				parts	= file.rsplit('/',1)[1].rsplit('.csv')[0].split('-')
				data 	= formatData(file)
				data[-1][0]	= company
				data[-1][1] = code
				data[-1][2]	= parts[1]

				for line in reversed(data):
					for field in line[:-1]:
						outfile.write(field+'|')
					outfile.write(line[-1]+'\n')
				# break
			# break