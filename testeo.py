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

