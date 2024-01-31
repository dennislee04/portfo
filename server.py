from flask import Flask, render_template, url_for, request, redirect
import csv
import requests
import hashlib
import smtplib
from email.message import EmailMessage

app = Flask(__name__)


@app.route('/')
def my_home():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    # write_type_to_file(page_name, type(page_name))
    if page_name == "Baseball.html":
        fileData = read_csv_to_html(page_name)
        return render_template(page_name, myData=fileData)
    else:
        return render_template(page_name)


# This is for submitting the contact form
@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == "POST":
        try:
            data = request.form.to_dict()
            # print(data)
            # write_to_file(data)
            write_to_csv(data)
            send_email(data)
            return redirect('thankyou.html')
        except:
            return 'did not save to database'
    else:
        return 'something went wrong. Try again!'


def write_type_to_file(pagename, pagename_type):
    with open('type.txt', mode='a') as database0:
        filetype = database0.write(f'\n{pagename}, {pagename_type}')

def read_csv_to_html(file):
    filename = f'{file}'
    data = pandas.read_csv(filename, header=0)
    myData = data.values 
    return myData

# This will write the user's contact information to the database.txt file
def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        file = database.write(f'\n{email}, {subject}, {message}')


# This will write the user's contact information to the database.csv file
def write_to_csv(data):
    with open('database.csv', mode='a', newline='') as database2:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])


def send_email(data):
    email = EmailMessage()
    email['from'] = 'leedennis04@gmail.com'
    email['to'] = 'leedennis04@gmail.com'
    email['subject'] = data["subject"]
    message = "From: " + data["email"] + "\n\n" + data["message"]

    email.set_content(message)
    password = ""

    with open('pwd_key.txt', mode='r') as file:
        password = file.readline()

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('leedennis04@gmail.com', str(password))
        smtp.send_message(email)


# This is the form for checking the password against the "https://haveibeenpwned.com/Passwords" API
@app.route('/password_check', methods=['POST', 'GET'])
def submit_form2(data="Lets see if you have a Strong Password!"):
    if request.method == "POST":
        try:
            data = request.form.to_dict()
            pwd= str(data['Password To Check'])
            count = pwned_api_check(pwd)
            #return {data}
            if (count):
                 # return render_template('workone.html', data=f"Your password: \'{pwd[0]}\' was FOUND: {count} times! You should change your password!")
                return render_template('workone.html', data=f"Your password was FOUND: {count} times. You should change your password!")
            else:
                 # return render_template('workone.html', data=f"Your password: \'{pwd[0]}\' was NOT FOUND. Carry on!")
                return render_template('workone.html', data=f"Your password was NOT FOUND. Carry on!")
        except:
            return 'did not check against the database'
    else:
        return 'something went wrong with button. Try again!'


# This will test to make sure that it can connect to the "https://haveibeenpwned.com/Passwords" API
def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching {res.status_code}, please check API & try again!')
    return res


# This will hash the user inputed password & will split this into 2 strings (first 5 char & all the char after the 5th)
def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks(response, tail)


# This will used the hased password & check against the "https://haveibeenpwned.com/Passwords" API to see how many times it shows up there
def get_password_leaks(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

# open CSV file in web-browser

"""
@app.route('/index.html')
def my_index():
    return render_template('index.html')


@app.route('/works.html')
def my_works():
    return render_template('works.html')


@app.route('/about.html')
def my_about():
    return render_template('about.html')


@app.route('/contact.html')
def my_contact():
    return render_template('contact.html')

"""
