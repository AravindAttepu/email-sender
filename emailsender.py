import smtplib
import csv
import mimetypes
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from tkinter import filedialog
from tkinter import *

root = Tk()
root.withdraw()

def read_template(filename):
    with open(filename, "r", encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def audiofile():
    msg = MIMEMultipart()
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav;*.ogg;*.m4a")])
    with open(file_path, 'rb') as f:
        audio_data = f.read()
        audio = MIMEAudio(audio_data)
        audio.add_header('Content-Disposition', 'attachment', filename=file_path)
        mimetype, _ = mimetypes.guess_type(file_path)
        audio.set_type(mimetype)
        msg.attach(audio)
        s.send_message(msg)
        del msg


def imagefile():
    msg = MIMEMultipart()
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif")])
    with open(file_path, 'rb') as f:
        image_data = f.read()
        image = MIMEImage(image_data, name='image.jpg')
        image.add_header('Content-Disposition', 'attachment', filename=file_path)
        msg.attach(image)
        s.send_message(msg)
        del msg  


def main():
    try:
        message_template = read_template("E:/project_expo/email sender/template.txt")
        with open("E:/project_expo/email sender/details.csv", "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            # the below statement will skip the first row
            next(csv_reader)
            for lines in csv_reader:
                msg = MIMEMultipart() # create a message
                # add in the actual person name to the message template
                message =message_template.substitute(PERSON_NAME=lines[0],SUB=lines[2],SENDER=lines[3],COMPANY=lines[4])
                print(message)
                # setup the parameters of the message
                msg['From']=MY_ADDRESS
                msg['To']=lines[1]
                msg['Subject']=lines[2]
                # add in the message body
                value=input("1. send text\n 2.send audio\n 3.send Image\n")
                if value=='1':
                    msg.attach(MIMEText(message, 'plain'))
                    # send the message via the server set up earlier.
                    s.send_message(msg)
                    del msg
                elif value=='2':
                    audiofile()
                elif value=='3':
                    imagefile()
    except Exception as e:
        print(e)    
    # Terminate the SMTP session and close the connection
    s.quit()

if __name__ == '__main__':
    MY_ADDRESS = "aravindattepu@gmail.com"
    PASSWORD = "zkcxkxfzwfiradsz"
    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)
    main()
