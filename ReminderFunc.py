import datetime
from ApiManager import ApiManager
import os
from email.message import EmailMessage
import ssl
import smtplib

class Reminder:
    inProgress = []
    notStarted = []
    
    tasks = ApiManager.get_pages()

    for task in tasks:
        props = task["properties"]
        
        # Extract task status, name, and due date
        status_select = props.get("Status", {}).get("status", {})
        status = status_select.get("name", "Unknown")
        name = props.get("Task name", {}).get("title", [{}])[0].get("text", {}).get("content", "Unknown")
        due_date = props.get("Due", {}).get("date", {}).get("start", "Unknown")
        if due_date != "Unknown":
            due_date = datetime.datetime.fromisoformat(due_date)
        else:
            due_date = None
            
        if status == "In progress":
            inProgress.append((name, due_date))  # Append (name, due_date) tuple to the inProgress list
        elif status == "Not started":
            notStarted.append((name, due_date))  # Append (name, due_date) tuple to the notStarted list
            
        # Do something with the extracted information
        print(f"Status: {status}, Name: {name}, Due Date: {due_date}")

    emailSender = "sender"
    emailPassword = os.environ.get('email_password')

    if emailPassword is None:
        raise ValueError("EMAIL_KEY environment variable is not set")

    emailReceiver = "your mail"
    
    title = "You have unfinished tasks in your TO-DO list"
    body = """
    In progress:
    {}

    Not yet started:
    {}
    """.format('\n'.join(f"{name} - {due_date}" for name, due_date in inProgress),
               '\n'.join(f"{name} - {due_date}" for name, due_date in notStarted))
    
    em = EmailMessage()
    
    em["From"] = emailSender
    em["To"] = emailReceiver
    em["Subject"] = title
    em.set_content(body)
    
    context = ssl.create_default_context()
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(emailSender, emailPassword)
        smtp.sendmail(emailSender, emailReceiver, em.as_string())

