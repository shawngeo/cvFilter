from flask import Flask, request, render_template
from flaskext.mysql import MySQL
import pandas as pd
from sqlalchemy import create_engine, sql


def format_url(url):
    if url.startswith('http') or url.startswith('https'):
        return f'<a href="{url}">{url}</a>'
    else:
        return url


conn = create_engine("mysql+mysqlconnector://root:mummyPAPPA1@127.0.0.1:3306/cvs")

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mummyPAPPA1'
app.config['MYSQL_DATABASE_DB'] = 'cvs'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)


@app.route('/')
def my_form():
    return render_template('demo.html')


@app.route('/', methods=['POST'])
def authenticate():
    if request.method == 'POST':
        year = request.form['y']
        area = request.form['area-names']
        project = request.form['Project-name']
        branch = request.form['Branch-name']
        skills = request.form['Skills-name']

        query = "select * from resume where 1=1"
        if year != '':
            query += " and yoe >= {}".format(year)
        if area != '':
            query += " and summary like '%{}%'".format(area)
        if project != '':
            query += " and summary like '%{}%'".format(project)
        if branch != '':
            query += " and designation like '%{}%'".format(branch)
        if skills != '':
            query += " and skills like '%{}%'".format(skills)

        sql_query = sql.text(query)
        with conn.connect() as mysql_conn:
            df = pd.read_sql(sql_query, mysql_conn)
        if df.empty:
            return render_template('norec.html')

        df['CVLink'] = df['CVLink'].apply(format_url)

        html_table = df.to_html(index=False, classes='table table-striped', border=1, justify='left', escape=False)
        html_table = html_table.replace('<table', '<table style="border-collapse: collapse; \
                                         width: 100%; margin: 0 auto; text-align: left; \
                                         font-family: Arial, Helvetica, sans-serif; \
                                         font-size: 12px; line-height: 1.4;"')
        html_table = html_table.replace('<thead>', '<thead style="background-color: #0077b6; \
                                         border-top: 1px solid #dee2e6; \
                                         border-bottom: 2px solid #dee2e6;">')
        html_table = html_table.replace('<th ', '<th style="padding: 18px; \
                                         font-weight: bold; text-align: left; \
                                         color: #ffffff; border-right: 1px solid #dee2e6; \
                                         background-color: #a0c8d6;" ')
        html_table = html_table.replace('<td ', '<td style="padding: 8px; \
                                         border-right: 1px solid #dee2e6; \
                                         background-color: #C8DCF2;" ')
        html_table = html_table.replace('<tbody>', '<tbody>')
        html_table = html_table.replace('<tr>', '<tr style="background-color: #C8DCF2;">')
        return html_table


if __name__ == '__main__':
    app.debug = True
    app.run()


