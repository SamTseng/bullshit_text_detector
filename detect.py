#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re, os, sys, json, time
from flask import Flask, request

from Bullshit import Bullshit
from highlight import Indexing, HighLightAll, HighLightFast, HighLightOne

data_json = 'data.json'
with open(data_json, "r", encoding="utf8") as f:
    TextPatterns = json.loads(f.read())
index = {}
index['F'] = Indexing(TextPatterns['famous'], 5)
index['B'] = Indexing(TextPatterns['bullshit'], 5)

html_head = '<html><head></head><body><center>'
html_end  = '</center></body></html>'

def form_template(value): 
    html = F'''
    <font size=+2><b>偵測唬爛產生器生成的文句</b>
        <form action="/detect" method="POST">
        <textarea name=text rows=10 cols=100 autofocus>
{value}
        </textarea>
        <br><input type="Submit" value="偵測">
        </form><hr>
    </font>
    '''
    return html


app = Flask(__name__)
@app.route("/")
def main():
    return html_head + form_template('') + html_end

@app.route('/detect', methods=['POST'])
def detect():
    time1 = time.time()
    text = request.form['text']
    (num_match, Sentences) = HighLightAll(text, TextPatterns, index)
    S = []
    for sent in Sentences:
        sent = sent.replace('<F>', '<font color="red">')
        sent = sent.replace('<B>', '<font color="blue">')
        sent = sent.replace('<P>', '<font color="orange">')
        sent = sent.replace('<A>', '<font color="green">')
        sent = re.sub(r'</.>', '</font>', sent)
        S.append(sent)
    output = ("It takes %2.4f seconds to detect %d matches in %d sentences.<hr>\n" 
        % ((time.time() - time1), num_match, len(Sentences)))
    output += "<table width=75%><tr><td>" + "<br>\n".join(S) + "</td></tr></table>"
    return html_head + form_template(text) + output + html_end


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'cmd': # run under command line to generate text
        topic = input("請輸入主題: ")
        min_length = int( input("請輸入最少字數: ").strip() )
        obj = Bullshit()
        print( obj.generate(topic, min_length) )
    else: # run in the browser to detect generated text
        print('[伺服器開始運行]')
        # 取得遠端環境使用的連接端口，若是在本機端測試則預設開啟於port=5005
        port = int(os.environ.get('PORT', 5005))
        # 本機測試使用127.0.0.1, debug=True; Heroku部署使用 0.0.0.0
        app.run(host='localhost', port=port, debug=True)


'''
# To detect text generated by bullshit_generator, run
python detect.py

# To generate text, run:
python detect.py cmd
'''
