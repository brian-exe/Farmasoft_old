import csv

class ValidacionException(Exception):
    def __init__(self,message=''):
        self.message=message
    def __repr__(self):
        print(message)

class Validador():
    def __init__(self, path=''):
        self.filePath=path
        self.icodigo=0
        self.icliente=0
        self.iproducto=0
        self.icantidad=0
        self.iprecio=0
        
    def validar_archivo(self):
        if (self.filePath == ''):
            raise ValidationException('Error, la ruta al archivo no está configurada')
        else:
            numLinea=0
            with open(self.filePath,'r') as f:
                reader= csv.reader(f)
                for linea in reader:
                    if(numLinea == 0):
                        self.setCabecera(linea)
                        numLinea+=1
                    else:
                        self.comprobarCantidadCampos(linea,numLinea)
                        
                        cliente=linea[self.icliente]
                        codigo=linea[self.icodigo]
                        producto=linea[self.iproducto]
                        cantidad=linea[self.icantidad]
                        precio=linea[self.iprecio]
                        
                        self.comprobarCampoVacio(codigo,numLinea)
                        self.comprobarEntero(cantidad,numLinea)
                        self.comprobarDecimal(precio,numLinea)
                        numLinea+=1
        return True
                        
    def setCabecera(self,listaCabecera):
        cantCabecera=0
        for i in range(len(listaCabecera)):
            if listaCabecera[i]=='CLIENTE':
                self.icliente=i
                cantCabecera+=1
            if listaCabecera[i] =='CODIGO':
                self.icodigo=i
                cantCabecera+=1
            if listaCabecera[i] =='PRODUCTO':
                self.iproducto=i
                cantCabecera+=1
            if listaCabecera[i] =='CANTIDAD':
                self.icantidad=i
                cantCabecera+=1
            if listaCabecera[i] =='PRECIO':
                self.iprecio=i
                cantCabecera+=1
        if (cantCabecera !=5):
                raise ValidationException('Error, la cabecera es incorrecta')
                 
    def comprobarCantidadCampos(self,linea,numLinea):
        if (len(linea) != 5):
            raise ValidationException("Error en Linea nro --> "+str(numLinea)+" del archivo. Cantidad invalida de campos.")
            
    def comprobarCampoVacio(self,campo,numLinea):
        if(campo ==''):
            raise ValidationException("Error en Linea nro --> "+str(numLinea)+" del  archivo. Campo vacío.")
            
    def comprobarEntero(self,campo,numLinea):
        try:
            aux=int(campo)#Se puede hacer con isinstance(valor,tipo)
        except ValueError:
            raise ValidationException("Error en Linea nro --> "+str(numLinea)+" tipo no admitido en campo cantidad.")
            
    def comprobarDecimal(self,campo,numLinea):
        try:
            aux=float(campo)
        except ValueError:
            raise ValidationException("Error en Linea nro --> "+str(numLinea)+" tipo no admitido en campo precio.")
