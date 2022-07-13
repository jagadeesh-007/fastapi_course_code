import pandas as pd
import glob
import shutil, os
import datetime

# getting excel files to be merged from the Desktop
path = "D:\\PHRoffice\\district_reports\\test\\"
move = "D:\\PHRoffice\\district_reports\\test\\old\\"
# read all the files with extension .xlsx i.e. excel
filenames = glob.glob(path + "\*.xlsx")
print('File names:', filenames)

# empty data frame for the new output excel file with the merged excel files
outputxlsx = pd.DataFrame()

# for loop to iterate all excel files
for file in filenames:
   # using concat for excel files
   # after reading them with read_excel()
   df = pd.concat(pd.read_excel( file, sheet_name=None), ignore_index=True, sort=False)

   # appending data of excel files
   outputxlsx = outputxlsx.append( df, ignore_index=True)

# To set booleian value to 0 and 1
outputxlsx['Active'] = outputxlsx['Active'].astype(bool)

# date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
# print(f"filename_{date}")

print('Final Excel sheet now generated at the same location:')
outputxlsx.to_excel("D:\\PHRoffice\\district_reports\\test\\District_user_report.xlsx", index=False)

# Rename the output with the current date
Current_Date = datetime.datetime.today().strftime ('%d-%b-%Y')
os.rename(r'D:\PHRoffice\district_reports\test\District_user_report.xlsx',r'D:\PHRoffice\district_reports\test\District_user_report_' + str(Current_Date) + '.xlsx')


# filenames = glob.glob(path + "\*.xlsx")
# for f in filenames:
#     shutil.move(f, glob.glob(move))
