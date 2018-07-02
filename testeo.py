import unittest
from alquimia import *

class TestAlquimia(unittest.TestCase):

	def testAll(self):
		#--------------------------------
		#	Elemento
		#--------------------------------
                oxigeno   = Elemento(cantProtones=8,cantNeutrones=8,simbolo='O')
                hidrogeno = Elemento(cantProtones=1,cantNeutrones=0,simbolo='H')
                carbono   = Elemento(cantProtones=6,cantNeutrones=6,simbolo='C')
                nitrogeno = Elemento(cantProtones=7,cantNeutrones=7,simbolo='N')

	        self.assertEqual(  8, oxigeno.cantProtones())
	        self.assertEqual(  8, oxigeno.cantNeutrones())
	        self.assertEqual(  8, oxigeno.cantElectrones())
	        self.assertEqual(  8, oxigeno.numeroAtomico())
	        self.assertEqual( 16, oxigeno.pesoAtomico())
	        self.assertEqual(  4, oxigeno.valencia())
	        self.assertEqual('O', oxigeno.simbolo())


		#-----------------------------------
		#	Tabla
		#-----------------------------------
                tabla = TablaPeriodica()

                # Escribimos dos veces al nitrogeno para ver si la tabla lo agrega una sola vez
		# Esto deberia imprimir un Warning

                for elemento in [oxigeno,carbono,hidrogeno,nitrogeno,nitrogeno]:
                        tabla.agregarElemento(elemento)

                self.assertEqual(  4,len(tabla.elementos()))
                self.assertEqual(  6,tabla.elementoS('C').numeroAtomico())
                self.assertEqual( 14,tabla.elementoN(7).pesoAtomico())

		
		#---------------------------------------
		#	Compuesto
		#---------------------------------------

		# Definicion mas basica
		nh3 = Compuesto('NH3')
		nh3.agregarAtomo(tabla.elementoS("N"), "N1")
		nh3.agregarAtomo(tabla.elementoS("H"), "H2")
		nh3.agregarAtomo(tabla.elementoS("H"), "H3")
		nh3.agregarAtomo(tabla.elementoS("H"), "H4")
		nh3.enlazar("N1", "H2")
		nh3.enlazar("N1", "H3")
		nh3.enlazar("N1", "H4")
		self.assertEqual( 4, nh3.cantAtomos())
		self.assertEqual(["H2", "H3", "H4"], nh3.atomosDe(tabla.elementoS('H')))
		self.assertTrue(nh3.incluyeAtomo("N1"))
		self.assertFalse(nh3.incluyeAtomo("N4"))
		self.assertTrue(nh3.incluyeElemento(tabla.elementoS('N')))
		self.assertFalse(nh3.incluyeElemento(tabla.elementoS('O')))
		self.assertEqual(["N","H"], [elem.simbolo() for elem in nh3.elementosPresentes()])
		self.assertEqual(3, nh3.cantEnlaces())
		self.assertEqual(1, nh3.cantEnlacesAtomo("H2"))
		self.assertEqual(3, nh3.cantEnlacesAtomo("N1"))
		self.assertEqual(17, nh3.masaMolar())
		self.assertAlmostEqual(0.8235, nh3.proporcionSobreMasa(tabla.elementoS('N')),places=3)
		self.assertEqual([], nh3.atomosConEnlacesDisponibles())
		self.assertEqual([], nh3.atomosConEnlacesSobrantes())
		self.assertEqual(["N1"], nh3.conQuienesEstaEnlazado("H2"))
		self.assertEqual(['H2', 'H3', 'H4'], nh3.conQuienesEstaEnlazado("N1"))
		self.assertTrue(nh3.estanEnlazados(tabla.elementoS("H"), tabla.elementoS("N")))
		self.assertFalse(nh3.estanEnlazados(tabla.elementoS("H"), tabla.elementoS("H")))

		# Definicion Plus
		nh3 = Compuesto('NH3')
		nh3.agregarAtomo(tabla.elementoS("N"), "N1")
		nh3.agregarAtomos(tabla.elementoS("H"), ["H2", "H3", "H4"])
		nh3.enlazarConVarios("N1", ["H2", "H3", "H4"])
                self.assertEqual( 4, nh3.cantAtomos())
                self.assertEqual(["H2", "H3", "H4"], nh3.atomosDe(tabla.elementoS('H')))
                self.assertTrue(nh3.incluyeAtomo("N1"))
                self.assertFalse(nh3.incluyeAtomo("N4"))
                self.assertTrue(nh3.incluyeElemento(tabla.elementoS('N')))
                self.assertFalse(nh3.incluyeElemento(tabla.elementoS('O')))
                self.assertEqual(["N","H"], [elem.simbolo() for elem in nh3.elementosPresentes()])
                self.assertEqual(3, nh3.cantEnlaces())
                self.assertEqual(1, nh3.cantEnlacesAtomo("H2"))
                self.assertEqual(3, nh3.cantEnlacesAtomo("N1"))
                self.assertEqual(17, nh3.masaMolar())
                self.assertAlmostEqual(0.8235, nh3.proporcionSobreMasa(tabla.elementoS('N')),places=3)
                self.assertEqual([], nh3.atomosConEnlacesDisponibles())
                self.assertEqual([], nh3.atomosConEnlacesSobrantes())
                self.assertEqual(["N1"], nh3.conQuienesEstaEnlazado("H2"))
                self.assertEqual(['H2', 'H3', 'H4'], nh3.conQuienesEstaEnlazado("N1"))
                self.assertTrue(nh3.estanEnlazados(tabla.elementoS("H"), tabla.elementoS("N")))
                self.assertFalse(nh3.estanEnlazados(tabla.elementoS("H"), tabla.elementoS("H")))

		#Definicion Gold
		#y chequeo los enlaces disponibles
		nh3 = Compuesto('NH3')
		nh3.autoAgregarAtomo(tabla.elementoS("N"))
		self.assertEqual(["N1"],nh3.atomosConEnlacesDisponibles())
		nh3.autoAgregarAtomos(tabla.elementoS("H"), 3)
                self.assertEqual(["N1","H2", "H3", "H4"],nh3.atomosConEnlacesDisponibles())
		nh3.enlazarConVarios("N1", ["H2", "H3", "H4"])

		#Hago enlaces que no deberian poder hacerse, esto deberia marcar warnings
		nh3.enlazar("N1", "N1")
		nh3.enlazar("N1", "C5")
		nh3.enlazar("H2", "H3")
		nh3.enlazar("N1", "H2")

                self.assertEqual( 4, nh3.cantAtomos())
                self.assertEqual(["H2", "H3", "H4"], nh3.atomosDe(tabla.elementoS('H')))
                self.assertTrue(nh3.incluyeAtomo("N1"))
                self.assertFalse(nh3.incluyeAtomo("N4"))
                self.assertTrue(nh3.incluyeElemento(tabla.elementoS('N')))
                self.assertFalse(nh3.incluyeElemento(tabla.elementoS('O')))
                self.assertEqual(["N","H"], [elem.simbolo() for elem in nh3.elementosPresentes()])
                self.assertEqual(3, nh3.cantEnlaces())
                self.assertEqual(1, nh3.cantEnlacesAtomo("H2"))
                self.assertEqual(3, nh3.cantEnlacesAtomo("N1"))
                self.assertEqual(17, nh3.masaMolar())
                self.assertAlmostEqual(0.8235, nh3.proporcionSobreMasa(tabla.elementoS('N')),places=3)
                self.assertEqual([], nh3.atomosConEnlacesDisponibles())
                self.assertEqual([], nh3.atomosConEnlacesSobrantes())
                self.assertEqual(["N1"], nh3.conQuienesEstaEnlazado("H2"))
                self.assertEqual(['H2', 'H3', 'H4'], nh3.conQuienesEstaEnlazado("N1"))
                self.assertTrue(nh3.estanEnlazados(tabla.elementoS("H"), tabla.elementoS("N")))
                self.assertFalse(nh3.estanEnlazados(tabla.elementoS("H"), tabla.elementoS("H")))


		#-----------------------------------------------
		#	Medio
		#-----------------------------------------------
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

		self.assertEqual(3093,medioRaro.masaTotal())
		self.assertEqual(['O', 'H', 'N', 'C'],medioRaro.elementosPresentes())
		self.assertEqual(['H2O', 'NH3', 'CH4', 'CO2'],medioRaro.compuestosPresentes())
		self.assertEqual(1800,medioRaro.masaDeCompuesto(agua))
		self.assertEqual(357,medioRaro.masaDeCompuesto(nh3))
		self.assertAlmostEqual(0.5819,medioRaro.proporcionCompuestoSobreMasa(agua),places=3)
		self.assertEqual(128,medioRaro.cantMolesElemento(tabla.elementoS("O")))
		self.assertEqual(2048,medioRaro.masaDeElemento(tabla.elementoS("O")))
		self.assertAlmostEqual(0.6621,medioRaro.proporcionElementoSobreMasa(tabla.elementoS("O")),places=3)
		self.assertAlmostEqual(0.1108,medioRaro.proporcionElementoSobreMasa(tabla.elementoS("H")),places=3)


		#----------------------------------------------
		#	Descripcion de medio
		#----------------------------------------------
		miDescripcion = DescripcionMedio("[H2O][CO2][H2O][CH4][CH4]")

		self.assertTrue(miDescripcion.apareceCompuesto(agua))
		self.assertTrue(miDescripcion.apareceCompuesto(co2))
		self.assertFalse(miDescripcion.apareceCompuesto(nh3))
		self.assertEqual(2,miDescripcion.molesCompuesto(agua))
		self.assertEqual(1,miDescripcion.molesCompuesto(co2))
		self.assertEqual(0,miDescripcion.molesCompuesto(nh3))
		self.assertEqual(['H2O', 'CH4'],[ comp.name() for comp in miDescripcion.quienesAparecen([agua, nh3, metano])])
		self.assertEqual(100,medioRaro.cantidad(agua))
		miDescripcion.agregarAMedio(medioRaro,agua)
		self.assertEqual(102,medioRaro.cantidad(agua))

		# Vemos el antes y despues de agregar al medio
		self.assertEqual(20,medioRaro.cantidad(metano))
		miDescripcion.agregarAMedio(medioRaro,metano)
		self.assertEqual(22,medioRaro.cantidad(metano))
	
		self.assertEqual(21,medioRaro.cantidad(nh3))
		miDescripcion.agregarAMedio(medioRaro,nh3)
		self.assertEqual(21,medioRaro.cantidad(nh3))

		#-----------------------------------------------
		#	Reacciones quimicas
		#-----------------------------------------------
		# Creo un compuesto que no esta en el medio para chequear el False en la reaccion quimica
		hidrogeno = Compuesto('Hidrogeno')
		hidrogeno.autoAgregarAtomos(tabla.elementoS("H"), 2)
		hidrogeno.enlazar("H1", "H2")
 
		miReaccion = ReaccionQuimica([hidrogeno],[metano])
		self.assertFalse(miReaccion.sePuedeAplicar(medioRaro))
		
		# Ahora reviso un True en mi reaccion quimica
		miReaccion = ReaccionQuimica([metano],[nh3])
		self.assertTrue(miReaccion.sePuedeAplicar(medioRaro))
		self.assertEqual(22,miReaccion.maximoMoles(medioRaro))

		# Vemos los moles antes de la reaccion
		self.assertEqual(22,medioRaro.cantidad(metano))
		self.assertEqual(21,medioRaro.cantidad(nh3))

		# Hacemos la reaccion quimica y vemos los cambios
		miReaccion.aplicar(medioRaro,0.5)
		self.assertEqual(11,medioRaro.cantidad(metano))
		self.assertEqual(32,medioRaro.cantidad(nh3))

