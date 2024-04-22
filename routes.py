import re
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')

    if request.method == 'POST':
        inputURL = request.form.get('fullURL')
        serializedURL = re.sub(r'[^\w\s]|[\d]', '', inputURL).lower()
        while len(serializedURL) > 8:
            newStr = ''
            if len(serializedURL) % 2 != 0: serializedURL = serializedURL[:-1]
            for i in range(0, len(serializedURL) - 1, 2):
                try:
                    ascii_int = int((ord(serializedURL[i]) + ord(serializedURL[i + 1])) / 2 )
                    newStr += chr(ascii_int)
                except: pass
            serializedURL = newStr

        with open('urls.txt', 'r+') as f:
            shortids = [webid.strip().split('|')[1] for webid in f.readlines()]
            if serializedURL not in shortids:
                f.write(f'{inputURL}|{serializedURL}\n')

        return render_template('creationsuccess.html', shortid=serializedURL, inputURL=inputURL)

@app.route('/go/<shortid>')
def goto_link(shortid):
    with open('urls.txt', 'r') as f:
        for webid in f.readlines():
            split_url = webid.strip().split('|')
            if shortid == split_url[1]:
                return redirect(split_url[0])
        else:
            return render_template('notfound.html')


@app.route('/directory')
def directory():
    urls = []
    with open('urls.txt', 'r') as f:
        urls = [webid.strip().split('|') for webid in f.readlines()]

    return render_template('directory.html', urls=urls)

if __name__ == '__main__':
    app.run(debug=True)