from validar import *

class AdminDB():
    def __init__(self,ruta=''):
        self.ruta_archivo=ruta
    def dame_list_archivo(self):
        with open(self.ruta_archivo, 'r') as f:
            reader = csv.reader(f)
            lista = list(reader)
        return lista
    def agregar(self,form):
        linea=''
        linea +=str(form.codigo.data)+','
        linea +=str(form.producto.data)+','
        linea +=str(form.cliente.data)+','
        linea +=str(form.cantidad.data)+','
        linea +=str(form.precio.data)+'\n'
        with open(self.ruta_archivo, 'a') as f:
            f.write(linea)
            
    def validar_archivo(self):
        validador=Validador(self.ruta_archivo)
        try:
            return validador.validar_archivo()
        except ValidacionException as e:
            return e.mensaje
            
    def agregar(self,usuario,password):
        archivo = open(self.ruta_archivo,'a')
        try:
            linea= str(usuario)+','+str(password)+','+'1'+'\n'
            archivo.write(linea)
        finally:
            archivo.close()
