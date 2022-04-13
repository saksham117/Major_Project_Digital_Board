import smtplib, ssl

port = 587  # For starttls

# need to update sender_email and receiver_email and psswd

smtp_server = "smtp.gmail.com"
sender_email = ""
receiver_email = ""
password = ""
message = """\
Subject: Digital Board Teaching Access

We are glad to inform you that you have been granted teaching access. Just log out from your current session and log in again.
We hope you will enjoy using our app :)

Regards
Team Digital Board
"""

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
