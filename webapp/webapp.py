from flask import Flask, render_template, url_for, request
import os
import io
import base64


import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] ='super-secret-key'

site_path = os.path.realpath(os.path.dirname(__file__))
csv_url = os.path.join(site_path, "static\data", "data.csv")

df = pd.read_csv('static/data/data.csv')

states_list = df.STATE.unique()
states_list = states_list.tolist()
data = {}

@app.route('/')
def display_home():
    global data
    return render_template('display_plot.html', data = data)

@app.route('/selected_option', methods=["POST"])
def selected_option():
    data['state'] = request.form['state']
    data['const'] = request.form['const']
    data['party'] = request.form['party']

    years = df[(df['STATE'] == data['state']) & (df['CONSTITUENCY'] == data['const']) & (df['PARTY'] == data['party'])]['YEAR'].tolist()
    unique_years = df[df['STATE'] == data['state']]['YEAR'].unique().tolist()

    l = []
    for i in unique_years:
        if i in years:
            l.append(1)
        else:
            l.append(0)

    plot_url = build_graph(unique_years,l)
    return render_template('display_plot.html', data = data, plot = plot_url, years = years, unique_years = unique_years)

def build_graph(x, y):
    img = io.BytesIO()
    plt.plot(x, y)
    plt.savefig(img, format='png')
    img.seek(5)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(graph_url)

if __name__ == '__main__':
    app.run(debug = True)
