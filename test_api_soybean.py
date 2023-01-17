import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import xlrd
location = ('test_input.xlsx')
var_wrkbk = xlrd.open_workbook(location)
sht=var_wrkbk.sheet_by_index(0)
print(sht.cell_value(1,0))