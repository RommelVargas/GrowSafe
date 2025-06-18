from flask import Flask, render_template, redirect, url_for, request, send_from_directory, flash
from flask_sqlalchemy import SQLAlchemy
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__, template_folder='templates')
app.secret_key = 'supersecretkey'

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    contrasena = db.Column(db.String(150), nullable=False)

# Modelo de resultado
class Resultado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_planta = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.String(500), nullable=False)
    resultado = db.Column(db.String(500), nullable=False)

# Configuración del correo electrónico
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

def enviar_correo(asunto, mensaje):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg['Subject'] = asunto

    msg.attach(MIMEText(mensaje, 'plain', 'utf-8'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        try:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        except smtplib.SMTPAuthenticationError:
            flash('Error de autenticación SMTP. Verifica tus credenciales de correo electrónico.', 'error')
        except smtplib.SMTPResponseException as e:
            flash(f'Error SMTP: {e.smtp_code} - {e.smtp_error}', 'error')

# Ruta principal redirige a la página de inicio de sesión
@app.route('/')
def inicio():
    return redirect(url_for('iniciar_sesion'))

# Ruta para la página de inicio de sesión
@app.route('/iniciar_sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        # Aquí puedes agregar la lógica para manejar el inicio de sesión
        recordar = request.form.get('recordar')
        if recordar:
            # Lógica para recordar al usuario
            pass
        try:
            enviar_correo('Inicio de sesión', 'Un usuario ha iniciado sesión.')

        except Exception as e:
            flash(f'Error al enviar el correo: {str(e)}', 'error')
        return redirect(url_for('index'))
    return render_template('login.html')

# Ruta para la página de registro
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        usuario = request.form.get('user')
        email = request.form.get('email')
        contrasena = request.form.get('pass')
        if not usuario or not email or not contrasena:
            flash('Todos los campos son obligatorios', 'error')
            return redirect(url_for('registro'))
        nuevo_usuario = Usuario(usuario=usuario, email=email, contrasena=contrasena)
        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            try:
                enviar_correo('Nuevo registro', 'Un nuevo usuario se ha registrado.')
            except Exception as e:
                flash(f'Error al enviar el correo: {str(e)}', 'error')
            return redirect(url_for('iniciar_sesion'))
        except Exception as e:
            db.session.rollback()
            flash('Error al registrar el usuario: ' + str(e), 'error')
            return redirect(url_for('registro'))
    return render_template('register.html')

# Ruta para la página de inicio
@app.route('/index')
def index():
    return render_template('index.html')

# Ruta para la página de analizar
@app.route('/analizar', methods=['GET', 'POST'])
def analizar():
    if request.method == 'POST':
        nombre_planta = request.form.get('nombre_planta')
        descripcion = request.form.get('descripcion')
        imagen = request.files.get('imagen')
        
        # Aquí puedes agregar la lógica para analizar la imagen y generar un resultado
        resultado_texto = f"Análisis de la planta {nombre_planta}: {descripcion}. (Resultado simulado)"
        
        # Guardar el resultado en la base de datos
        nuevo_resultado = Resultado(nombre_planta=nombre_planta, descripcion=descripcion, resultado=resultado_texto)
        db.session.add(nuevo_resultado)
        db.session.commit()
        
        return render_template('analizar.html', resultado=resultado_texto)
    return render_template('analizar.html')

# Ruta para la página de resultados
@app.route('/resultados')
def resultados():
    return render_template('resultados.html')

# Ruta para la página de guía
@app.route('/guia')
def guia():
    return render_template('guia.html')

# Ruta para la página de contacto
@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        mensaje = request.form.get('mensaje')
        # Aquí puedes agregar la lógica para manejar el mensaje de contacto
        flash('Mensaje enviado correctamente', 'success')
        return redirect(url_for('contacto'))
    return render_template('contacto.html')

# Ruta para la página de mi cuenta
@app.route('/mi_cuenta')
def mi_cuenta():
    return render_template('mi_cuenta.html')

# Ruta para la página de olvidaste tu contraseña
@app.route('/olvidaste_contrasena', methods=['GET', 'POST'])
def olvidaste_contrasena():
    if request.method == 'POST':
        # Aquí puedes agregar la lógica para manejar el cambio de contraseña
        try:
            enviar_correo('Cambio de contraseña', 'Un usuario ha solicitado cambiar su contraseña.')
        except Exception as e:
            flash(f'Error al enviar el correo: {str(e)}', 'error')
        return redirect(url_for('iniciar_sesion'))
    return render_template('forgot_password.html')

# Ruta para servir archivos estáticos
@app.route('/static/<path:filename>')
def archivos_estaticos(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


@app.route('/analizar_suelo', methods=['POST'])
def analizar_suelo():
    # Procesar imagen y datos de suelo (IA)
    pass