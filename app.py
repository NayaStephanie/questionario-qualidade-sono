from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

app.static_folder = 'static'

# Inicializa o banco de dados
def init_db():
    conn = sqlite3.connect('psqi-form.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            birthdate DATE,
            bedtime TEXT,
            sleep_latency INTEGER,
            wake_time TEXT,
            sleep_duration INTEGER,
            q5a INTEGER,
            q5b INTEGER,
            q5c INTEGER,
            q5d INTEGER,
            q5e INTEGER,
            q5f INTEGER,
            q5g INTEGER,
            q5h INTEGER,
            q5i INTEGER,
            q5j INTEGER,
            q6 INTEGER,
            q7 INTEGER,
            q8 INTEGER,
            q9 INTEGER,
            q10 INTEGER,
            global_score INTEGER,
            component1 INTEGER,
            component2 INTEGER,
            component3 INTEGER,
            component4 INTEGER,
            component5 INTEGER,
            component6 INTEGER,
            component7 INTEGER,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
       )
    ''')
    conn.commit()
    conn.close()

# Função para calcular a pontuação do PSQI
def calculate_psqi_score(response):
    component1 = int(response['q6'])
    
    # Cálculo dos outros componentes
    if response['sleep_latency'] <= 15:
        component2 = 0
    elif 16 <= response['sleep_latency'] <= 30:
        component2 = 1
    elif 31 <= response['sleep_latency'] <= 60:
        component2 = 2
    else:
        component2 = 3
    
    if response['sleep_duration'] >= 7:
        component3 = 0
    elif 6 <= response['sleep_duration'] < 7:
        component3 = 1
    elif 5 <= response['sleep_duration'] < 6:
        component3 = 2
    else:
        component3 = 3

    bedtime_hours = int(response['bedtime'].split(':')[0])
    wake_hours = int(response['wake_time'].split(':')[0])
    total_bedtime = (wake_hours - bedtime_hours) * 60
    sleep_duration = response['sleep_duration'] * 60
    sleep_efficiency = (sleep_duration / total_bedtime) * 100 if total_bedtime > 0 else 0

    if sleep_efficiency >= 85:
        component4 = 0
    elif 75 <= sleep_efficiency < 85:
        component4 = 1
    elif 65 <= sleep_efficiency < 75:
        component4 = 2
    else:
        component4 = 3

    component5 = int(response['q5a']) + int(response['q5b']) +  int(response['q5c']) +  int(response['q5d']) +  int(response['q5e']) +  int(response['q5f']) +  int(response['q5g']) +  int(response['q5h']) +  int(response['q5i']) +  int(response['q5j'])
    component6 = int(response['q7'])
    component7 = int(response['q8']) + int(response['q9'])

    global_score = component1 + component2 + component3 + component4 + component5 + component6 + component7

    return {
        'component1': component1,
        'component2': component2,
        'component3': component3,
        'component4': component4,
        'component5': component5,
        'component6': component6,
        'component7': component7,
        'global_score': global_score
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    response = {
        'bedtime': request.form['bedtime'],
        'sleep_latency': int(request.form['sleep-latency']),
        'wake_time': request.form['wake-time'],
        'sleep_duration': int(request.form['sleep-duration']),
        'q5a': int(request.form['q5a']),
        'q5b': int(request.form['q5b']),
        'q5c': int(request.form['q5c']),
        'q5d': int(request.form['q5d']),
        'q5e': int(request.form['q5e']),
        'q5f': int(request.form['q5f']),
        'q5g': int(request.form['q5g']),
        'q5h': int(request.form['q5h']),
        'q5i': int(request.form['q5i']),
        'q5j': int(request.form['q5j']),
        'q6': int(request.form['q6']),
        'q7': int(request.form['q7']),
        'q8': int(request.form['q8']),
        'q9': int(request.form['q9']),
        'q10': int(request.form['q10'])
    }

    score = calculate_psqi_score(response)
    session['score'] = score

    # Salvar a resposta no banco de dados
    conn = sqlite3.connect('psqi-form.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO responses 
        (bedtime, sleep_latency, wake_time, sleep_duration, q5a, q5b, q5c, q5d, q5e, q5f, q5g, q5h, q5i, q5j, q6, q7, q8, q9, q10, global_score, component1, component2, component3, component4, component5, component6, component7)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (response['bedtime'], response['sleep_latency'], response['wake_time'], response['sleep_duration'], response['q5a'], response['q5b'], response['q5c'], response['q5d'], response['q5e'], response['q5f'], response['q5g'], response['q5h'], response['q5i'], response['q5j'], response['q6'], response['q7'], response['q8'], response['q9'], response['q10'], score['global_score'], score['component1'], score['component2'], score['component3'], score['component4'], score['component5'], score['component6'], score['component7']))
    conn.commit()
    conn.close()

    return redirect(url_for('results'))

@app.route('/results')
def results():
    score = session.get('score', None)
    if score is None:
        return redirect(url_for('index'))
    return render_template('results.html', score=score)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

