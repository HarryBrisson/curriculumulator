import json
from datetime import datetime, timedelta

from flask import Flask, request, render_template

from functions.curriculumulator import *



app = Flask(__name__)

@app.route('/')
def home():
    return render_template('menu.html')


@app.route('/ranker')
def ranker():
    
    data = get_curriculumulator_data()

    return render_template('hbars.html',
         data_string = data['data_string'],
         option_list = data['option_list'],
         )


@app.route('/explorer')
def explorer():
    
    data = get_curriculumulator_data()

    return render_template('biplot.html',
         data_string = data['data_string'],
         option_list = data['option_list'],
         )


@app.route('/scorecard')
def scorecard():
    
    subject = request.args.get('subject')

    return f'coming soon: {subject} scorecard'


if __name__ == '__main__':
    app.run(debug=True)



