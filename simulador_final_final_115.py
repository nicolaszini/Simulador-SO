import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import copy
import matplotlib.pyplot as plt
import random 
import numpy as np




#Clase heredada de QMainWindow (Constructor de ventanas)
class Ventana(QMainWindow):
 #Método constructor de la clase
	def __init__(self):
		#Iniciar el objeto QMainWindow
		QMainWindow.__init__(self)
		#Cargar la configuracón del archivo .ui en el objeto
		uic.loadUi("interfaz105.ui", self)
		self.setWindowTitle("Planificador de procesos")
		
		
		#no mostrar quantum, el cuadro de particionar ni el cuadro de particiones
		self.quantum.setVisible(False)
		self.lab_quantum_P_Alta.setVisible(True)
		self.lab_quantum_P_Media.setVisible(False)
		self.quantum_P_Alta.setVisible(True)
		self.quantum_P_Media.setVisible(False)
		self.lay_procesos.setEnabled(False)
		self.cajaProcesos.setEnabled(False)
		self.tab_widget.setCurrentIndex(0)
		self.quantum.setMaximum(10)
		self.lab_quantum.setVisible(False)
		self.group_particiones.setVisible(False)
		self.group_colas.setVisible(False)
		self.actualizar_part()
		self.real2 = 0
		self.tamReal(self.real2)
		self.BF.setEnabled(False)
		self.datos=list()
		########---- abrir archivos ???? ##########
		self.bot_guardar.clicked.connect(self.saveProceso)
		self.bot_cargar.clicked.connect(self.abrirArchivo)
		############################################
		self.bot_carga_procesos.clicked.connect(self.nextSteap)
		self.bot_rafaga.clicked.connect(self.agregar_rafaga)
		self.algoritmo.currentTextChanged.connect(self.clickEvent)
		self.algoritmos_P_Alta.currentTextChanged.connect(self.clickEvent2)
		self.algoritmos_P_Media.currentTextChanged.connect(self.clickEvent3)
		self.tam_memoria.valueChanged.connect(self.tamReal)
		self.tam_so.valueChanged.connect(self.tamReal)
		#no mostrar boton de particionar
		self.bot_limpiar_result1.clicked.connect(self.limpiar1)
		self.bot_limpiar_result2.clicked.connect(self.limpiar2)
		self.bot_limpiar_result3.clicked.connect(self.limpiar3)
		self.particion.currentTextChanged.connect(self.clickEvent)
		self.bot_volver.clicked.connect(self.volver)
		self.bot_proceso.clicked.connect(self.add_proceso)
		self.bot_planificar.clicked.connect(self.planificar)
		self.bot_borrar_todo.clicked.connect(self.borrar_todo)
		self.bot_borrar.clicked.connect(self.borrar)
		self.bot_agregar_part.clicked.connect(self.agregar_part)
		self.bot_eliminar_part.clicked.connect(self.eliminar_part)
		self.tam_memoria.valueChanged.connect(self.modificar)
		self.tam_so.valueChanged.connect(self.modificar)
		self.particion.currentTextChanged.connect(self.actualizar_part)
		self.quantum.valueChanged.connect(self.control_q)
		self.tam.setMaximum(self.tam_memoria.value())
		#self.opc_cargar_tabla.triggered.connect(self.cargar_tabla)
		self.box_tiempo.valueChanged.connect(self.imprimir_resultado2)
		self.box_tiempo.setEnabled(False)
		self.bot_graficar_gantt.setEnabled(False)
		self.gantt=list()
		self.bot_graficar_gantt.clicked.connect(self.graficar_gantt)
		self.prioridaList = list()
	
	

	def abrirArchivo(self,prioridaList):
		try:
			filename = QFileDialog.getOpenFileName(self,'Busqueda de archivo ',os.getenv('HOME'), "Text Files (*.txt)")
			
			with open(filename[0], 'r') as f:
				
				file_text = f.readline()
				file_text = f.readline()
				
				while file_text !='':			
					
					file_text=file_text.split('|')
					self.tab_procesos.setRowCount(self.tab_procesos.rowCount()+1)
					p=QTableWidgetItem(str(file_text[0]))
					p.setTextAlignment(Qt.AlignCenter)
					tam=QTableWidgetItem(str(file_text[1]))
					tam.setTextAlignment(Qt.AlignCenter)
					arribo=QTableWidgetItem(str(file_text[2]))
					arribo.setTextAlignment(Qt.AlignCenter)
					rafaga=file_text[3]
					rafaga=rafaga.rstrip('\n')
					rafaga=rafaga+''
					#print(rafaga)
					r=QTableWidgetItem(rafaga)
					
					if self.algoritmo.currentIndex() == 4:
						priori=QTableWidgetItem(str(file_text[4]))
						priori.setTextAlignment(Qt.AlignCenter)				
						
					else:
						self.prioridaList.append(str(file_text[4]))
						priori = "---"
						priori=QTableWidgetItem(str(priori))
						priori.setTextAlignment(Qt.AlignCenter)
						

					self.tab_procesos.setItem(self.tab_procesos.rowCount()-1,0,p)
					self.tab_procesos.setItem(self.tab_procesos.rowCount()-1,1,tam)
					self.tab_procesos.setItem(self.tab_procesos.rowCount()-1,2,arribo)
					self.tab_procesos.setItem(self.tab_procesos.rowCount()-1,3,r)
					self.tab_procesos.setItem(self.tab_procesos.rowCount()-1,4,priori)

					self.id_proceso.setText(str(self.tab_procesos.rowCount()+1))
					file_text = f.readline()
				f.close()
			
		except:
			pass	
	
	def saveProceso(self):

		if self.tab_procesos.rowCount() != 0:
			try:
				file = QFileDialog.getSaveFileName(self,'Guardar archivo',os.getenv('HOME'), "Text Files (*.txt)")
				
				with open(file[0], 'w') as f:
					
					f.write('ID|TAMAÑO|ARRIBO|RECURSO: TIEMPO|PRIORIDAD (Espacio entre recurso: y tiempo) \n')
					fila = str(self.tab_procesos.rowCount())
					columna = str(self.tab_procesos.columnCount())
					row = int(fila)				
					column = int(columna)
			
					for i in range(0,row):
						
						idp = self.tab_procesos.item(i,0)
						tamp = self.tab_procesos.item(i,1)
						arribop = self.tab_procesos.item(i,2)
						rafagap = self.tab_procesos.item(i,3)
						prioridadp = self.tab_procesos.item(i,4)
						f.write(idp.text()+'|'+tamp.text()+'|'+arribop.text()+'|'+rafagap.text()+'|'+prioridadp.text()+'\n')
					
			except:
				pass

		else:
			pass	


	def nextSteap(self):

		"""
		la funcion nextSteap pasa al usuario a la carga de los procesos, bloqueando todo lo referido a definicion
		de memoria y tipos de algoritmos de planificacion y ordenamiento.
		"""
		
		self.lay_procesos.setEnabled(True)
		self.cajaProcesos.setEnabled(True)
		self.frame.setEnabled(False)
		self.group_particiones.setEnabled(False)
		self.group_colas.setEnabled(False)
		self.renewTaable(self.prioridaList)

	def renewTaable(self,prioridaList):
		
		"""
		la funcion renewTable cambia la columna de prioridades segun corresponda la opcion
		seleccionada en la parte de algoritmos, colocando la proridad correspondiente del archivo cargado si se 
		esta utilizando el algoritmo de colas multinivel o --- si se utiliza cualquier otro.
		"""

		try:
			if self.algoritmo.currentIndex() == 4:
				
				cont = 0
				column = int(self.tab_procesos.columnCount())
				row = int(self.tab_procesos.rowCount())
			
				for i in range(0 , row):
					
					print(row)
					var =QTableWidgetItem( str(self.prioridaList[cont]))
					var.setTextAlignment(Qt.AlignCenter)
					
					for j in range(0,column):
						self.tab_procesos.setItem(i,self.tab_procesos.columnCount()-1, var )
					cont = cont + 1

			else:

				cont = 0
				column = int(self.tab_procesos.columnCount())
				row = int(self.tab_procesos.rowCount())

				for i in range(0 , row):
					print(row)
					var =QTableWidgetItem('---')
					var.setTextAlignment(Qt.AlignCenter)
		
					for j in range(0,column):
						self.tab_procesos.setItem(i,self.tab_procesos.columnCount()-1, var )
					cont = cont + 1

		except:
			pass	

	def limpiar1(self):
		self.algolConf.setText('-----')
		self.memConf.setText('-----')
		self.ordenConf.setText('-----')
		self.resul1.clear()
		self.lab_valor_rp_2.setText('0')
		self.lab_valor_ep_2.setText('0')

	def limpiar2(self):
		self.algolConf2.setText('-----')
		self.memConf2.setText('-----')
		self.ordenConf2.setText('-----')
		self.resul2.clear()
		self.lab_valor_rp_3.setText('0')
		self.lab_valor_ep_3.setText('0')


	def limpiar3(self):
		self.algolConf3.setText('-----')
		self.memConf3.setText('-----')
		self.ordenConf3.setText('-----')
		self.resul3.clear()
		self.lab_valor_rp_4.setText('0')
		self.lab_valor_ep_4.setText('0')

	def volver(self):

		"""
		la funcion volver pasa al usuario a la seleccion del tipo de memoria, tamaño, y seleccion de tipos de algoritmos y ordenamientos,
		bloqueando todo lo realacionado a la carga de procesos e inicializacion del planificador.
		"""

		self.frame.setEnabled(True)
		self.group_particiones.setEnabled(True)
		self.group_colas.setEnabled(True)
		self.cajaProcesos.setEnabled(False)
		self.lay_procesos.setEnabled(False)

	def tamReal(self,real2):
		real = round((int(self.tam_memoria.value()) * int(self.tam_so.value())) / 100)
		self.tam_real.setText(str(int(self.tam_memoria.value())-real))
		self.real2 = int(self.tam_real.text())

	def control(self):  #control de datos que debe realizar antes de ejecutar la planificacion
		if self.control_q() and self.control_m:
			if self.particion.currentIndex()==1: #si es variable entonces no tiene que controlar las particiones
				return True
			else:
				if self.control_p():
					return True
		else:
			return False

	def control_p(self): #controla las particiones
		if self.tab_procesos.rowCount()>0:
			return True
		else:			
			return False

	def control_m(self): #controla la memoria total
		if int(self.tam_real.text())!=0:
			self.tam_real.setStyleSheet("background-color: rgb(255, 255, 255);")
			if self.particiones.rowCount()>0:
				self.divisiones.setStyleSheet("background-color: rgb(255, 255, 255);")
				for i in range(self.particiones.rowCount()):
					if (self.particiones.item(i,0)==None or int(self.particiones.item(i,0).text())==0):
						self.particiones.item(i,0).setBackground(QColor('#ffff7f'))
						return False
				self.limpiar_raf()
				return True
			else:
				self.divisiones.setStyleSheet("background-color: rgb(255, 255, 127);")
				return False			
		else:
			self.tam_real.setStyleSheet("background-color: rgb(255, 255, 127);")
			return False

	def control_q(self):
		if self.algoritmo.currentIndex()==3:
			if self.quantum.value()>0:
				self.quantum.setStyleSheet("background-color: rgb(255, 255, 255);")
				return True
			else:
				self.quantum.setStyleSheet("background-color: rgb(255, 255, 127);")
				return False
		else:
			return True #si se selecciona rrq controla q

	def actualizar_part(self):
		resta=0
		self.tam.setMaximum(0)
		for i in range(self.particiones.rowCount()):
			if self.particiones.item(i,0).text()!='':
				resta=resta+int(self.particiones.item(i,0).text())
			if self.tam.maximum()<int(self.particiones.item(i,0).text()):
				self.tam.setMaximum(int(self.particiones.item(i,0).text()))
		resta=int(self.tam_real.text())-resta
		self.tam_restante.setText(str(resta)) #muestra el tamaño de memoria por asignar

	def agregar_part(self):
		if (self.tam_particion.value()!=0):
			tam_particion=self.tam_particion.value()
			if tam_particion<=int(self.tam_restante.text()):
				self.particiones.setRowCount(self.particiones.rowCount()+1)
				self.particiones.setItem(self.particiones.rowCount()-1,0,QTableWidgetItem(str(tam_particion)))
				self.particiones.item(self.particiones.rowCount()-1,0).setTextAlignment(Qt.AlignCenter)
				self.actualizar_part()
				self.tam_particion.setStyleSheet("background-color: rgb(255, 255, 255);")
			else:
				self.tam_particion.setStyleSheet("background-color: rgb(255, 255, 127);")
		else:
			self.tam_particion.setStyleSheet("background-color: rgb(255, 255, 127);")

	def eliminar_part(self):
		delete=list()
		for i in range(self.particiones.rowCount()):
			if self.particiones.item(i,0).isSelected():
					delete.append(i)		
		for i in delete:
			self.particiones.removeRow(i)
		self.actualizar_part()

	def particionar(self):
		if (self.divisiones.value()!=0):
			cant=self.divisiones.value()
			self.particiones.setRowCount(cant)
			tam=int(self.tam_real.tex())
			tam_part=tam/cant
			part=QTableWidgetItem()
			for i in range(self.particiones.rowCount()):
				self.particiones.setItem(i,0,QTableWidgetItem('0'))
				self.particiones.item(i,0).setTextAlignment(Qt.AlignCenter)
			self.divisiones.setStyleSheet("background-color: rgb(255, 255, 255);")
		else:
			self.divisiones.setStyleSheet("background-color: rgb(255, 255, 127);") #
		
	def modificar(self): #mofifica el valor del label tamaño restante
		self.tam_restante.setText(str(self.tam_real.text()))
		if self.particion.currentText()=='Variables':
			self.tam.setMaximum(self.tam_memoria.value())

	def borrar(self):  #borra las filas seleccionadas
		delete=list()
		for i in range(self.tab_procesos.rowCount()):
			for j in range(self.tab_procesos.columnCount()):				
				if self.tab_procesos.item(i,j).isSelected():
					delete.append(i)
					break
		for i in delete:
			self.tab_procesos.removeRow(i)
		if self.tab_procesos.rowCount()==0:
			self.id_proceso.setText(str(1))
		else:
			self.id_proceso.setText(str(int(self.tab_procesos.item(self.tab_procesos.rowCount()-1,0).text())+1)) #borra 

	
	def borrar_todo(self):
		i = 0
		if self.tab_procesos.rowCount() == 0:
			pass

		while self.tab_procesos.rowCount()>0:
			self.tab_procesos.removeRow(i)
			self.id_proceso.setText(str(self.tab_procesos.rowCount()+1)) #borra toda la lista de procesos
			self.resultado.clear()
			self.bot_graficar_gantt.setEnabled(False)
			self.box_tiempo.setEnabled(False)
			self.cola_cpu.clear()
			self.cola_entrada.clear()
			self.cola_salida.clear()
			self.datos_memoria.clear()
			self.lab_valor_rp.setText('0')
			self.lab_valor_ep.setText('0')
			self.arribo.setValue(0)
			self.tam.setValue(0)
			self.prioridaList.clear()		

	def planificar(self): #lleva a cabo la planificacion
		self.tab_widget.setCurrentIndex(1)
		if self.control():
			nue_p=list()
			#instanciar proceso para cada fila de la tabla de procesos
			if self.BF.isChecked():
				ordenamiento='BF'
			elif self.WF.isChecked():
				ordenamiento='WF'
			else:
				ordenamiento='FF'
			#se instancia el tipo de memoria seleccionada
			if self.particion.currentText()=='Variables':
				mem=Memoria_variable(self.tam_memoria.value(),ordenamiento)
			elif self.particion.currentText()=='Fijas':
				mem=Memoria_fija(self.tam_memoria.value(),ordenamiento)
				for i in range(self.particiones.rowCount()):
					h=int(self.particiones.item(i,0).text())
					mem.particiones.append(Particion(i+1,h))
			if self.algoritmo.currentIndex()==0:
				algoritmo='fifo'
			elif self.algoritmo.currentIndex()==1:
				algoritmo='sjf'
			elif self.algoritmo.currentIndex()==2:
				algoritmo='srtf'
			elif self.algoritmo.currentIndex()==3:
				algoritmo='rrq'
				q=self.quantum.value()
			else:
				algoritmo=list()
				algo1='rrq'
				if self.algoritmos_P_Media.currentIndex() == 0:
					algo2 = 'fifo'
				elif self.algoritmos_P_Media.currentIndex() == 1:
					algo2 = 'srtf'
				elif self.algoritmos_P_Media.currentIndex() == 2:
					algo2 = 'sjf'
				else:
					algo2 = 'rrq'
				if self.algoritmos_P_Baja.currentIndex() == 0:
					algo3 = 'fifo'
				elif self.algoritmos_P_Baja.currentIndex() == 1:
					algo3 = 'srtf'
				else:
					algo3 = 'sjf'
				algoritmo.append(algo1)
				algoritmo.append(algo2)
				algoritmo.append(algo3)
			for i in range(self.tab_procesos.rowCount()):
				p=int(self.tab_procesos.item(i,0).text())
				a=int(self.tab_procesos.item(i,2).text())
				tam=int(self.tab_procesos.item(i,1).text())
				rafaga=self.tab_procesos.item(i,3).text()
				if isinstance (algoritmo, list):
					prio=self.tab_procesos.item(i,4).text()
					if prio=='Alta' or prio == 'Alta\n':
						prio=1
					elif prio=='Media' or prio == 'Media\n':
						prio=2
					elif prio =='Baja' or prio == 'Baja\n':
						prio=3
				else:
					prio=0
				nue_p.append(proceso(p,a,tam,rafaga,prio))
			plan=planificador(algoritmo,nue_p, mem,self.quantum.value())
			resultado=plan.planificar()
			plan.promediar_t()
			self.imprimir_resultado(resultado[0])
			self.imprimir_promedios(plan.ret_prom,plan.esp_prom)			
			self.datos=plan.datos_proc
			self.bot_graficar_gantt.setEnabled(True)
			self.box_tiempo.setEnabled(True)
			self.box_tiempo.setMaximum(len(self.datos)-1)
			self.imprimir_resultado2()
			self.gantt=resultado[1]			

	def graficar_gantt(self):

		"""
		muestra el gantt si se realizo la planificacion, en caso contrario no hace nada.
		"""
		
		if self.gantt:
			self.gantt.show()
		else:
			pass

	def imprimir_promedios(self, retorno, espera):
		
		self.lab_valor_rp.setText(str(retorno))
		self.lab_valor_ep.setText(str(espera))
		
		if self.lab_valor_rp_2.text() =='0' or self.lab_valor_rp_2.text() =='':
		
			self.lab_valor_rp_2.setText(str(retorno))
			self.lab_valor_ep_2.setText(str(espera))
		
		elif self.lab_valor_rp_3.text() =='0':
		
			self.lab_valor_rp_3.setText(str(retorno))
			self.lab_valor_ep_3.setText(str(espera))
		
		else:
		
			self.lab_valor_rp_4.setText(str(retorno))
			self.lab_valor_ep_4.setText(str(espera))

	def imprimir_resultado2(self):
	
		cola_cpu=str(self.datos[self.box_tiempo.value()][0]).replace('[','').replace(']','')
		self.cola_cpu.setText(cola_cpu)
		cola_entrada=str(self.datos[self.box_tiempo.value()][1]).replace('[','').replace(']','')
		self.cola_entrada.setText(cola_entrada)
		cola_salida=str(self.datos[self.box_tiempo.value()][2]).replace('[','').replace(']','')
		self.cola_salida.setText(cola_salida)
		particiones=''
	
		for i in self.datos[self.box_tiempo.value()][3]:
	
			if self.particion.currentText()=='Fijas':
				particiones=particiones+'P:'+str(i.nro_particion)+'['+str(i.tamañoPart)+'] - '#particio fija no guarda el tamaño del proceso reveer si se quiere mostrar
			particiones=particiones+'ID: '+str(i.proceso_p)+'('+str(i.tamañoP)+')\n'
	
		self.datos_memoria.setText(particiones)
		self.datos_memoria.setStyleSheet('text-align: center')

	def imprimir_resultado(self,texto):

		self.resultado.setText(texto)
		val1 = self.resul1.toPlainText()
		val2 = self.resul2.toPlainText()
		val3 = self.resul3.toPlainText()
		
		if val1 =='':
			if self.algoritmo.currentIndex() == 0:
				self.algolConf.setText('FCFS')
			elif self.algoritmo.currentIndex() ==1:
				self.algolConf.setText('SJF')
			elif self.algoritmo.currentIndex() ==2:
				self.algolConf.setText('SRTF')
			elif self.algoritmo.currentIndex() ==3:
				self.algolConf.setText('RR')
			else:
				self.algolConf.setText('CM')
			if self.particion.currentIndex() == 0:
				self.memConf.setText('VARIABLE')
			else:
				self.memConf.setText('FIJA')
			if self.FF.isChecked():
				self.ordenConf.setText('FIRST FIT')
			elif self.BF.isChecked():
				self.ordenConf.setText('BEST FIT')
			else:
				self.ordenConf.setText('WORST FIT')
			self.resul1.setText(texto)
		elif val2 =='':
			if self.algoritmo.currentIndex() == 0:
				self.algolConf2.setText('FCFS')
			elif self.algoritmo.currentIndex() ==1:
				self.algolConf2.setText('SJF')
			elif self.algoritmo.currentIndex() ==2:
				self.algolConf2.setText('SRTF')
			elif self.algoritmo.currentIndex() ==3:
				self.algolConf2.setText('RR')
			else:
				self.algolConf2.setText('CM')
			if self.particion.currentIndex() == 0:
				self.memConf2.setText('VARIABLE')
			else:
				self.memConf2.setText('FIJA')
			if self.FF.isChecked():
				self.ordenConf2.setText('FIRST FIT')
			elif self.BF.isChecked():
				self.ordenConf2.setText('BEST FIT')
			else:
				self.ordenConf2.setText('WORST FIT')			
			self.resul2.setText(texto)
		else:
			if self.algoritmo.currentIndex() == 0:
				self.algolConf3.setText('FCFS')
			elif self.algoritmo.currentIndex() ==1:
				self.algolConf3.setText('SJF')
			elif self.algoritmo.currentIndex() ==2:
				self.algolConf3.setText('SRTF')
			elif self.algoritmo.currentIndex() ==3:
				self.algolConf3.setText('RR')
			else:
				self.algolConf3.setText('CM')
			if self.particion.currentIndex() == 0:
				self.memConf3.setText('VARIABLE')
			else:
				self.memConf3.setText('FIJA')
			if self.FF.isChecked():
				self.ordenConf3.setText('FIRST FIT')
			elif self.BF.isChecked():
				self.ordenConf3.setText('BEST FIT')
			else:
				self.ordenConf3.setText('WORST FIT')
			self.resul3.setText(texto)

	def print_resultados(self, cpu, e, s): #imprime resultados en ventana
		
		text='T | Proceso en uso de recurso'+'\n'
		
		for i in range(len(cpu)):
		
			text=text+str(i)+'|cpu: '+str(cpu[i][1])+'entrada: '+str(e[i][1])+' salida: '+ str(s[i][1])+'\n'
		
		self.resultado.setText(text)
	
	def clickEvent2(self): #para el combo box de la priridad media en cm
		
		if self.algoritmos_P_Alta.currentIndex()==3:
			self.lab_quantum_P_Alta.setVisible(True)
			self.quantum_P_Alta.setVisible(True)
		
		else:
			self.lab_quantum_P_Alta.setVisible(False)
			self.quantum_P_Alta.setVisible(False)

	def clickEvent3(self): #para el combo box de la priridad baja en cm
		
		if self.algoritmos_P_Media.currentIndex()==3:
			self.lab_quantum_P_Media.setVisible(True)
			self.quantum_P_Media.setVisible(True)
		
		else:
			self.lab_quantum_P_Media.setVisible(False)
			self.quantum_P_Media.setVisible(False)

	def clickEvent(self): #trae o quita de la ventana las opciones de quantum y particiones fija
		
		if self.algoritmo.currentIndex()==3: #activa la entrada del cuantum (el idx 3 es rrr)
			self.quantum.setVisible(True)
			self.lab_quantum.setVisible(True)
		
		else:
			self.quantum.setVisible(False)
			self.lab_quantum.setVisible(False)		
		
		if self.algoritmo.currentIndex()==4: #activa la entrada de las colas (el idx 4 es cm)
			self.group_colas.setVisible(True)
			self.lay_prioridad.setEnabled(True)			
		
		else:
			self.group_colas.setVisible(False)
			self.lay_prioridad.setEnabled(False)
		
		if self.particion.currentText()=='Fijas': #activa la entrada de las particiones 
			self.group_particiones.setVisible(True)
			self.BF.setEnabled(True)
			self.WF.setEnabled(False)
		
		else:
			self.tam.setMaximum(self.tam_memoria.value())
			self.group_particiones.setVisible(False)
			self.BF.setEnabled(False)
			self.WF.setEnabled(True)
		
	def add_proceso(self,real2): #agrega el proceso que se estaba editando a la tabla de procesos
		
		if self.id_proceso.text()!='' and self.tam.value()!=0 and self.tam.value() <= self.real2:
			if (self.verificar_rafagas()):				
				self.tab_procesos.setRowCount(self.tab_procesos.rowCount()+1)
				p=QTableWidgetItem(self.id_proceso.text())
				p.setTextAlignment(Qt.AlignCenter)
				tam=QTableWidgetItem(str(self.tam.value()))
				tam.setTextAlignment(Qt.AlignCenter)
				arribo=QTableWidgetItem(str(self.arribo.value()))
				arribo.setTextAlignment(Qt.AlignCenter)
				rafaga=''
				for i in range(self.rafaga.columnCount()):
					rafaga=rafaga+self.rafaga.item(0,i).text()+':'+self.rafaga.item(1,i).text()+';'
				r=QTableWidgetItem(rafaga)
				prioridad='---'
				if self.algoritmo.currentIndex() == 4:
					if self.lay_prioridad.currentIndex()==0:
						prioridad="Alta"
					elif self.lay_prioridad.currentIndex()==1:
						prioridad="Media"
					else:
						prioridad="Baja"
				else:
					prioridad = "---"
				prioridad=QTableWidgetItem(str(prioridad))
				prioridad.setTextAlignment(Qt.AlignCenter)
				self.tab_procesos.setItem(self.tab_procesos.rowCount()-1,0,p)
				self.tab_procesos.setItem(self.tab_procesos.rowCount()-1,1,tam)
				self.tab_procesos.setItem(self.tab_procesos.rowCount()-1,2,arribo)
				self.tab_procesos.setItem(self.tab_procesos.rowCount()-1,3,r)
				self.tab_procesos.setItem(self.tab_procesos.rowCount()-1,4,prioridad)				
				self.id_proceso.setText(str(self.tab_procesos.rowCount()+1))
				i=1
				while self.rafaga.columnCount()>1:
					self.rafaga.removeColumn(i)
				self.rafaga.item(1,0).setText('0')			
		else:
			pass

	def verificar_rafagas(self):
		
		for i in range(self.rafaga.columnCount()):
			if (self.rafaga.item(1,i)==None or int(self.rafaga.item(1,i).text())==0):
				self.rafaga.item(1,i).setBackground(QColor('#ffff7f'))
				return False
		self.limpiar_raf()
		return True #controla que ninguna de las rafagas sea 0

	def limpiar_raf(self): 
		
		for i in range(self.rafaga.columnCount()):
			self.rafaga.item(1,i).setBackground(QColor('white'))

	def limpiar_part(self):
		
		for i in range(self.particiones.rowCount()):
			self.particiones.item(i,0).setBackground(QColor('white'))

	def agregar_rafaga(self):
		
		self.rafaga.setColumnCount(self.rafaga.columnCount()+1)
		
		if (self.entrada.isChecked()):
			self.rafaga.setItem(0,self.rafaga.columnCount()-1,QTableWidgetItem('E')) #(fila columna, qtablewidgetitem) empieza de 0 tambien
		
		else:
			self.rafaga.setItem(0,self.rafaga.columnCount()-1, QTableWidgetItem('S'))
		#tiempo=self.tiempo.value()
		self.rafaga.setItem(1,self.rafaga.columnCount()-1, QTableWidgetItem('0'))
		self.rafaga.item(0,self.rafaga.columnCount()-1).setTextAlignment(Qt.AlignCenter)
		self.rafaga.item(1,self.rafaga.columnCount()-1).setTextAlignment(Qt.AlignCenter)
		#agrega una rafaga de cpu con 0 de tiempo
		self.rafaga.setColumnCount(self.rafaga.columnCount()+1)
		self.rafaga.setItem(0,self.rafaga.columnCount()-1, QTableWidgetItem('CPU'))
		self.rafaga.setItem(1,self.rafaga.columnCount()-1, QTableWidgetItem(str(0)))
		self.rafaga.item(0,self.rafaga.columnCount()-1).setTextAlignment(Qt.AlignCenter)
		self.rafaga.item(1,self.rafaga.columnCount()-1).setTextAlignment(Qt.AlignCenter) #agrega una rafaga de e o s y una de cpu automaticamente
		
class planificador:
	
	def __init__(self,algoritmo,tab,memoria,quantum):
		self.proc=tab
		self.memoria=memoria
		self.q=quantum
		self.cola=list()		
		self.alg=algoritmo
		self.q=''
		if self.alg=='rrq':
			self.q=quantum
		self.interrupcion=False			
		self.cpu=list() #contiene datos del proceso ejecutandose: proc, arribo, rafaga restante
		self.ent=list()
		self.sal=list()
		self.cola_bloq_e=list()
		self.cola_bloq_s=list()
		self.cola_list=list()
		self.gant_cpu=list()
		self.gant_e=list()
		self.gant_s=list()
		self.dat_proc=list()
		self.ret_prom=0
		self.esp_prom=0
		self.datos_proc=list()
		self.ordenar_proc()

	def planificar(self):
		listaX=list(range(0,80))
		plt.title('Grafico de Gantt',size=15)
		plt.xlabel('Tiempo',size=15)
		plt.ylabel('Procesos',size=15)
		plt.xticks(listaX)
		plt.plot([0,0],[0,0],marker="^",ls="-.",color="mediumturquoise",mec="darkcyan",ms=8,alpha=0.5,label="Arribo de proceso")
		plt.plot([0,0],[0,0],marker="v",ls="-.",color="red",mec="firebrick",ms=8,alpha=0.5,label="Fin de proceso")
		plt.plot([0,0],[0,0],marker="^",ls="-.",color="white",ms=8,alpha=1.0)
		plt.plot([0,0],[0,0],marker="v",ls="-.",color="white",ms=8,alpha=1.0)
		plt.plot([0,0],[0,0],color="mediumblue",lw=4,label="En CPU")
		plt.plot([0,0],[0,0],color="chocolate",lw=4,label="En disp. de entrada")
		plt.plot([0,0],[0,0],color="forestgreen",lw=4,label="En disp. de salida")
		plt.plot([0,0],[0,0],ls=":",color="mediumblue",lw=2,alpha=0.75,label="En cola de listos")
		plt.plot([0,0],[0,0],ls=":",color="chocolate",lw=2,alpha=0.75,label="En cola de bloq. de entrada")
		plt.plot([0,0],[0,0],ls=":",color="forestgreen",lw=2,alpha=0.75,label="En cola de bloq. de salida")
		t=0
		quantum=self.q
		exit=False
		resultado_icono=list()
		if self.memoria.algAsig=="BF":
			self.memoria.ordenarMemoriaBF()		
		resultado=''
		while len(self.proc)>0 or not exit: #sale cuando 
			#print('tiempo = '+str(t))
			resultado=resultado+'Tiempo: '+str(t)+'\n'
			#if self.alg=='rrq':
				#print('QUANTUM S:  ',quantum)
			self.add_cola(t)
	#-----------Eleccion del proximo proceso a ejecutarse en el recurso
			#print('cola listos: ',self.cola_list)
			resultado=resultado+'->Cola listos: '+str(self.cola_list)+'\n'
			if (len(self.cpu)==0 or quantum==0 or self.interrupcion): #trata la apropiacion de la cpu
				if (quantum==0 or self.interrupcion):
					if (quantum==0): #interrupcion por tiempo
						#print('Int. por fin de q')
						quantum=self.q
						resultado=resultado+'#Q!'+'\n'
						if (len(self.cpu)!=0):
							self.guardar_pbc()
					if (self.interrupcion):#interrupcion por e/s
					 	resultado=resultado+'#P!'+'\n'
					 	self.guardar_pbc()
					 	self.interrupcion=False
					 	#print('Int. por e/s')
				if (len(self.cola_list)>0): #elige el siguiente proceso a cpu
					print(self.cola_list)
					self.cola_list=self.elegir_proc_cl(self.alg,copy.deepcopy(self.cola_list))
				else:
					self.gant_cpu.append([t,0])
			#print('Cola bloq p/E:',self.cola_bloq_e)
			resultado=resultado+'->Cola bloq p/E:'+str(self.cola_bloq_e)+'\n'
			if (len(self.ent)==0): #si no hay nada en la cpu elegir un p de la cola de listos. SOLO SIRVE PARA EL PRIMER PROCESO Q ENTRE YA QUE (1)
				if (len(self.cola_bloq_e)>0):
					self.elegir_proc_cb('e')
				else:
					self.gant_e.append([t,0])
			#print('Cola bloq p/S:',self.cola_bloq_s)
			resultado=resultado+'->Cola bloq p/S:'+str(self.cola_bloq_s)+'\n'
			if (len(self.sal)==0): #si no hay nada en la cpu elegir un p de la cola de listos. SOLO SIRVE PARA EL PRIMER PROCESO Q ENTRE YA QUE (1)
				if (len(self.cola_bloq_s)>0):
					self.elegir_proc_cb('s')
				else:
					self.gant_s.append([t,0])			
			self.guardar_datos()
	#-----------Control de fin de rafagas de los procesos ejecutandose en recursos
			#print('PROCESO EN CPU: '+str(self.cpu))
			resultado=resultado+'CPU: '+str(self.cpu)+'\n'
			if (len(self.cpu)>0):
				plt.plot([t,t+1],[self.cpu[0],self.cpu[0]],color="mediumblue",lw=4)
				if (self.alg=='rrq'): #descuenta el quantum
					quantum=quantum-1
				self.cpu[1]=(self.cpu[1])-1
				self.gant_cpu.append([t,self.cpu[0]])	#UN PROCESO SE EJECUTA POR TODO EL SEGUNDO QUE INDICA CADA ARREGLO
				if (self.cpu[1]<1): #si termino su su tiempo de remanencia entonces echarlo
					if (self.alg=='rrq'):
						quantum=self.q
					self.fin_rafaga(self.cpu,'cpu',t)
					self.terminar_proc(t+1)
					self.cpu.clear()			
			#print('Rec Entrada: ', self.ent)
			resultado=resultado+'Entrada: '+str(self.ent)+'\n'
			if (len(self.ent)>0):
				plt.plot([t,t+1],[self.ent[0],self.ent[0]],color="chocolate",lw=4)
				self.ent[1]=(self.ent[1])-1
				self.gant_e.append([t,self.ent[0]])
				if (self.ent[1]<1): #si termino su su tiempo de remanencia entonces echarlo
					self.fin_rafaga(self.ent,'e',t)
					self.ent.clear()
			#print('Rec Salida: ', self.sal)
			resultado=resultado+'Salida: '+str(self.sal)+'\n'
			if (len(self.sal)>0):
				plt.plot([t,t+1],[self.sal[0],self.sal[0]],color="forestgreen",lw=4)
				self.sal[1]=(self.sal[1])-1
				self.gant_s.append([t,self.sal[0]])
				if (self.sal[1]<1): #si termino su su tiempo de remanencia entonces echarlo
					self.fin_rafaga(self.sal,'s',t)
					self.sal.clear()
			exit=True
			for i in self.cola:
				if i.tfin==0:
					exit=False
					break			
			for j in range(0,len(self.memoria.particiones)):
				self.memoria.particiones[j].impr_particion()				
			#resultado=resultado+'Tiempo: '+str(t)+'\n'+'->Cola listos: '+str(self.cola_list)+'\n'+'CPU: '+str(self.cpu)+'\n'+'->Cola bloq p/E:'+str(self.cola_bloq_e)+'\n'+'Entrada: '+str(self.ent)+'\n'+'->Cola bloq p/S:'+str(self.cola_bloq_s)+'\n'+'Salida: '+str(self.sal)+'\n'
			resultado=resultado+'_______________________'+'\n'			
			if len(self.cola_list)>0:
				for j in range(len(self.cola_list)):
					plt.plot([t,t+1],[self.cola_list[j][0],self.cola_list[j][0]],":",color="mediumblue",lw=2,alpha=1)
			if len(self.cola_bloq_e)>0:
				for j in range(len(self.cola_bloq_e)):
					plt.plot([t,t+1],[self.cola_bloq_e[j][0],self.cola_bloq_e[j][0]],":",color="chocolate",lw=2,alpha=0.75)
			if len(self.cola_bloq_s)>0:
				for j in range(len(self.cola_bloq_s)):
					plt.plot([t,t+1],[self.cola_bloq_s[j][0],self.cola_bloq_s[j][0]],":",color="forestgreen",lw=2,alpha=0.75)
			#print('_______________________________________')
			t=t+1
		resultado=resultado+'Tiempo: '+str(t)+'\n'+'->Cola listos: '+str(self.cola_list)+'\n'+'CPU: '+str(self.cpu)+'\n'+'->Cola bloq p/E:'+str(self.cola_bloq_e)+'\n'+'Entrada: '+str(self.ent)+'\n'+'->Cola bloq p/S:'+str(self.cola_bloq_s)+'\n'+'Salida: '+str(self.sal)+'\n'
		resultado=resultado+'___________________________'+'\n'
		self.guardar_datos()
		plt.legend(loc="best",framealpha=0.0)	
		return [resultado, plt]

	def add_cola(self, tact): #agrega a la cola si es el momento de arribo y si hay espacio en memoria
		delete=list()
		for i in range(len(self.proc)):
			#print(i)
			if(self.proc[i].arribo<=tact): #tiempo de arribo del proceso es igual al instante en el q esta entonces
				#if (self.memoria.disp(self.proc[i])==True): #Existe espacio en memoria para dicho proceso
				if self.memoria.asignarMemoria(self.proc[i].id,self.proc[i].tam)==True:
					#nuevo=[self.proc[i].id,self.proc[i].irrupcion,self.proc[i].recursos]
					nuevo=self.proc[i]
					self.cola.append(nuevo)
					
					plt.plot([tact,tact],[0,self.proc[i].id],"^-.",color="mediumturquoise",mec="darkcyan",ms=8,alpha=0.75)
					delete.append(self.proc[i])
		for i in delete:
			if (i in self.proc):
				self.proc.remove(i)
		#agregar a las colas particulares
		if isinstance (self.alg, list):
			self.cola=sorted(self.cola, key=lambda objeto: objeto.prioridad)
		for i in self.cola:
			if i.tfin==0:
				#busca la siguiente rafaga a ejecutar
				while i.rafagas[i.ejec].tiempo==0:
				 	i.ejec=i.ejec+1
				#como se realiza en todos los ciclos, se debe comprobar de que el proceso ya no este en cola del recurso
				if (i.rafagas[i.ejec].recurso)=='cpu':
					exist=False
					for j in self.cola_list:
						if (j[0]==i.id):
							exist=True
							break
					if not exist:
						self.cola_list.append([i.id,i.rafagas[i.ejec].tiempo,i.prioridad])
						if (len(self.cpu)>0 and (self.alg=='srtf' or isinstance(self.alg, list))):
							self.interrupcion=True						
				elif (i.rafagas[i.ejec].recurso)=='e':
					exist=False
					for j in self.cola_bloq_e:
						if (j[0]==i.id):
							exist=True
							break
					if not exist:
						self.cola_bloq_e.append([i.id,i.rafagas[i.ejec].tiempo])
				elif (i.rafagas[i.ejec].recurso)=='s':
					exist=False
					for j in self.cola_bloq_s:
						if (j[0]==i.id):
							exist=True
							break
					if not exist:
						self.cola_bloq_s.append([i.id,i.rafagas[i.ejec].tiempo])

	def guardar_datos(self):
		colaCpu=list()
		for i in self.cola_list:
			colaCpu.append(i[0])
		colaEnt=list()
		for i in self.cola_bloq_e:
			colaEnt.append(i[0])
		colaSal=list()
		for i in self.cola_bloq_s:
			colaSal.append(i[0])
		memoria=list()
		for i in self.memoria.particiones:
			memoria.append(copy.copy(i))
			#print(i.__dict__)
		self.datos_proc.append([colaCpu,colaEnt,colaSal,memoria])

	def elegir_proc_cl(self,alg, listos): #selecciona el proceso a cpu segun el algoritmo indicado
		if (alg=='sjf' or alg=='srtf'):
			tmin=listos[0][1]		
			p=listos[0]
			for pr in listos:			
				if (pr[1]<tmin):
					tmin=pr[1]
					p=pr					 
			self.cpu=[p[0],p[1],p[2]]
			listos.remove(p)
			listos.insert(0,p)
		elif (alg=='fifo' or alg=='rrq'):
			p=listos[0]
			self.cpu=[p[0],p[1],p[2]]
		else:
			max_pr=4
			print(listos)
			for l in listos:
				if l[2] < max_pr:
					max_pr=l[2]
			lista_aux=copy.deepcopy(listos)
			lista_aux=list(filter(lambda x: x[2] == max_pr, lista_aux))
			listos = list(filter(lambda x: x not in lista_aux, listos))
			lista_aux=self.elegir_proc_cl(alg[max_pr-1], lista_aux)
			listos = listos + lista_aux
			listos=sorted(listos, key=lambda x: x[2])
		return listos


	def elegir_proc_cb(self, tipo): #selecciona el siguiente proceso por fifo para las colas de bloqueados
		if (tipo=='e'):
			nue_proc=self.cola_bloq_e[0]
			self.ent=[nue_proc[0],nue_proc[1]]
		else:
			nue_proc=self.cola_bloq_s[0]
			self.sal=[nue_proc[0],nue_proc[1]]

	def guardar_pbc(self): #guarda la informacion del proceso que se interrumpio
		#print('interrumpe por fin q')
		proc_cpu=self.cpu
		i=0
		while (proc_cpu[0]!=self.cola_list[i][0]):
			i=i+1
		del self.cola_list[i]
		self.cola_list.append(proc_cpu)
		#print('CL dps de int: ', self.cola_list)

	def fin_rafaga(self,recurso,tipo,t): #cuando un proceso termina de usar un recurso se lo quita de la cola del recurso
		p=0
		#buscar en la cola general el proceso que se estaba ejecutando
		while ((p<len(self.cola)) and (self.cola[p].id!=recurso[0])):
			p=p+1
		#el proceso en el siguiente siclo debera hacer la siguiente rafaga indexada por cola.ejec o terminar definitivamente
		if (self.cola[p].id==recurso[0]):
			self.cola[p].ejec=self.cola[p].ejec+1
		#borro de la cola correspondiente al recurso que utilizaba
		if (tipo=='cpu'):			
			del self.cola_list[0]		
		elif (tipo=='e'):
			#plt.plot([t,t+1],[self.ent[0],self.ent[0]],color="chocolate",lw=4)
			del self.cola_bloq_e[0]
		elif (tipo=='s'):
			#plt.plot([t,t+1],[self.sal[0],self.sal[0]],color="forestgreen",lw=4)
			del self.cola_bloq_s[0]

	def terminar_proc(self,t): #quita de la cola general y de la memoria a un proceso que termino todas sus rafagas
		#busco el que se estaba ejecutando en la cola gral
		x=0
		idp=self.cpu[0]
		while (x<len(self.cola) and idp!=self.cola[x].id):
			x=x+1
		if (idp==self.cola[x].id):
			#verifica el contador el contador de rafagas. termina si es igual al tamaño pq empezo de 0
			if self.cola[x].ejec==len(self.cola[x].rafagas):
				#print('proceso ',self.cpu[0],' terminado')
				self.memoria.desasignarMemoria(self.cpu[0])
				
				plt.plot([t,t],[0,self.cpu[0]],"v-.",color="red",mec="firebrick",ms=8,alpha=0.75)
				self.cola[x].finalizar(t)				

	def ordenar_proc(self): #ordena procesos de la cola general por tiempo de arribo
		proc=list()		
		while(len(self.proc)>0):
			tmin=self.proc[0].arribo		
			p=self.proc[0]
			for pr in self.proc:			
				if (pr.arribo<tmin):
					tmin=pr.arribo
					p=pr
			proc.append(p)
			self.proc.remove(p)
		self.proc=proc #ordena los procesos por tiempo de arribo

	def promediar_t(self): #imprime los calculos promedios
		n=len(self.cola)
		for proceso in self.cola:
			self.ret_prom=self.ret_prom+proceso.retorno
			self.esp_prom=self.esp_prom+proceso.espera
		self.ret_prom=round(self.ret_prom/n,2)
		self.esp_prom=round(self.esp_prom/n,2)
		#print('Retorno promedio: '+str(self.ret_prom))
		#print('Espera promedio: '+str(self.esp_prom)) 

	def print_gant(self):
		#print('T | Proceso en uso de recurso')
		for i in range(len(self.gant_cpu)):
			pass
			#print(i,'|cpu: ',self.gant_cpu[i][1],'entrada: ',self.gant_e[i][1],' salida: ', self.gant_s[i][1])

	def print_gant2(self,label):
		text='T | Proceso en uso de recurso'
		for i in range(len(self.gant_cpu)):
			text=text+str(i)+'|cpu: '+str(self.gant_cpu[i][1])+'entrada: '+str(self.gant_e[i][1])+' salida: '+ str(self.gant_s[i][1])+'\n'
		#print(text)
		label.setText(text)

class proceso:
	def __init__(self, idp, arribo, tam, rafagas, prio):
		self.id=idp
		self.arribo=arribo
		#self.recursos=recursos
		self.tfin=0
		self.retorno=0
		self.tuso=0	
		self.prioridad=prio
		rafagas=rafagas.split(';')
		#print(rafagas)
		if '' in rafagas:
			rafagas.remove('')
		self.rafagas=list()
		for r in rafagas:
			r=r.split(':')
			self.rafagas.append(rafaga(r[0].lower(),int(r[1])))
		for i in self.rafagas:			
			self.tuso=self.tuso+i.tiempo
		self.espera=0
		self.tam=tam
		self.ejec=0
		
	def finalizar(self, t): #guarda los datos de finalizacion para el proceso una vez que se termina
		self.tfin=t
		self.retorno=self.tfin-self.arribo
		self.espera=self.retorno-self.tuso

class rafaga:
	def __init__(self,r,t):
		self.recurso=r
		self.tiempo=t

class Particion_variable:
	def __init__(self,tamañoProceso):
		self.tamañoP=tamañoProceso #proceso
		self.inicio=0
		self.proceso_p=0
		self.fin=self.inicio+self.tamañoP
	def impr_particion(self):
		pass

class Memoria_variable:
	def __init__(self,tamañoTot,algAsig):
		self.tamañoTot=tamañoTot
		self.particiones=[]
		self.algAsig=algAsig
		
	def asignarMemoria(self,procesoId,tamProceso):
		if len(self.particiones)==0:
			x=Particion_variable(tamProceso)
			x.proceso_p=procesoId
			x.fin=tamProceso
			self.particiones.append(x)
			y=Particion_variable(self.tamañoTot-tamProceso)
			y.proceso_p=0
			y.inicio=x.fin
			y.fin=self.tamañoTot
			self.particiones.append(y)
			return True
		else:
			if self.algAsig!="WF":
				band=False	
				for i in range (0,len(self.particiones)):
					if self.particiones[i].proceso_p==0:
						if self.particiones[i].tamañoP == tamProceso:
							self.particiones[i].proceso_p=procesoId
							return True
							break
						elif self.particiones[i].tamañoP > tamProceso:
							tamañoNuevo=self.particiones[i].tamañoP - tamProceso
							z=Particion_variable(tamañoNuevo)
							self.particiones[i].tamañoP=tamProceso
							self.particiones[i].proceso_p=procesoId
							self.particiones[i].fin=self.particiones[i].inicio + tamProceso
							z.proceso_p=0
							z.inicio=self.particiones[i].fin
							z.fin=z.inicio+z.tamañoP
							band=True
							pos=i+1
							break
				if band==True:
					self.particiones.insert(pos,z)
					return True
				else:
					#print ("No se pudo asignar el proceso ",procesoId," a memoria.")
					return False
			else:
				mayor=0
				mayorPos="null" #agregue esto porque si el proceso es muy grande para ser asignado a la memoria, al preguntar en el if de abajo, no se conoce a "mayorPos"
				for i in range(0,len(self.particiones)):
					if self.particiones[i].proceso_p==0:
						if self.particiones[i].tamañoP>=tamProceso: #Si la particion es más grande que el proceso:
							if self.particiones[i].tamañoP>mayor:	#Si la partición es, hasta ahora, la particion libre más grande:
								mayor=self.particiones[i].tamañoP
								mayorPos=i
				if mayorPos!="null":
					if self.particiones[mayorPos].tamañoP == tamProceso:
						self.particiones[mayorPos].proceso_p=procesoId
						return True
					elif self.particiones[mayorPos].tamañoP > tamProceso:
						tamañoNuevo=self.particiones[mayorPos].tamañoP - tamProceso
						z=Particion_variable(tamañoNuevo)
						self.particiones[mayorPos].tamañoP=tamProceso
						self.particiones[mayorPos].proceso_p=procesoId
						self.particiones[mayorPos].fin=self.particiones[mayorPos].inicio + tamProceso
						z.proceso_p=0
						z.inicio=self.particiones[mayorPos].fin
						z.fin=z.inicio+z.tamañoP
						band=True
						pos=mayorPos+1
						self.particiones.insert(pos,z)
						return True
				else:
					#print ("No se pudo asignar el proceso ",procesoId," a memoria.")
					return False
 
	def desasignarMemoria(self,procesoId):
		band1=False
		band2=False
		for i in range(0,len(self.particiones)):
			if self.particiones[i].proceso_p == procesoId:
				if i != 0 and i!= (len(self.particiones)-1):
					if self.particiones[i-1].proceso_p==0:
						band1=True
						pos1=i-1
						self.particiones[i].inicio=self.particiones[i-1].inicio
						self.particiones[i].tamañoP=self.particiones[i].tamañoP+self.particiones[i-1].tamañoP
					if self.particiones[i+1].proceso_p==0:
						band2=True
						pos2=i+1
						self.particiones[i].tamañoP=self.particiones[i].tamañoP+self.particiones[i+1].tamañoP
						self.particiones[i].fin=self.particiones[i+1].fin
					self.particiones[i].proceso_p=0
					break
				if i==0:
					if self.particiones[i+1].proceso_p==0:
						band2=True
						pos2=i+1
						self.particiones[i].tamañoP=self.particiones[i].tamañoP+self.particiones[i+1].tamañoP
						self.particiones[i].fin=self.particiones[i+1].fin
					self.particiones[i].proceso_p=0
					break
				if i==len(self.particiones)-1:
					if self.particiones[i-1].proceso_p==0:
						band1=True
						pos1=i-1
						self.particiones[i].inicio=self.particiones[i-1].inicio
						self.particiones[i].tamañoP=self.particiones[i].tamañoP+self.particiones[i-1].tamañoP
					self.particiones[i].proceso_p=0
					break
		if band1==True:
			del(self.particiones[pos1])
			if band2==True:
				del(self.particiones[pos2-1])
		else:
			if band2==True:
				del(self.particiones[pos2])
		#print("Proceso ",procesoId," terminado")
	
	def ordenarMemoriaBF(self):
		(self.particiones).sort(key=lambda Particion: int(Particion.tamañoP))
	
class Particion:
	def __init__(self,nro_particion,tamaño):
		self.nro_particion=nro_particion
		self.tamañoPart=tamaño #particion
		self.tamañoP=0 #proceso, asi tiene mismo nombre que la particion variable

		self.proceso_p=0
		
	def impr_particion(self):
		pass
		#if self.proceso_p!=0:
		#	print("Partición:",self.nro_particion,"  Tamaño:",self.tamañoPart," kB"," Proceso presente: ",self.proceso_p)
		#else:
		#	print("Partición:",self.nro_particion,"  Tamaño:",self.tamañoPart," kB"," PARTICION LIBRE")

class Memoria_fija:
	def __init__(self,tamañoTot,algAsig):
		self.tamañoTot=tamañoTot
		
		self.particiones=[]
		self.algAsig=algAsig #Será el tipo de asignacion de memoria: "BF" o "FF" en el caso de MEMORIA FIJA y "WF" o "FF" en el caso de MEMORIA VARIABLE
		
	def asignarMemoria(self,procesoId,tamProceso):
		for k in range(0,len(self.particiones)):
			if self.particiones[k].proceso_p ==0:
				if int(self.particiones[k].tamañoPart)>=tamProceso:
					self.particiones[k].proceso_p=procesoId
					self.particiones[k].tamañoP=tamProceso
					return True
					break
		#print("No se pudo asignar el proceso ",procesoId," a la memoria")
		return False				
		
	def desasignarMemoria(self,procesoId):
		for i in range(0,len(self.particiones)):
			if self.particiones[i].proceso_p ==procesoId:
				self.particiones[i].proceso_p=0
				self.particiones[i].tamañoP=0
				break				
		#print("Proceso ",procesoId," terminado")
	def ordenarMemoriaBF(self):
		(self.particiones).sort(key=lambda Particion: int(Particion.tamañoPart))

if __name__ == "__main__":
	import sys 
	#Instancia para iniciar una aplicación
	app = QApplication(sys.argv)
	#Crear un objeto de la clase
	_ventana = Ventana()
	#Mostrar la ventana
	_ventana.show()
	#Ejecutar la aplicación
	app.exec_()
	sys.exit(app.exec_())
