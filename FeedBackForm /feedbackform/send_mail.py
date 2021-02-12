import smtplib
from email.mime.text import MIMEText


def send_mail(customer, email, guest, room, arrival, departure, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '2c88ce6de01198'
    password = 'a8dec52e4e7cde'
    message = f"<h3>Reservation Submission</h3><ul><li>Customer: {customer}</li><li>Email: {email}</li><li>Guest: {guest}</li><li>Room: {room}</li><li>Arrival: {arrival}</li><li>Departure: {departure}</li><li>Comments: {comments}</li></ul>"

    sender_email = 'shahriarksaurov@gmail.com'
    receiver_email = 'shahriar.saurov@yahoo.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Hotel Reservation'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with smtplib.SMTP(smtp_server,port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email,msg.as_string())
