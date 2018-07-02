import sys
import re

class Elemento:
	def __init__(self,cantProtones=None,cantNeutrones=None,cantElectrones=None,simbolo=None):
		self._cantProtones   = int(cantProtones)
                self._cantNeutrones  = int(cantNeutrones)
                self._simbolo        = simbolo

	def cantProtones(self):
		return self._cantProtones

        def cantNeutrones(self):
                return self._cantNeutrones

        def cantElectrones(self):
                return self._cantProtones

        def numeroAtomico(self):
                return self._cantProtones

        def pesoAtomico(self):
                return self._cantProtones + self._cantNeutrones 

        def valencia(self):
		#Atomo especial
		if self.simbolo() == 'C':
			return 4

                _valencia = self._cantProtones
		for (nivel,orbital) in [(1,'s'),
					(2,'s'),(2,'p'),
					(3,'s'),(3,'p'),
					(4,'s'),(3,'d'),(4,'p'),
					(5,'s'),(4,'d'),(5,'p'),
					(6,'s'),(4,'f'),(5,'d'),(6,'p'),
                                        (7,'s'),(5,'f'),(6,'d'),(7,'p'),
                                        (8,'s'),(5,'g'),(6,'f'),(7,'d'),(8,'p')]:

			if orbital == 's':
				nelec = 2
			elif orbital == 'p':
				nelec = 6
			elif orbital == 'd':
				nelec = 10
			elif orbital == 'f':
				nelec = 14
			elif orbital == 'g':
				nelec = 18

			attempt = _valencia - nelec
			if attempt <= 0:
				if orbital in ['d','f','g']:
		                        sys.stdout.write('Info. Elemento de transicion o transicion interna.\n')

					return 2
				else:
					return _valencia
			else:
				_valencia -= nelec

        def simbolo(self):
                return self._simbolo



class TablaPeriodica:
	def __init__(self):
		self._elementos = []

	def agregarElemento(self,elemento): 
		symlist = []
		for elementoTabla in self.elementos():
			symlist.append(elementoTabla.simbolo())
		if elemento.simbolo() in symlist:
			sys.stdout.write('Warning. El simbolo "'+elemento.simbolo()+'" ya se encuentra en la tabla periodica. El elemento NO fue agregado.\n')
		else:
			self._elementos.append(elemento)

	def elementos(self): 
		return self._elementos

	def elementoS(self,simbolo):
                for elementoTabla in self.elementos():
                        if elementoTabla.simbolo() == simbolo:
				return elementoTabla


 
	def elementoN(self,numero): 
                for elementoTabla in self.elementos():
                        if elementoTabla.numeroAtomico() == numero:
                                return elementoTabla


class Compuesto:
	def __init__(self,name):
		self._name    = name
		self._atomos  = []
		self._enlaces = []
	
	def name(self):
		return self._name
	
	def agregarAtomo(self,elemento,nombreAtomo):
		namelist = []
                for atomoCompuesto in self._atomos:
                        namelist.append(atomoCompuesto[0])
                if nombreAtomo in namelist:
                        sys.stdout.write('Warning. El nombre "'+nombreAtomo+'" ya se encuentra en el compuesto. El atomo NO fue agregado.\n')
                else:
			self._atomos.append([nombreAtomo,elemento])

	def agregarAtomos(self, elemento, listaNombreAtomos):
		for nombreAtomo in listaNombreAtomos:
			self.agregarAtomo(elemento,nombreAtomo)		

	def autoAgregarAtomo(self,elemento):
		name = elemento.simbolo() + str(len(self._atomos)+1)
		self.agregarAtomo(elemento,name)

        def autoAgregarAtomos(self,elemento,numero):
		for i in range(numero):
			self.autoAgregarAtomo(elemento)


        def incluyeAtomo(self,nombre):
                for atomoCompuesto in self._atomos:
                        if atomoCompuesto[0] == nombre:
                                return True
                return False


	def elementoDe(self,nombreAtomo):
		for atomo in self._atomos:
			if nombreAtomo == atomo[0]:
				return atomo[1]

        def cantEnlacesAtomo(self,nombre):
                nEnlaces = 0
                for enlace in self._enlaces:
                        if nombre in enlace:
                                nEnlaces += 1
                return nEnlaces

	def conQuienesEstaEnlazado(self,nombre):
                listaEnlazados = []
                for enlace in self._enlaces:
                        if nombre in enlace:
				if nombre == enlace[0]:
					listaEnlazados.append(enlace[1])
				else:
					listaEnlazados.append(enlace[0])
                return listaEnlazados

	def estanEnlazados(self, elem1, elem2):
                for enlace in self._enlaces:
			if ( (elem1 == self.elementoDe(enlace[0])) and (elem2 == self.elementoDe(enlace[1]))  ):
				return True
                        if ( (elem1 == self.elementoDe(enlace[1])) and (elem2 == self.elementoDe(enlace[0]))  ):
                                return True
		return False



	def enlaceOK(self,nombreAtomo1,nombreAtomo2):
	
                if nombreAtomo1 == nombreAtomo2:
                        return False
		elif (not self.incluyeAtomo(nombreAtomo1)) or (not self.incluyeAtomo(nombreAtomo2)):
			return False
		elif ((self.cantEnlacesAtomo(nombreAtomo1) >= self.elementoDe(nombreAtomo1).valencia()) or
		      (self.cantEnlacesAtomo(nombreAtomo2) >= self.elementoDe(nombreAtomo2).valencia()) ):
			return False
                else:
			return True


	def enlazar(self,nombreAtomo1,nombreAtomo2):
		if self.enlaceOK(nombreAtomo1,nombreAtomo2):
			self._enlaces.append([nombreAtomo1,nombreAtomo2])
		else:
			sys.stdout.write('Warning. Hay un problema con este enlace. El enlace NO fue agregado.\n')

	def enlazarConVarios(self, nombreAtomo1, listaNombreAtomos):
		for nombreAtomo2 in listaNombreAtomos:
			self.enlazar(nombreAtomo1,nombreAtomo2)

	def cantAtomos(self):
		return len(self._atomos)

	def atomosDe(self,elemento):
		namelist = []
		for atomoCompuesto in self._atomos:
			if atomoCompuesto[1] == elemento:
				namelist.append(atomoCompuesto[0])
		return namelist


        def elementosPresentes(self):
                elemlist = []
                for atomoCompuesto in self._atomos:
                        if not atomoCompuesto[1] in elemlist:
                                elemlist.append( atomoCompuesto[1] )
                return elemlist


	def incluyeElemento(self,elemento):
		return elemento in self.elementosPresentes()

	def cantEnlaces(self):
		return len(self._enlaces)

	def masaMolar(self):
		masa = 0
		for atomo in self._atomos:
			masa += atomo[1].pesoAtomico()
		return masa
	
	def proporcionSobreMasa(self,elemento):
                masa = 0
                for atomo in self._atomos:
			if atomo[1] == elemento:
	                        masa += atomo[1].pesoAtomico()
		masa /= float(self.masaMolar())
                return masa
	def atomosConEnlacesSobrantes(self):
		lista = []
		for atomo in self._atomos:
			if (self.cantEnlacesAtomo(atomo[0]) > atomo[1].valencia()):
				lista.append(atomo[0])
		return lista
					
	def atomosConEnlacesDisponibles(self):
                lista = []
                for atomo in self._atomos:
                        if (self.cantEnlacesAtomo(atomo[0]) < atomo[1].valencia()):
                                lista.append(atomo[0])
                return lista


class Medio:
	def __init__(self):
		self._componentes = []
		self._cantidad = {}

	def cantidad(self,comp):
		return self._cantidad[comp]
	
	def agregarComponente(self,molecula,cantidad):
		if molecula in self._componentes:
			self._cantidad[molecula] += cantidad
		else:
			self._componentes.append(molecula)
			self._cantidad[molecula] = cantidad

	def masaTotal(self):
		masa = 0
		for molecula in self._componentes:
			masa += self.masaDeCompuesto(molecula)
		return masa

	def elementosPresentes(self):
		elemlist = []
                for molecula in self._componentes:
			for elemento in molecula.elementosPresentes():
				if not elemento.simbolo() in elemlist:
					elemlist.append(elemento.simbolo())
		return elemlist

	def compuestosPresentes(self):
		return [ molecula._name for molecula in self._componentes]

	def masaDeCompuesto(self,molecula):
		return float(self._cantidad[molecula]*molecula.masaMolar())

	def proporcionCompuestoSobreMasa(self,molecula):
		return self.masaDeCompuesto(molecula)/self.masaTotal()

	def cantMolesElemento(self,elem):
		moles=0.0
                for molecula in self._componentes:
			moles += self._cantidad[molecula]*len(molecula.atomosDe(elem))
		return moles
			
	def masaDeElemento(self,elem):
		return self.cantMolesElemento(elem)*elem.pesoAtomico()

        def proporcionElementoSobreMasa(self,elem):
		return self.masaDeElemento(elem)/self.masaTotal()

	
class DescripcionMedio:
	def __init__(self,string):
		lista = re.findall(r'\[([A-Za-z0-9_]+)\]',string) 
		self._cantidad = {i:lista.count(i) for i in lista}
		self._componentes = self._cantidad.keys()

	def apareceCompuesto(self,comp):
		return comp._name in self._componentes

	def molesCompuesto(self,comp):
		if self.apareceCompuesto(comp):
			return self._cantidad[comp._name]
		else:
			return 0

	def quienesAparecen(self,listaDeCompuestos):
		aparecen = []
		for comp in listaDeCompuestos:
			if self.apareceCompuesto(comp):
				aparecen.append(comp)
		return aparecen

	def agregarAMedio(self,medio, compuesto):
                if self.apareceCompuesto(compuesto):
			medio.agregarComponente(compuesto,self._cantidad[compuesto._name])
		
class ReaccionQuimica:
	def __init__(self,reactivos,productos):
		self._reactivos = reactivos
		self._productos = productos

	def sePuedeAplicar(self,medio):
		for reactivo in self._reactivos:
			if not reactivo in medio._componentes:
				return False
			if medio.masaDeCompuesto(reactivo) <= 0.0:
				return False
		return True

	def maximoMoles(self,medio):
		if not self.sePuedeAplicar(medio):
			return 0.0
		molesReactivos = []
                for reactivo in self._reactivos:
			molesReactivos.append(medio.masaDeCompuesto(reactivo)/reactivo.masaMolar())
		return max(molesReactivos)
	
	def aplicar(self,medio,proporcion):
		nMoles = proporcion*self.maximoMoles(medio)
                for reactivo in self._reactivos:
			medio.agregarComponente(reactivo,-nMoles)
                for producto in self._productos:
                        medio.agregarComponente(producto,nMoles)

'''
#----------------------------------------
#  1. Clase Elemento
#----------------------------------------
oxigeno   = Elemento(cantProtones=8,cantNeutrones=8,simbolo='O')
print 'oxigeno.cantProtones():', oxigeno.cantProtones()
print 'oxigeno.cantNeutrones():', oxigeno.cantNeutrones()
print 'oxigeno.cantElectrones():', oxigeno.cantElectrones()
print 'oxigeno.numeroAtomico():', oxigeno.numeroAtomico()
print 'oxigeno.pesoAtomico():', oxigeno.pesoAtomico()
print 'oxigeno.valencia():', oxigeno.valencia()
print 'oxigeno.simbolo():', oxigeno.simbolo()
print ''

hidrogeno = Elemento(cantProtones=1,cantNeutrones=0,simbolo='H')
carbono   = Elemento(cantProtones=6,cantNeutrones=6,simbolo='C')
nitrogeno = Elemento(cantProtones=7,cantNeutrones=7,simbolo='N')


#-----------------------------------------------
# 2. Clase TablaPeriodica
#-----------------------------------------------
tabla = TablaPeriodica()
for elemento in [oxigeno,hidrogeno,carbono,nitrogeno,nitrogeno]:
	tabla.agregarElemento(elemento)

print 'len(tabla.elementos()):',len(tabla.elementos()) 
print "tabla.elementoS('C').numeroAtomico():", tabla.elementoS('C').numeroAtomico()
print 'tabla.elementoN(7).pesoAtomico():', tabla.elementoN(7).pesoAtomico()
print ''

#---------------------------------------------------
#   3. Clase Compuesto
#---------------------------------------------------
nh3 = Compuesto('NH3')
nh3.agregarAtomo(tabla.elementoS("N"), "N1")
nh3.agregarAtomo(tabla.elementoS("H"), "H2")
nh3.agregarAtomo(tabla.elementoS("H"), "H3")
nh3.agregarAtomo(tabla.elementoS("H"), "H4")
nh3.enlazar("N1", "H2")
nh3.enlazar("N1", "H3")
nh3.enlazar("N1", "H4")

nh3 = Compuesto('NH3')
nh3.agregarAtomo(tabla.elementoS("N"), "N1")
nh3.agregarAtomos(tabla.elementoS("H"), ["H2", "H3", "H4"])
nh3.enlazarConVarios("N1", ["H2", "H3", "H4"])

nh3 = Compuesto('NH3')
nh3.autoAgregarAtomo(tabla.elementoS("N"))
print 'nh3.atomosConEnlacesDisponibles():', nh3.atomosConEnlacesDisponibles()
nh3.autoAgregarAtomos(tabla.elementoS("H"), 3)
nh3.enlazarConVarios("N1", ["H2", "H3", "H4"])
nh3.enlazar("N1", "N1")
nh3.enlazar("N1", "C5")
nh3.enlazar("H2", "H3")
nh3.enlazar("N1", "H2")


print 'nh3.cantAtomos():',nh3.cantAtomos()
print 'nh3.atomosDe(tabla.elementoS("H")):', nh3.atomosDe(tabla.elementoS('H'))
print 'nh3.incluyeAtomo("N1"):', nh3.incluyeAtomo("N1")
print 'nh3.incluyeAtomo("N4"):',nh3.incluyeAtomo("N4")
print 'nh3.incluyeElemento(tabla.elementoS("N")):', nh3.incluyeElemento(tabla.elementoS('N'))
print 'nh3.incluyeElemento(tabla.elementoS("O")):', nh3.incluyeElemento(tabla.elementoS('O'))
print '[elem.simbolo() for elem in nh3.elementosPresentes()]:', [elem.simbolo() for elem in nh3.elementosPresentes()]
print 'nh3.cantEnlaces():',nh3.cantEnlaces()
print 'nh3.cantEnlacesAtomo("H2"):', nh3.cantEnlacesAtomo("H2")
print 'nh3.cantEnlacesAtomo("N1"):', nh3.cantEnlacesAtomo("N1")
print 'nh3.masaMolar():',nh3.masaMolar()
print 'nh3.proporcionSobreMasa(tabla.elementoS("N"))', nh3.proporcionSobreMasa(tabla.elementoS('N'))
print 'nh3.atomosConEnlacesDisponibles():', nh3.atomosConEnlacesDisponibles()
print 'nh3.atomosConEnlacesSobrantes():', nh3.atomosConEnlacesSobrantes()
print 'nh3.conQuienesEstaEnlazado("H2"):', nh3.conQuienesEstaEnlazado("H2")
print 'nh3.conQuienesEstaEnlazado("N1"):', nh3.conQuienesEstaEnlazado("N1")
print 'nh3.estanEnlazados(tabla.elementoS("H"), tabla.elementoS("N")):', nh3.estanEnlazados(tabla.elementoS("H"), tabla.elementoS("N"))
print 'nh3.estanEnlazados(tabla.elementoS("H"), tabla.elementoS("H")):', nh3.estanEnlazados(tabla.elementoS("H"), tabla.elementoS("H"))
print ''

#---------------------------------------------
#   4. Medio
#---------------------------------------------
agua = Compuesto('H2O')
agua.autoAgregarAtomo(tabla.elementoS("O"))
agua.autoAgregarAtomos(tabla.elementoS("H"), 2)
agua.enlazarConVarios("O1", ["H2", "H3"])

metano = Compuesto('CH4')
metano.autoAgregarAtomo(tabla.elementoS("C"))
metano.autoAgregarAtomos(tabla.elementoS("H"), 4)
metano.enlazarConVarios("C1", ["H2", "H3","H4","H5"])

co2 = Compuesto('CO2')
co2.autoAgregarAtomo(tabla.elementoS("C"))
co2.autoAgregarAtomos(tabla.elementoS("O"), 2)
co2.enlazarConVarios("C1", ["O2", "O3"])


medioRaro = Medio()
medioRaro.agregarComponente(agua, 100)
medioRaro.agregarComponente(nh3, 6)
medioRaro.agregarComponente(metano, 20)
medioRaro.agregarComponente(co2, 14)
medioRaro.agregarComponente(nh3, 15)
print 'medioRaro.masaTotal():',medioRaro.masaTotal()
print 'medioRaro.elementosPresentes():',medioRaro.elementosPresentes()
print 'medioRaro.compuestosPresentes():',medioRaro.compuestosPresentes()
print 'medioRaro.masaDeCompuesto(agua):',medioRaro.masaDeCompuesto(agua)
print 'medioRaro.masaDeCompuesto(nh3):',medioRaro.masaDeCompuesto(nh3)
print 'medioRaro.proporcionCompuestoSobreMasa(agua):', medioRaro.proporcionCompuestoSobreMasa(agua)
print 'medioRaro.cantMolesElemento(tabla.elementoS("O")):', medioRaro.cantMolesElemento(tabla.elementoS("O"))
print 'medioRaro.masaDeElemento(tabla.elementoS("O")):', medioRaro.masaDeElemento(tabla.elementoS("O"))
print 'medioRaro.proporcionElementoSobreMasa(tabla.elementoS("O")):',medioRaro.proporcionElementoSobreMasa(tabla.elementoS("O"))
print 'medioRaro.proporcionElementoSobreMasa(tabla.elementoS("H")):',medioRaro.proporcionElementoSobreMasa(tabla.elementoS("H"))
print ''

#---------------------------------------------------
#   5. Descripcion del medio
#---------------------------------------------------
miDescripcion = DescripcionMedio("[H2O][CO2][H2O][CH4][CH4]")

print "miDescripcion.apareceCompuesto(agua):", miDescripcion.apareceCompuesto(agua)
print "miDescripcion.apareceCompuesto(co2):", miDescripcion.apareceCompuesto(co2)
print "miDescripcion.apareceCompuesto(nh3):", miDescripcion.apareceCompuesto(nh3)
print "miDescripcion.molesCompuesto(agua):", miDescripcion.molesCompuesto(agua)
print "miDescripcion.molesCompuesto(co2):", miDescripcion.molesCompuesto(co2)
print "miDescripcion.molesCompuesto(nh3):", miDescripcion.molesCompuesto(nh3)
print "miDescripcion.quienesAparecen([agua, nh3, metano]):", miDescripcion.quienesAparecen([agua, nh3, metano])
print "miDescripcion.agregarAMedio(medioRaro,agua):", medioRaro._cantidad[agua],
miDescripcion.agregarAMedio(medioRaro,agua)
print "cambia a ", medioRaro._cantidad[agua]


print "miDescripcion.agregarAMedio(medioRaro,metano):", medioRaro._cantidad[metano], 
miDescripcion.agregarAMedio(medioRaro,metano)
print "cambia a ", medioRaro._cantidad[metano] 

print "miDescripcion.agregarAMedio(medioRaro,nh3):", medioRaro._cantidad[nh3],
miDescripcion.agregarAMedio(medioRaro,nh3)
print "cambia a ", medioRaro._cantidad[nh3]
print ''

#------------------------------------------------------
#    6. Reacciones Quimicas
#------------------------------------------------------
hidrogeno = Compuesto('Hidrogeno')
hidrogeno.autoAgregarAtomos(tabla.elementoS("H"), 2)
hidrogeno.enlazar("H1", "H2")
 
miReaccion = ReaccionQuimica([hidrogeno],[metano])
print 'miReaccion.sePuedeAplicar(medioRaro):',miReaccion.sePuedeAplicar(medioRaro)

miReaccion = ReaccionQuimica([metano],[nh3])
print 'miReaccion.sePuedeAplicar(medioRaro):',miReaccion.sePuedeAplicar(medioRaro)
print 'miReaccion.maximoMoles(medioRaro):',miReaccion.maximoMoles(medioRaro)
print 'miReaccion.aplicar(medioRaro,0.5):', 'metano=',medioRaro._cantidad[metano], 'nh3=',medioRaro._cantidad[nh3],
miReaccion.aplicar(medioRaro,0.5)
print 'cambia a metano=',medioRaro._cantidad[metano], 'nh3=',medioRaro._cantidad[nh3]
'''
