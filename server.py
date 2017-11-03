#!/home/brian/Envs/env1/bin/python3.5

from flask import Flask,request, url_for
from flask_bootstrap import Bootstrap
from flask import render_template,redirect
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from flask_login import LoginManager, login_user, login_required, logout_user
from formularios import *
from AdminDB import *
from validar import ValidationException
import csv

class User():
    def __init__(self, name, password,active =False):
        self.name = name
        self.password = password
        self.active = active

    def __repr__(self):
        return '<User %r>' % self.name
    def is_authenticated(self):
        return True
    def is_active(self):
        return self.active
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.name)

class UserRepository():
    def __init__(self,path=''):
        self.filePath=path
    def authenticate_user(self,name,password):
        with open(self.filePath,'r') as usersFile:
            user = None
            for line in usersFile:
                line_list= line.split(",")
                str_user=line_list[0].strip()
                str_pass=line_list[1].strip()
                str_active=line_list[2].strip()
                bool_active=str_active=='1'

                if (name == str_user):
                    if (password== str_pass):
                        user=User(name,password,bool_active)
        return user
    def getUser(self,name):
        with open(self.filePath,'r') as usersFile:
            user = None
            for line in usersFile:
                line_list= line.split(",")
                str_user=line_list[0].strip()
                str_pass=line_list[1].strip()
                str_active=line_list[2].strip()
                bool_active=str_active=='1'
                
                if (name == str_user):
                    user=User(name,str_pass,bool_active)
        return user

              
   
app= Flask(__name__)
app.config['SECRET_KEY'] = 'UN STRING MUY DIFICIL'
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
boot = Bootstrap(app)
login_manager=LoginManager()
login_manager.init_app(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
    
@app.route('/lista',methods=['GET'])
@login_required
def listarCsv():
    try:
        admin = AdminDB('archivo.csv')
        archivo = admin.dame_list_archivo()
        return render_template('lista.html',model=archivo)
    except ValidationException as e:
        return render_template('customError.html', mensaje=e.message )
    
@app.route('/AgregarVenta',methods=['GET'])
@login_required
def agregarVGet():
    form = FormularioNuevaVenta()
    return render_template('agregarVenta.html',formulario=form,mostrar_mje=False)
    
@app.route('/AgregarVenta', methods=['POST'])
def agregarVPost():
    formulario=FormularioNuevaVenta()
    valida=formulario.validate_on_submit()
    if (valida):
        admin = AdminDB('archivo.csv')
        admin.agregar(formulario)
        formulario=FormularioNuevaVenta()
        return render_template('agregarVenta.html',formulario=formulario,mostrar_mje=True)
    return render_template('error.html',formulario=formulario,valida=valida)

@app.route('/alta',methods=['GET'])
def altaG():
    form = FormularioAlta()
            
    return render_template('alta.html',form=form,mostrar_mje=False)
    
@app.route('/alta',methods=['POST'])
def altaP():
    admin =AdminDB('usuarios.csv')
    form = FormularioAlta()
    if (form.validate_on_submit()):
        if(form.password.data != form.confirm.data):
            return "Los passwords no coinciden!!! Hdp!"
        else:
            admin.agregar(form.username.data,form.password.data)
            return render_template('alta.html',form=form,mostrar_mje=True)
            
    return render_template('alta.html',form=form)

@login_manager.user_loader
def load_user(user_id):
    return UserRepository('usuarios.csv').getUser(user_id)
    
@app.route('/productosCliente',methods=['GET'])
@login_required
def prodXClienteG():
    admin=AdminDB('archivo.csv')
    lista=admin.get_lista_clientes()
    return render_template('prodXCliente.html',lista_clientes=lista)

@app.route('/productosCliente/<cliente_name>',methods=['GET'])
@login_required
def prodXClienteP(cliente_name):
    admin=AdminDB('archivo.csv')
    lista_productos=admin.get_productos_de_cliente(cliente_name)
    lista_clientes=admin.get_lista_clientes()
    return render_template('prodXCliente.html',lista_clientes=lista_clientes,lista_productos=lista_productos)

#@app.route('/productosCliente',methods=['POST'])
#@login_required
#def prodXClienteP():
    
@app.route('/login', methods=['GET'])
def loginG():
    form = FormularioLogin()    
    return (render_template('login.html',form = form))
    
    
@app.route('/login', methods=['POST'])
def loginP():
    form = FormularioLogin()
    if form.validate_on_submit():
        repository = UserRepository('usuarios.csv')
        user = repository.authenticate_user(form.name.data,form.password.data)
        if (user != None):
            login_user(user)
            next = request.args.get('next')
            
            return redirect(next or url_for('index'))
            #return render_template('session.html')
            
    return render_template('login.html', form=form,error=True)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('index.html')
    
@app.route('/session', methods=['GET'])
def return_session():
    return render_template('session.html')

##Manejo de errores####################
@app.errorhandler(401)
def not_authorized(e):
    return render_template('noLogin.html')

@app.errorhandler(404)
def not_found(e):
    return "Ooooooooooooooooooooooooops", 404

@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500    

##Fin Manejo de errores#################

if(__name__ == '__main__'):
    app.run(debug=True,host='0.0.0.0')
