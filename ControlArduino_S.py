##uso de modulo pyserial
import serial as s
###################################

#Practica:
#   diseñar una interfaz de comunicación con arduino que contenga dos botones:
#           Normalizar       Estandarizar
#
#           Seleccionar 3 Sensores de los vistos en clase..
#               y comenzar el envio se parado de información de los sensores.
#
#           Con base en los datos recopilados, deberá aplicarse alguno de los procesos
#           de tratamiento de datos.
#
#           NOTA: los procesos solo podrán aplicarse cuando la comunicación serial se haya cerrado
#           NOTA2: los tres sensores enviarán la información al mismo tiempo
#           NOTA3: se aplicará cada proceso sobre los datos de los sensores de forma independiente
#           NOTA4: Al menos dos de los sensores deben entregar salidas con más de dos estados
#           


import sys

from PyQt5 import uic, QtWidgets, QtCore

qtCreatorFile = "ControlArduino_S.ui"  # Nombre del archivo

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.arduino = None

        self.btn_conexion.clicked.connect(self.conexion)


        self.SegundoPlano = QtCore.QTimer()
        self.SegundoPlano.timeout.connect(self.accion)


        self.btn_control.clicked.connect(self.control)

    def control(self):
        v = self.btn_control.text()
        if v == "PRENDER":
            self.btn_control.setText("APAGAR")
            self.arduino.write("1".encode())
        else:
            self.btn_control.setText("PRENDER")
            self.arduino.write("0".encode())

    def accion(self):
        #TAREA: diseñar una forma en la que solo se realicen lecturas cuando exista información que leer

        #print("Hola")
        valor = self.arduino.readline().decode()
        #print("A",valor,"F")
        valor = valor.replace("\n","")
        valor = valor.replace("\r", "")
        #print("E",valor,"R")

        self.datosSensor.addItem(valor)

        self.datosSensor.setCurrentRow(self.datosSensor.count()-1)

        ########################################################

    def conexion(self):
        v = self.btn_conexion.text()
        if v == "CONECTAR": #pasa de desconectado a conectado
            self.btn_conexion.setText("DESCONECTAR")

            if self.arduino == None: #SI NUNCA ME HABIA CONECTADO
                com = "COM" + self.txt_com.text()
                self.arduino = s.Serial(com, baudrate=9600, timeout=1000) ##realiza la conexion
                # y la iniciliza
                self.txt_estado.setText("INICIALIZADA")

                self.SegundoPlano.start(100)

            elif not self.arduino.isOpen():
                self.arduino.open()
                self.txt_estado.setText("REESTABLECIDA")

                self.SegundoPlano.start(100)

        else: #pasa de conectado a desconectado
            self.btn_conexion.setText("CONECTAR")

            self.arduino.close()
            self.txt_estado.setText("CERRADA")

            self.SegundoPlano.stop()

    def mensaje(self, msj):
        m = QtWidgets.QMessageBox()
        m.setText(msj)
        m.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())