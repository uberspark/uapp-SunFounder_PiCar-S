import csv
import sys

# Expecting the filename to be passed as an argument
if len(sys.argv) == 2:
   file_name = sys.argv[1]
   with open(file_name) as csv_file:
      csv_reader = csv.reader(csv_file,skipinitialspace=True,delimiter=',')
      line_count=0
      error_score = 0
      for row in csv_reader:
            print(row[0], row[1], row[2], row[3], row[4])
            line_count += 1
            if (row[0]=='1') or  (row[4]=='1') :
                error_score += 2
            elif (row[1] == '1') or (row[3]=='1') :
                error_score += 1
            elif (row[2]=='0') :
                error_score += 3
            print("error_score: ",error_score)
      print(f'Processed {line_count} lines.')
else:
    print("\nUsage: python3 score_line.py filename.log\n")
