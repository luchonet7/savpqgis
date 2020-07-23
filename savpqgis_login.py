'''
Created on 22 nov. 2019

@author: Lucho
'''
import os

from qgis.core import QgsProject,QgsJsonExporter,QgsWkbTypes,Qgis,QgsExpressionContextUtils
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog,QMessageBox,QMenu
from PyQt5.QtGui import QPixmap, QImage   
import requests

from .acceso import AccesoToken
# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'savpqgis_dialog_login.ui'))


class savpqgisLogin(QDialog, FORM_CLASS):
    '''
    classdocs
    '''
    def __init__(self, menu= None, iface = None, parent=None):
        """Constructor."""
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        
        super(savpqgisLogin,self).__init__(parent)
        self.iface = iface
        self.Layers = None
        
        self.setupUi(self)
        self.menu = menu
        
        inputImg =  QImage(os.path.dirname(__file__) + "/login.png");
        pixmap01 = QPixmap.fromImage(inputImg)
        pixmap_image = QPixmap(pixmap01)
        self.label_3.setPixmap(pixmap_image)
        #self.accepted.connect(self.accepto)
        
    def accept(self):

        if (self.lineEdit.text() =="" or self.mLineEdit.text()=="") :
            QMessageBox.warning(self, 'Advertencia',  b'Ingresa usuario y/o contrase\xc3\xb1a'.decode("utf-8"))
            return
            
        try:
            API_ENDPOINT = AccesoToken.ip_server + "/Api/Login/authenticate"
            data_body = {'Usuario': self.lineEdit.text(), 
                    'Contrasena':self.mLineEdit.text()} 
            
            r = requests.post(url = API_ENDPOINT, data = data_body)
            
            if(r.status_code == 401) :
                QMessageBox.critical(self, 'Mensaje', b'Usuario y/o contrase\xc3\xb1a err\xc3\xb3neos'.decode("utf-8"))
                return
            
        except requests.exceptions.HTTPError as errh:
            self.iface.messageBar().pushMessage("Error", "Http Error:" + str(errh), level=Qgis.Critical)
            return
        except requests.exceptions.ConnectionError as errc:
            self.iface.messageBar().pushMessage("Error", "Error Connecting:" + str(errc), level=Qgis.Critical)
            return
        except requests.exceptions.Timeout as errt:
            self.iface.messageBar().pushMessage("Error", "Timeout Error:" + str(errt), level=Qgis.Critical)
            return
        except requests.exceptions.RequestException as err:
            self.iface.messageBar().pushMessage("Error", "OOps: Something Else" + str(err), level=Qgis.Critical)
            return
           
        data = r.json() 
        AccesoToken.acces_key=data['access_token']
        QgsExpressionContextUtils.setGlobalVariable('user_mtc', self.lineEdit.text())
           
        QMessageBox.information(self, 'Mensaje', 'Bienvenido '+self.lineEdit.text())
        
       
        action = [i for i in self.menu.actions() if i.text() == 'Cargar Capas'][0]
        action.setEnabled(True)
        action = [i for i in self.menu.actions() if i.text() == b'Cerrar Sesi\xc3\xb3n'.decode("utf-8")][0]
        action.setEnabled(True)
        action = [i for i in self.menu.actions() if i.text() == b'Iniciar Sesi\xc3\xb3n'.decode("utf-8")][0]
        action.setEnabled(False)
        self.close()

        
        
        

        