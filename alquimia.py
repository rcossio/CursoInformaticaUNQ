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

