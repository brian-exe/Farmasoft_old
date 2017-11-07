import csv
class Config():
    def __init__(self):
        self.ARCHIVO_USUARIOS=""
        self.ARCHIVO_DATOS=""
        with open('./datos/config.conf','r') as f:
            reader=csv.reader(f,delimiter=':')
            for linea in reader:
                if linea[0]=='datos':
                    self.ARCHIVO_DATOS=linea[1]
                if linea[0]=='usuarios':
                    self.ARCHIVO_USUARIOS=linea[1]
                
    def get_path_to_users_file(self):
        return self.ARCHIVO_USUARIOS
    
    def get_path_to_data_file(self):
        return self.ARCHIVO_DATOS
        
    def reload_configurations(self):
        with open('./datos/config.conf','r') as f:
            reader=csv.reader(f,delimiter=':')
            for linea in reader:
                if linea[0]=='datos':
                    self.ARCHIVO_DATOS=linea[1]
                if linea[0]=='usuarios':
                    self.ARCHIVO_USUARIOS=linea[1]
        return True
