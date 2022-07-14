from flask import Flask, render_template, request, redirect
import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path
import csv


app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(f'{page_name}.html')


def write_to_csv(data):
    with open('database.csv', mode='a', newline='') as database:
        email = data['email']
        subject = data['subject']
        message = data['message']
        csv_writer = csv.writer(database, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])


def send_email(data):
    body = f'''
        Contact me:

        email : {data['email']}
        subject : {data['subject']}
        message : {data['message']}
    '''

    email = EmailMessage()
    email['from'] = 'javasmtptest_86@yahoo.com'
    email['to'] = 'shayansam86@yahoo.com'
    email['subject'] = 'Contact me!'

    email.set_content(body)
    with smtplib.SMTP(host='smtp.mail.yahoo.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('javasmtptest_86@yahoo.com', 'dnbkujnvuztehzjr')
        smtp.send_message(email)


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    data = request.form.to_dict()
    if request.method == 'POST' and data['email'] and data['message']:
        try:
            write_to_csv(data)
            send_email(data)
            return redirect('thankyou')
        except:
            return redirect('error')
    else:
        return redirect('error')
