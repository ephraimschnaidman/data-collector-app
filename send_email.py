from email.mime.text import MIMEText
import smtplib

def send_email(email, weight, height, bmi, avg_bmi, count):
    from_email="feschnaidman26@gmail.com"
    from_password="*********" #censored to public
    to_email=email

    subject="BMI Data"
    message="Hello. This is an auto-generated email regarding your BMI information. <br> Your weight is <strong>%s</strong>. <br> Your height is <strong>%s m</strong>. <br> Your BMI is <strong>%s Kg</strong>. <br> The average BMI is <strong>%s</strong> out of <strong>%s</strong> entries so far. <br> Thank you!" % (weight, height, bmi, avg_bmi, count)
    print(message)

    msg=MIMEText(message, 'html')
    msg['Subject']=subject
    msg['To']=to_email
    msg['From']=from_email

    gmail=smtplib.SMTP('smtp.gmail.com',587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)
