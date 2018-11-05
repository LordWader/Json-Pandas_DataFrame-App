import pandas as pd
from flask import Flask, render_template, send_file
from flask import request
import hashlib
import bencode

 
app = Flask(__name__, static_url_path='')
data = pd.read_json('text.json')

@app.route('/getfile/<name>')
def get_output_file(name):
    return send_file(name, as_attachment=True)

@app.route('/f', methods=['POST'])
def f():   
    b = request.form['dzen']
    if b == '1':
        if request.form['A'].upper() == 'ALL':
            A = [i for i in range(1, 45)]
        else:
            A = list(map(int, request.form['A'].split(',')))
        df = pd.DataFrame(data[A])
        excel_writer = pd.ExcelWriter('output_1.xlsx')
        df.to_excel(excel_writer, sheet_name="sheet1")
        df.to_csv('csv_1.csv', encoding='utf-8', index=False)
        excel_writer.save()
        return data[A].to_html() +  """
                                    <html>
                                       <head>
                                          <meta charset="utf-8">
                                          <title>Result for the first option</title>
                                       </head>
                                       <body>
                                         <p><a href=/getfile/output_1.xlsx>Скачать файл в xlsx формате</a>
                                         <a href=/getfile/csv_1.csv>Скачать файл в csv формате</a>
                                       </body>
                                    </html>
                                    """
    elif b == '2':
        A = map(int, request.form['A'])
        results = [[0 for i in range(44)] for j in range(44)]
        for i in range(1, 45):
            if data[i][0] != 0 and data[i][0] != 'EMPTY':
                results[i-1][i-1] = 1
            else:
                results[i-1][i-1] = 0
        df = pd.DataFrame(results)
        excel_writer = pd.ExcelWriter('output_2.xlsx')
        df.to_excel(excel_writer, sheet_name="sheet1")
        df.to_csv('csv_2.csv', encoding='utf-8', index=False)
        excel_writer.save()
        return df.to_html() + """
                              <html>
                                 <head>
                                    <meta charset="utf-8">
                                    <title>Results for the second option</title>
                                 </head>
                                 <body>
                                    <p><a href=/getfile/output_2.xlsx>Скачать файл в xlsx формате</a>
                                    <a href=/getfile/csv_2.csv>Скачать файл в csv формате</a>
                                 </body>
                               </html>
                               """
    elif b == '3':
        A = list(request.form['A'].split(','))
        if len(A) == 1:
            return str(','.join(data[i][int(A[0])] for i in range(1, 45)))
        symb = A[1]    
        return str(symb.join(data[i][int(A[0])] for i in range(1, 45)))
    else:
        if request.form['A'].upper() == 'ALL':
            A = [i for i in range(452)]
        else:
            A = list(map(int, request.form['A'].split(',')))
        answer = [0]*len(A)
        for i in range(len(A)):
            result = []
            for j in range(1, 45):
                result.append(data[j][A[i]])
            answer[i] = hashlib.md5(bencode.bencode(result)).hexdigest()
        df = pd.DataFrame(answer)
        excel_writer = pd.ExcelWriter('output_4.xlsx')
        df.to_excel(excel_writer, sheet_name="sheet1")
        df.to_csv('csv_4.csv', encoding='utf-8', index=False)
        excel_writer.save()
        return df.to_html() + """
                              <html>
                                 <head>
                                    <meta charset="utf-8">
                                    <title>Results for the second option</title>
                                 </head>
                                 <body>
                                   <p><a href=/getfile/output_4.xlsx>Скачать файл в xlsx формате</a>
                                      <a href=/getfile/csv_4.csv>Скачать файл в csv формате</a>
                                 </body>
                               </html>
                               """

@app.route('/')
def f0():
    return render_template('index.html')
 
if __name__ == '__main__':
    app.run(debug=True)
