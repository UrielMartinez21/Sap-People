from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from database import db
from forms import PersonaForm
from models import Persona

app = Flask(__name__)

# --> Configuracion de la DB
USER_DB = 'postgres'
PASS_DB = 'admin'
URL_DB = 'localhost'
NAME_DB = 'test_db'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

# --> Configuracion de SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --> Inicializacion de SQLAlchemy
db.init_app(app)

# --> Configuracion de flask-migrate
migrate = Migrate()
migrate.init_app(app, db)

# --> Configuracion de flask-wtf
app.config['SECRET_KEY'] = 'llave_secreta'


# ----------------------| RUTAS |---------------------- #
@app.route('/')
@app.route('/index')
@app.route('/index.html')
def inicio():
    # Listado de personas
    personas = Persona.query.order_by(Persona.id).all()
    total_personas = Persona.query.count()
    # Mensajes de debug
    app.logger.debug(f'Listado de personas: {personas}')
    app.logger.debug(f'Cantidad de personas: {total_personas}')
    # Renderizado de la plantilla
    return render_template('index.html', personas=personas, total_personas=total_personas)


@app.route('/ver/<int:id_elemento>')
def ver_detalle(id_elemento):
    # Busqueda de la persona
    persona = Persona.query.get_or_404(id_elemento)

    # Mensaje de debug
    app.logger.debug(f'Ver persona: {persona}')

    # Renderizado de la plantilla
    return render_template('detalle.html', persona=persona)


@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    persona = Persona()
    persona_form = PersonaForm(obj=persona)
    # --> Si se envia el formulario
    if request.method == 'POST':
        # --> Validacion de los datos del formulario
        if persona_form.validate_on_submit():                   # Validar el formulario
            persona_form.populate_obj(persona)                  # Llenar el objeto persona
            app.logger.debug(f'Persona a insertar: {persona}')  # Mensaje de debug
            # --> Se agrega la persona a la DB
            db.session.add(persona)                             # Agregar la persona a la DB
            db.session.commit()                                 # Confirmar la transaccion
            # --> Se redirecciona al inicio
            return redirect(url_for('inicio'))
    return render_template('agregar.html', forma=persona_form)


@app.route('/editar/<int:id_elemento>', methods=['GET', 'POST'])
def editar(id_elemento):
    # --> Busqueda de la persona
    persona = Persona.query.get_or_404(id_elemento)
    persona_form = PersonaForm(obj=persona)
    # --> Si se envia el formulario
    if request.method == 'POST':
        # --> Validacion de los datos del formulario
        if persona_form.validate_on_submit():                   # Validar el formulario
            persona_form.populate_obj(persona)                  # Llenar el objeto persona
            app.logger.debug(f'Persona a editar: {persona}')
            # --> Se agrega la persona a la DB
            db.session.commit()
            # --> Se redirecciona al inicio
            return redirect(url_for('inicio'))
    return render_template('editar.html', forma=persona_form)


@app.route('/eliminar/<int:id_elemento>')
def eliminar(id_elemento):
    # --> Busqueda de la persona
    persona = Persona.query.get_or_404(id_elemento)
    # --> Se elimina la persona de la DB
    db.session.delete(persona)
    db.session.commit()
    # --> Se redirecciona al inicio
    return redirect(url_for('inicio'))


# ----------------------| MAIN |---------------------- #
if __name__ == '__main__':
    app.run()
