#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, url_for, session, render_template, Response, request, flash, redirect, abort, jsonify
from flaskext.mysql import MySQL
import json
import time


mysql = MySQL()

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('IROOM_SETTINGS', silent=True)
mysql.init_app(app)
type_sensor = ['temperature', 'humidity', 'light',
               'sound', 'motion', 'red', 'green', 'blue']
last_value = [0, 0, 0, 0, 0, 0, 0, 0]


def event_sensor():
    code = 0
    while True:
        conn = mysql.connect()
        cursor = conn.cursor()
        sensor = type_sensor[code]

        cursor.execute(
            f"""SELECT valor FROM sensors WHERE nombre='{sensor}' order by time desc""")
        value = int(cursor.fetchone()[0])
        if value != last_value[code]:
            sensor = {"tipo": sensor, "valor": value}
            data_json = json.dumps(sensor)
            print(sensor)
            yield 'data: %s\n\n' % str(data_json)
            last_value[code] = value
            # flash(f'Actualizado sensor de {sensor}')
        if code >= 7:
            code = 0
            """ Si no hago la pausa la BBDD me echa """
            time.sleep(1)
        else:
            code += 1


@app.route('/update_sensor')
def sse_request():
    return Response(event_sensor(), mimetype='text/event-stream')


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/sensors')
def sensors():
    return render_template('sensors.html')


@app.route('/sensorsChart')
def sensorsChart():
    return render_template('sensorsChart.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('Has entrado en la sesion')
            return redirect(url_for('sensors'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Has salido de la sesion')
    return redirect(url_for('main'))


@app.route('/iluminacion')
def iluminacion():
    return render_template('iluminacion.html')


@app.route('/setcolor', methods=['GET'])
def setcolor():
    """
            PARTE 3: INSERTE AQUI EL CÓDIGO PARA GUARDAR EL COLOR DE LA BASE DE DATOS
            CUANDO SE RECIBE DESDE EL CLIENTE POR AJAX
    """
    success = True
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        color = request.args.get('color')
        red = int('0x' + color[1:3], 16)
        green = int('0x' + color[3:5], 16)
        blue = int('0x' + color[5:7], 16)
        colors = {'red': red, 'green': green, 'blue': blue}
        for code in colors:
            cursor.execute(
                """INSERT INTO sensors(nombre, valor) values(%s, %s)""", (code, colors[code]))
            conn.commit()
    except ValueError:
        success = False
        print("Something went wrong")
    finally:
        return jsonify(success)


if __name__ == '__main__':
    with app.test_request_context():
        app.debug = True
        app.run(host='0.0.0.0')
