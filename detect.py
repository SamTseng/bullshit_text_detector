#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import Flask, request
import os, sys, json

from Bullshit import Bullshit
from highlight import Indexing, HighLightFast, HighLightOne, HighLightAll

data_json = 'data.json'
with open(data_json, "r", encoding="utf8") as f:
    TextPatterns = json.loads(f.read())
index = {}
index['F'] = Indexing(TextPatterns['famous'], 5)
index['B'] = Indexing(TextPatterns['bullshit'], 5)

html_head = '<html><head></head><body><center>'
html_end  = '</center></body></html>'

def form_template(value): # input is a dictionary 
# with keys in 'root_type', 'root', 'word', 'version', 'level', 'lesson', 'frequency'
    html = F'''
    <font size=+2><b>偵測唬爛產生器生成的文句</b>
        <form action="/detect" method="GET">
        <input type=textarea name=text high=100 width=100 value="{value}">
        <br><input type="Submit" value="查詢">
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
    text = request.form['text']
    output = ''


    (num_match, Sentences) = HighLightAll(text, TextPatterns, index)

    if len(sys.argv) == 4: # if give an html_file name
        S = []
        for sent in Sentences:
            sent = sent.replace('<F>', '<font color="red">')
            sent = sent.replace('<B>', '<font color="blue">')
            sent = sent.replace('<P>', '<font color="orange">')
            sent = sent.replace('<A>', '<font color="green">')
            sent = re.sub(r'</.>', '</font>', sent)
            S.append(sent)
        with open(sys.argv[3], 'w') as outF:
            outF.write("<html><head></head><body><h2>Highlighted Text:</h2>\n")
            outF.write("<br>\n".join(S))
            outF.write(f"\n<h2>Original Text:</h2>\n{text}\n")
            outF.write('</body></html>')
    else:
        print("\nHighlighted Text:\n" + "".join(Sentences))

    sys.stderr.write("It takes %2.4f seconds for %d matches in %d sentences.\n" 
        % ((time.time() - time1), num_match, len(Sentences)))
    

    return html_head + form_template(text) + output + html_end



'''
主程式區域
'''
if __name__ == "__main__":
    if sys.argv[1] == 'cmd': # run under command line to generate text
        topic = input("請輸入主題: ")
        min_length = int( input("請輸入最少字數: ").strip() )
        obj = Bullshit()
        print( obj.generate(topic, min_length) )
    else: # run in the browser to detect generated text
        print('[伺服器開始運行]')
        # 取得遠端環境使用的連接端口，若是在本機端測試則預設開啟於port=5005
        port = int(os.environ.get('PORT', 5005))
        print(f'[Flask運行於連接端口:{port}]')
        # 本機測試使用127.0.0.1, debug=True; Heroku部署使用 0.0.0.0
        app.run(host='localhost', port=port, debug=True)


'''
python run.py cmd
'''
