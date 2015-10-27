import anfis
import membership #import membershipfunction, mfDerivs
import numpy
import xlrd


# read the excel files to load the inputs
#   Build the inputs
workbook=xlrd.open_workbook('d_set_all_50_centerofmass.xls',on_demand= True)
worksheet=workbook.sheet_by_index(0)
all_inputs=[]
all_targets=[]
row=0
column=16

print "opening the sheet to read values"
while row<300:
	inc=0
	temp=[] #empty list for each training example
	print "iterating through each row"
	while inc<14:
		#print worksheet.cell(row,column+inc).value
		temp.append(worksheet.cell(row,column+inc).value)
		inc+=1
	all_inputs.append(temp)
	row+=1

print all_inputs

#reading the label vector
row=301
column=16

while row<601:
	inc=0
	temp=[] #empty list for each training output
	print "iterating through each row"
	while inc<50:
		#print worksheet.cell(row,column+inc).value
		temp.append(worksheet.cell(row,column+inc).value)
		inc+=1
	all_targets.append(temp)
	row+=1
print all_targets


mf = [[['gaussmf',{'mean':-11.,'sigma':5.}],['gaussmf',{'mean':-8.,'sigma':5.}],['gaussmf',{'mean':-14.,'sigma':20.}],['gaussmf',{'mean':-7.,'sigma':7.}]],
            [['gaussmf',{'mean':-10.,'sigma':20.}],['gaussmf',{'mean':-20.,'sigma':11.}],['gaussmf',{'mean':-9.,'sigma':30.}],['gaussmf',{'mean':-10.5,'sigma':5.}]]]


mfc = membership.membershipfunction.MemFuncs(mf)
anf = anfis.ANFIS(all_inputs, all_targets, mfc)
anf.trainHybridJangOffLine(epochs=10)
print round(anf.consequents[-1][0],6)
print round(anf.consequents[-2][0],6)
print round(anf.fittedValues[9][0],6)
if round(anf.consequents[-1][0],6) == -5.275538 and round(anf.consequents[-2][0],6) == -1.990703 and round(anf.fittedValues[9][0],6) == 0.002249:
	print 'test is good'
anf.plotErrors()
anf.plotResults()
