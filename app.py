from flask import Flask, render_template, request, redirect, url_for, flash

#create Flask app
app = Flask(__name__)
app.secret_key = "supersecretkay" #needed for flash messages

#1 Home page route
@app.route('/')
def home():
    return render_template('index.html')

#2 Booking page route
@app.route('/booking')
def booking():
    return render_template('booking.html')

#3 Handle booking form sbmissions
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    service = request.form['service']
    date = request.form['date']

    with open('booking.csv', 'a') as f:
        f.write(f"{name},{email},{service},{date}\n")

    flash(f"Booking confirmed for {name} on {date} for a {service}. We'll email you at {email}.")
    return redirect(url_for('booking'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

