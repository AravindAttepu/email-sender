import smtplib
import csv
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def read_template(filename):
 with open(filename, "r", encoding='utf-8') as template_file:
  template_file_content = template_file.read()
 return Template(template_file_content)
def main():
 try:
  message_template = read_template("E:/project_expo/email sender/template.txt")
  MY_ADDRESS = "aravindattepu@gmail.com"
  PASSWORD = "zkcxkxfzwfiradsz"
# set up the SMTP server
  s = smtplib.SMTP(host='smtp.gmail.com', port=587)
  s.starttls()
  s.login(MY_ADDRESS, PASSWORD)
 
  with open("E:/project_expo/email sender/details.csv", "r") as csv_file:
   csv_reader = csv.reader(csv_file, delimiter=',')
  # the below statement will skip the first row
   next(csv_reader)
   for lines in csv_reader:
     msg = MIMEMultipart() # create a message
# add in the actual person name to the melinesssage template
     message =message_template.substitute(PERSON_NAME=lines[0],MSG=lines[3],
     SENDER=lines[4],COMPANY=lines[5])
     print(message)
# setup the parameters of the message
     msg['From']=MY_ADDRESS
     msg['To']=lines[1]
     msg['Subject']=lines[2]
# add in the message body
     msg.attach(MIMEText(message, 'plain'))
# send the message via the server set up earlier.
     s.send_message(msg)
     del msg
 except Exception as e:
  print(e)    
 
 # Terminate the SMTP session and close the connection
  s.quit()
if __name__ == '__main__':
 main()