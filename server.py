from flask import Flask, render_template, url_for, request, redirect
import csv

app = Flask(__name__)


@app.route('/')
def my_home():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == "POST":
        try:
            data = request.form.to_dict()
            # print(data)
            # write_to_file(data)
            write_to_csv(data)
            return redirect('thankyou.html')
        except:
            return 'did not save to database'
    else:
        return 'something went wrong. Try again!'


@app.route('/password_check', methods=['POST', 'GET'])
def submit_form2():
    if request.method == "POST":
        try:
            return redirect('workone.html')
        except:
            return 'did not check against the database'
    else:
        return 'something went wrong with button. Try again!'


def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        file = database.write(f'\n{email}, {subject}, {message}')


def write_to_csv(data):
    with open('database.csv', mode='a', newline='') as database2:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])




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
