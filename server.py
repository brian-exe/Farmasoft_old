#!/home/brian/Envs/env1/bin/python3.5

from flask import Flask,request, url_for,render_template,redirect
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from flask_login import LoginManager, login_user, login_required, logout_user,current_user
from formularios import *
from AdminDB import *
from validar import ValidationException
from user_administration import User,UserRepository
from Config import Config
import csv



app= Flask(__name__)
app.config['SECRET_KEY'] = '$$hard$$secret$$key$$'
#app.config['BOOTSTRAP_SERVE_LOCAL'] = True
boot = Bootstrap(app)
login_manager=LoginManager()
login_manager.init_app(app)
manager=Manager(app)
configurador = Config()
app.config['ARCHIVO_DB']=configurador.get_path_to_data_file()
app.config['ARCHIVO_USUARIOS']=configurador.get_path_to_users_file()

'''Metodo encargado de leer el archivo de configuraciones y recargar las variables ARCHIVO_DB y ARCHIVO_USUARIOS'''
def recargarConfiguraciones():
    if (configurador.reload_configurations()):
        app.config['ARCHIVO_DB']=configurador.get_path_to_data_file()
        app.config['ARCHIVO_USUARIOS']=configurador.get_path_to_users_file()

#INICIO RUTAS#
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
    
@app.route('/configurar')
def configurar():
    recargarConfiguraciones()
    return "Configurado!"
    
@app.route('/lista',methods=['GET'])
@login_required
def listarCsv():
    admin = AdminDB(app.config['ARCHIVO_DB'])
    archivo = admin.dame_list_archivo()
    return render_template('lista.html',model=archivo)
    
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
        admin = AdminDB(app.config['ARCHIVO_DB'])
        admin.agregar_venta(formulario)
        formulario=FormularioNuevaVenta()
        return render_template('agregarVenta.html',formulario=formulario,mostrar_mje=True)
    #formulario=FormularioNuevaVenta()
    return render_template('agregarVenta.html',formulario=formulario,mostrar_mje=False)

@app.route('/alta',methods=['GET'])
def altaG():
    form = FormularioAlta()
            
    return render_template('alta.html',form=form,mostrar_mje=False)
    
@app.route('/alta',methods=['POST'])
def altaP():
    user_admin =UserRepository(app.config['ARCHIVO_USUARIOS'])
    form = FormularioAlta()
    if (form.validate_on_submit()):
        if(form.password.data == form.confirm.data):
            user_admin.add_user(form.username.data,form.password.data)
            return render_template('alta.html',form=form,mostrar_mje=True)
            
    return render_template('alta.html',form=form)

@login_manager.user_loader
def load_user(user_id):
    return UserRepository(app.config['ARCHIVO_USUARIOS']).getUser(user_id)
    
@app.route('/productosCliente',methods=['GET'])
@app.route('/productosCliente/',methods=['GET'])
@login_required
def prodXClienteG():
    admin=AdminDB(app.config['ARCHIVO_DB'])
    lista=admin.get_lista_clientes()
    return render_template('prodXCliente.html',lista_clientes=lista)

@app.route('/productosCliente/cliente=<cliente_name>',methods=['GET'])
@login_required
def prodXClienteP(cliente_name):
    admin=AdminDB(app.config['ARCHIVO_DB'])
    lista_productos=admin.get_productos_de_cliente(cliente_name)
    lista_clientes=admin.get_lista_clientes()
    return render_template('prodXCliente.html',lista_clientes=lista_clientes,lista_productos=lista_productos,busqueda=cliente_name)
    
@app.route('/clientesProductos',methods=['GET'])
@app.route('/clientesProductos/',methods=['GET'])
@login_required
def clienteXProdG():
    admin=AdminDB(app.config['ARCHIVO_DB'])
    lista=admin.get_lista_productos()
    return render_template('clientesXProd.html',lista_productos=lista)

@app.route('/clientesProductos/producto=<producto_name>',methods=['GET'])
@login_required
def clienteXProdP(producto_name):
    admin=AdminDB(app.config['ARCHIVO_DB'])
    lista_productos=admin.get_lista_productos()
    lista_clientes=admin.get_clientes_de_productos(producto_name)
    return render_template('clientesXProd.html',lista_clientes=lista_clientes,lista_productos=lista_productos,busqueda=producto_name)

@app.route('/masVendidos',methods=['GET'])
@app.route('/masVendidos/',methods=['GET'])
@login_required
def masVendidosG():
    return render_template('masVendidos.html')

@app.route('/masVendidos/cantResultados=<cant_resultados>',methods=['GET'])
@login_required
def masVendidosP(cant_resultados):
    admin=AdminDB(app.config['ARCHIVO_DB'])
    lista_resultados=admin.get_cant_mas_vendidos(cant_resultados)
    return render_template('masVendidos.html', lista_resultados=lista_resultados)
    
@app.route('/mejoresClientes/',methods=['GET'])
@app.route('/mejoresClientes',methods=['GET'])
@login_required
def mejoresClientesG():
    return render_template('mejoresClientes.html')
    
@app.route('/mejoresClientes/cantResultados=<cant_resultados>',methods=['GET'])
@login_required
def mejoresClientesP(cant_resultados):
    admin=AdminDB(app.config['ARCHIVO_DB'])
    lista_resultados=admin.get_cant_mejores_clientes(cant_resultados)
    return render_template('mejoresClientes.html', lista_resultados=lista_resultados)
    
    
@app.route('/editarUsuarios',methods=['GET'])
def editar_usuarios():
    if not current_user.is_admin():
        return "No es admin!"
    else:
        user_admin =UserRepository(app.config['ARCHIVO_USUARIOS'])
        model=user_admin.get_user_list()
        return render_template('editarUsuarios.html',model=model)
    
@app.route('/editarUsuario/<usuario>',methods=['GET','POST'])
def editar_usuario(usuario):
    form=FormularioEditarUsuario()
    user_admin =UserRepository(app.config['ARCHIVO_USUARIOS'])
    user=user_admin.getUser(usuario)
    form.username.data=user.name
    #form.role.data=user.role
    form.roles.choices=user_admin.get_role_list()
    
    if form.validate_on_submit():
        user_admin.change_role_user(form.username.data,form.roles.data)
        return redirect(url_for('editar_usuarios'))

    return render_template('editarUsuario.html',formulario=form)

#@app.route('/cambiarArchivo')

@app.route('/login', methods=['GET'])
def loginG():
    if (current_user.is_authenticated):
        return redirect('/')
    else:
        form = FormularioLogin()
        return (render_template('login.html',form = form))
    
    
@app.route('/login', methods=['POST'])
def loginP():
    form = FormularioLogin()
    if form.validate_on_submit():
        repository = UserRepository(app.config['ARCHIVO_USUARIOS'])
        user = repository.authenticate_user(form.name.data,form.password.data)
        if (user != None):
            login_user(user)
            next = request.args.get('next')
            return redirect(next or url_for('index'))
            
    return render_template('login.html', form=form,error=True)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('index.html')
    
#FIN SECCION RUTAS#


##Manejo de errores####################

'''Error handler personalizado para atrapar las excepciones de validacion que pudieran ocurrir'''
@app.errorhandler(ValidationException)
def custom_handler(e):
    return render_template('customError.html', mensaje=e.message )
    
@app.errorhandler(401)
def not_authorized(e):
    return render_template('noLogin.html')

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500    

##Fin Manejo de errores#################

    

if(__name__ == '__main__'):
    manager.run()
