from flask import Flask, render_template, request, redirect, url_for, send_file,abort, Response, send_from_directory, jsonify
import pandas as pd
import os
import uuid
import datetime
# import requests

app = Flask(__name__)

@app.route('/')
def home():
    name = "Prince"
    return render_template('index.html', user_name=name)


@app.route('/file', methods=['POST'])
def file():
    file = request.files['file']

    if file.content_type == 'text/plain':
        content = file.read().decode('utf-8')
        return render_template('file_viewer.html',content = content,ext='txt')
    elif (file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' or
          file.content_type == 'application/vnd.ms-excel'):
        df = pd.read_excel(file)
        content = df.to_html(index=False)
        return render_template('file_viewer.html',content = content,ext='csv')


@app.route('/download/<filename>')
def download(filename):
    _,ext = os.path.splitext(filename)
    today = datetime.datetime.now()
    downloaded_filename = f'result_{today.strftime("%Y-%m-%d_%H:%M:%S")}'
    if ext=='.txt':
        return send_from_directory('downloads', filename, download_name=f'{downloaded_filename}.txt', mimetype='text/plain', as_attachment=True)
    elif ext=='.csv':
        return send_from_directory('downloads', filename, download_name=f'{downloaded_filename}.csv', mimetype='text/csv', as_attachment=True)
    else:
        return abort(400, description="Only Text and CSV files are allowed.")
    # return ext


@app.route('/convert_csv_2', methods=['POST'])
def convert_csv_2():
    file = request.files['file']

    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    if file.content_type == 'text/plain':
        filename = f'{uuid.uuid4()}.txt'
        file_path = os.path.join('downloads', filename)
        file.save(file_path)
        return render_template('download.html', filename=filename)

    elif (file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' or
          file.content_type == 'application/vnd.ms-excel'):
        df = pd.read_excel(file)
        filename = f'{uuid.uuid4()}.csv'
        # if not os.path.exists('downloads'):
        #     os.makedirs('downloads')

        df.to_csv(os.path.join('downloads', filename))
        return render_template('download.html', filename=filename)


@app.route('/handle_post', methods=['POST'])
def handle_post():
    greeting = request.json['greeting']
    name = request.json['name']

    with open('file.txt', 'w') as f:
        f.write(f'{greeting}, {name}')

    return jsonify({'message': 'Successfully written! '})


if __name__ == '__main__':
    app.run(debug=True)
