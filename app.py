import streamlit as st

if not hasattr(st, 'already_started_server'):
    # Hack the fact that Python modules (like st) only load once to
    # keep track of whether this file already ran.
    st.already_started_server = True

    st.write('''
        The first time this script executes it will run forever because it's
        running a Flask server.

        Just close this browser tab and open a new one to see your Streamlit
        app.
    ''')

from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

model_file = open('Model.pkl', 'rb')
model = pickle.load(model_file, encoding='bytes')

@app.route('/')
def index():
    return render_template('index.html', cuaca_esok=' ')

@app.route('/predict', methods=['POST'])
def predict():
    '''
    Predict the insurance cost based on user inputs
    and render the result to the html page
    '''
    TempMin, TempMax, LemAvg, Hujan, SinMth, AnginAvg = [x for x in request.form.values()]

    data = []

    data.append(float(TempMin))
    data.append(float(TempMax))
    data.append(float(LemAvg))
    data.append(float(Hujan))
    data.append(float(SinMth))
    data.append(float(AnginAvg))

    
    prediction = model.predict([data])

    return render_template('index.html', cuaca_esok=prediction[0])


if __name__ == '__main__':
    app.run(debug=True)
