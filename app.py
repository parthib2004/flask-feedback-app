from flask import Flask, render_template, request
from flask_pymongo import PyMongo

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['MONGO_URI'] = 'mongodb://host.docker.internal:27017/mercedes'
else:
    app.debug = False
    app.config['MONGO_URI'] = 'mongodb://host.docker.internal:27017/mercedes'

mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        
        if customer == '' or dealer == '':
            return render_template('index.html', message='Please enter required fields')
        
        # Check if feedback already exists
        existing_feedback = mongo.db.feedback.find_one({'customer': customer})
        if existing_feedback is None:
            # Insert new feedback
            mongo.db.feedback.insert_one({
                'customer': customer,
                'dealer': dealer,
                'rating': rating,
                'comments': comments
            })
            return render_template('success.html')
        
        return render_template('index.html', message='You have already submitted feedback')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)