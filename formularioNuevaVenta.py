from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *

class FormularioNuevaVenta(FlaskForm):
    codigo= StringField("Codigo de Producto", validators=[DataRequired()])
    producto= StringField("Nombre de Producto", validators=[DataRequired()])
    cliente= StringField("Nombre Cliente", validators=[DataRequired()])
    cantidad= StringField("Cantidad", validators=[DataRequired()])
    precio= StringField("Precio del Producto", validators=[DataRequired()])
    submit=SubmitField('Agregar')
    
    
class FormularioLogin(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')
