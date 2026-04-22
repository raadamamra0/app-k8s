from flask import Flask, request, render_template_string
import psycopg2
import os

app = Flask(__name__)

# Récupération des identifiants via variables d'environnement
ADMIN_USER = os.getenv('APP_USER', 'professeur')
ADMIN_PASS = os.getenv('APP_PASS', 'Reponse2024')

def get_db_connection():
    return psycopg2.connect(
        host='postgres', 
        database='college_db_v2', 
        user='root', 
        password='root'
    )

LOGIN_HTML = """
<div style="text-align:center; margin-top:50px;">

    <img src="/static/logo_m2icollege.png" width="150">

    <h1>Connexion - Gestion du Collège</h1>

    <form method="post">
        Utilisateur: <input type="text" name="username"><br><br>
        Mot de passe: <input type="password" name="password"><br><br>
        <input type="submit" value="Se connecter">
    </form>

</div>
"""
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == ADMIN_USER and request.form['password'] == ADMIN_PASS:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('SELECT e.nom, e.prenom, e.classe, n.matiere, n.note FROM eleves e JOIN notes n ON e.id = n.eleve_id;')
            rows = cur.fetchall()
            cur.close()
            conn.close()
            
            html = "<h1>Tableau des Notes</h1><table border='1'><tr><th>Nom</th><th>Prénom</th><th>Classe</th><th>Matière</th><th>Note</th></tr>"
            for row in rows:
                html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td></tr>"
            html += "</table><br><a href='/'>Déconnexion</a>"
            return html
        else:
            error = 'Identifiants invalides'
    return render_template_string(LOGIN_HTML, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
