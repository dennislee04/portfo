from flask import Flask, render_template, url_for, request, redirect, send_file
import csv
import requests
import hashlib
import smtplib
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pylab import savefig
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime
from email.message import EmailMessage
from openpyxl import load_workbook
# workon my-virtualenv (to install libraries to & work on my virtual environment on Python Anywhere)

app = Flask(__name__)


@app.route('/')
def my_home():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    # write_type_to_file(page_name, type(page_name))
    if page_name == "Baseball.html":
        create_csv_to_html(page_name)
        return render_template(page_name)
    elif (page_name == "worktwo.html") or (page_name == "workthree.html"):
        # data = read_csv_file('./portfo/data_files/Baseball.csv')
        firstFive = first_five_data_row_csv('./portfo/data_files/Baseball.csv')
        rowOne = read_csv_row_one_csv('./portfo/data_files/Baseball.csv')
        columnOne = read_csv_column_one_csv('./portfo/data_files/Baseball.csv')
        return render_template(page_name, tables=[firstFive.to_html()], titles=[''], rowOne=rowOne, columnOne=columnOne)
    else:
        return render_template(page_name)


# This is for submitting the contact form
@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == "POST":
        try:
            data = request.form.to_dict()
            # print(data)
            write_to_file(data)
            write_to_csv(data)
            send_email(data)
            return redirect('thankyou.html')
        except:
            return 'did not save to database'
    else:
        return 'something went wrong. Try again!'


@app.route('/submit_formula', methods=['POST', 'GET'])
def submit_formula():
    if request.method == "POST":
        try:
            page_name = request.form.get('htmlForm')
            basic = request.form.get('basicStat')
            team = request.form.get('columnOneData')
            rowoneData = request.form.get('rowOneData')
            if page_name == "worktwo.html":
                firstFive = first_five_data_row_csv('./portfo/data_files/Baseball.csv')
                rowOne = read_csv_row_one_csv('./portfo/data_files/Baseball.csv')
                columnOne = read_csv_column_one_csv('./portfo/data_files/Baseball.csv')
                df = pd.read_csv("./portfo/data_files/Baseball.csv")
                if basic == "Mean":
                    if team == "All":
                        formulaUsed = f'df.loc[:, \"{rowoneData}\"].mean()'
                        altformula = f'df.{rowoneData}.mean()'
                        results = df.loc[:, rowoneData].mean()
                    else:
                        formulaUsed = f'df.loc[df.Team == \"{team}\", \"{rowoneData}\"].mean()'
                        altformula = f'df.loc[df.Team == \"{team}\"].{rowoneData}.mean()'
                        results = df.loc[(df.Team == team, rowoneData)].mean()
                elif basic == "Medium":
                    if team == "All":
                        formulaUsed = f'df.loc[:, \"{rowoneData}\"].median()'
                        altformula = f'df.{rowoneData}.median()'
                        results = df.loc[:, rowoneData].median()
                    else:
                        formulaUsed = f'df.loc[df.Team == \"{team}\", \"{rowoneData}\"].median()'
                        altformula = f'df.loc[df.Team == \"{team}\"].{rowoneData}.median()'
                        results = df.loc[(df.Team == team, rowoneData)].median()
                elif basic == "Mode":
                    if team == "All":
                        formulaUsed = f'df.loc[:, \"{rowoneData}\"].mode()'
                        altformula = f'df.{rowoneData}.mode()'
                        results = df.loc[:, rowoneData].mode()
                    else:
                        formulaUsed = f'df.loc[df.Team == \"{team}\", \"{rowoneData}\"].mode()'
                        altformula = f'df.loc[df.Team == \"{team}\"].{rowoneData}.mode()'
                        results = df.loc[(df.Team == team, rowoneData)].mode()
                elif basic == "StanDev":
                    if team == "All":
                        formulaUsed = f'df.loc[:, \"{rowoneData}\"].std()'
                        altformula = f'df.{rowoneData}.std()'
                        results = df.loc[:, rowoneData].std()
                    else:
                        formulaUsed = f'df.loc[df.Team == \"{team}\", \"{rowoneData}\"].std()'
                        altformula = f'df.loc[df.Team == \"{team}\"].{rowoneData}.std()'
                        results = df.loc[(df.Team == team, rowoneData)].std()
                else:
                    formulaUsed = "No formula was used"
                    results = "No Results"
                return render_template(page_name, tables=[firstFive.to_html()], titles=[''], rowOne=rowOne, columnOne=columnOne, formulaUsed="Formula Used:" + formulaUsed, altformula="Alternative Formula:"+altformula, formulaChoosen=basic, results=results)
            else:
                return (str(page_name) + " Not Found")
        except RuntimeError as rte:
            return {rte}
        except TypeError as te:
            return {te}
        except NameError as ne:
            return {ne}
        #except:
            #return 'formula did not work'
    else:
        return 'something went wrong with the formula. Try again!'


@app.route('/submit_correlation', methods=['POST', 'GET'])
def submit_correlation():
    if request.method == "POST":
        try:
            page_name = request.form.get('htmlForm')
            category_one = request.form.get('category_one')
            category_two = request.form.get('category_two')
            category_three = request.form.get('category_three')
            #return category_three
            if page_name == "workthree.html":
                firstFive = first_five_data_row_csv('./portfo/data_files/Baseball.csv')
                rowOne = read_csv_row_one_csv('./portfo/data_files/Baseball.csv')
                columnOne = read_csv_column_one_csv('./portfo/data_files/Baseball.csv')
                df = pd.read_csv("./portfo/data_files/Baseball.csv")

                formulaUsed = f'df[[{category_one}, {category_two}, {category_three}]]'
                formulaUsedTwo = f'df_correlation.corr()'
                df_correlation = df[[category_one, category_two, category_three]]
                resultsOne = df_correlation.corr()
                resultsTwo = "Place holder for results Two"

                # fig, ax = plt.subplots(figsize=(6,6))
                # ax = sns.set_style(style="darkgrid")
                # x = [i for i in range(100)]
                # y = [i for i in range(100)]

                formulaUsedThree = f"sns.heatmap(data = df_correlation.corr(), annot = True, fmt = '.2g', center = 0, cmap = 'coolwarm', linewidth = 1, linecolor = 'black')"
                # resultsThree = sns.heatmap(resultsOne, annot = True, fmt = '.2g', center = 0, cmap = 'coolwarm', linewidth = 1, linecolor = 'black')
                # sns.heatmap(resultsOne, annot = True, fmt = '.2g', center = 0, cmap = 'coolwarm', linewidth = 1, linecolor = 'black')
                # canvas = FigureCanvas(fig)
                # fig.savefig(os.path.join('static', 'assets/plots/heatmap.png'), dpi=75)
                resultsThree = "Plase Holder for Results Three"


                return render_template(page_name, tables=[firstFive.to_html()], titles=[''], rowOne=rowOne, columnOne=columnOne, formulaUsed="First Formula Used:"+formulaUsed, formulaUsedTwo="Second Formula Used:"+formulaUsedTwo, formulaUsedThree="Third Formula Used:"+formulaUsedThree, resultsOne=[resultsOne.to_html()], resultsTwo=resultsTwo, resultsThree=restulsThree)
            else:
                return (str(page_name) + " Not Found")
        except RuntimeError as rte:
            return {rte}
        except TypeError as te:
            return {te}
        except NameError as ne:
            return {ne}
        #except:
    else:
        return 'something went wrong with the Correlation Formula. Try again!'


# this is for routing files & allowing users to download files from the server
@app.route('/downloads/<id>')
def downloads(id):
    if id == 'Baseball.csv':
        path = './data_files/Baseball.csv'
    else:
        return 'something went wrong with the download. Try again!'
    # write_type_to_file(os.getcwd(), type(os.getcwd()))
    # write_type_to_file(path, type(path))
    return send_file(path, as_attachment=True)


# This function will read the inputed csv file & return the first column, from the server
def read_csv_column_one_csv(file):
    data = read_csv_file(file)
    return data.iloc[:, 0]


# This function will read the inputed csv file & return the first row, from the server
def read_csv_row_one_csv(file):
    data = pd.read_csv(file)
    return data.head(1)


# This function will read the inputed csv file & return the first 6 rows, from the server
def first_five_data_row_csv(file):
    data = pd.read_csv(file)
    return data.head(6)


# This function will read the inputed csv file, from the server
def read_csv_file(file):
    data = pd.read_csv(file)
    return data


# This function is used to help be diagnose issues, by writing the variable & its' type to a file
def write_type_to_file(pagename, pagename_type):
    with open('type.txt', mode='a') as database0:
        # os.getcwd()
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        filetype = database0.write(f'\n{pagename}, {pagename_type}, {dt_string}')


# This will read an existing CSV file from the server & will create an html file of the data to display
def create_csv_to_html(file):
    filename = file.replace("html", "csv")
    loadfile = pd.read_csv("./portfo/data_files/" + filename)
    html_file = loadfile.to_html("./portfo/templates/file")


# This will write the user's contact information to the database.txt file
def write_to_file(data):
    with open('./portfo/data_files/database.txt', mode='a') as database:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        file = database.write(f'\n{email}, {subject}, {message}')


# This will write the user's contact information to the database.csv file
def write_to_csv(data):
    with open('./portfo/data_files/database.csv', mode='a', newline='') as database2:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])


# This will send an email to myself, the inputed user's email address, with the sender as me (leedennis04@gmail.com)
# Using a Gmail API: https://console.cloud.google.com/apis/api/gmail.googleapis.com/
# That I had created under my gmail account
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
                return render_template('workone.html', data=f"Your password \'{pwd}\' was FOUND: {count} times. You should change your password!")
            else:
                 # return render_template('workone.html', data=f"Your password: \'{pwd[0]}\' was NOT FOUND. Carry on!")
                return render_template('workone.html', data=f"Your password \'{pwd}\' was NOT FOUND. Carry on!")
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
