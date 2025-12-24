from flask import Flask, request
import mysql.connector
app = Flask(__name__)
@app.route('/guardar', methods=['POST'])
def guardar():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='skate_revistas'
    )
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO preferencias (nombre, email, revista, comentario, fecha) VALUES (%s, %s, %s, %s, NOW())",
        (request.form['nombre'], request.form['email'], request.form['revista'], request.form['comentario'])
    )
    conn.commit()
    conn.close()
    return '''
        <script>
            alert("¡Tu voto fue guardado exitosamente!");
            window.location.href = document.referrer;
        </script>
    '''
@app.route('/ver')
def ver():
    conn = mysql.connector.connect(host='localhost', user='root', password='', database='skate_revistas')
    cursor = conn.cursor()
    cursor.execute("SELECT revista, COUNT(*) FROM preferencias GROUP BY revista")
    datos = cursor.fetchall()
    conn.close()
    html = '<h2>Resultados:</h2>'
    for revista, votos in datos:
        html += f'<p>{revista}: {votos} votos</p>'
    return html + '<a href="/">Volver</a>'
@app.route('/')
def inicio():
    return '<h1>Funciona ✓</h1><a href="/ver">Ver resultados</a>'

app.run(debug=True, port=5000)