from django.test import TestCase
from django.urls import reverse
from serviciosApp.models import Servicio
from .models import Solicitud


class SolicitudListadoTests(TestCase):
	@classmethod
	def setUpTestData(cls):
		Solicitud.objects.all().delete()
		Solicitud.objects.create(
			nombre='Solicitud de luminaria defectuosa',
			estado='Pendiente',
			sector='Centro',
			descripcion='Falta iluminación en una calle.',
		)
		Solicitud.objects.create(
			nombre='Revisión de bache en avenida principal',
			estado='En proceso',
			sector='La Serena',
			descripcion='Deterioro en la superficie de la avenida.',
		)

	def test_lista_muestra_controles_y_datos(self):
		response = self.client.get(reverse('solicitudes'))
		solicitud = Solicitud.objects.get(nombre='Solicitud de luminaria defectuosa')
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Agregar')
		self.assertContains(response, 'Modificar')
		self.assertContains(response, 'Eliminar')
		self.assertContains(response, 'Buscar')
		self.assertContains(response, 'Solicitud de luminaria defectuosa')
		self.assertContains(response, reverse('admin:solicitudesApp_solicitud_add'))
		self.assertContains(
			response,
			reverse('admin:solicitudesApp_solicitud_change', args=[solicitud.pk]),
		)
		self.assertContains(
			response,
			reverse('admin:solicitudesApp_solicitud_delete', args=[solicitud.pk]),
		)

	def test_busqueda_filtra_solicitudes(self):
		response = self.client.get(reverse('solicitudes'), {'q': 'Centro'})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Solicitud de luminaria defectuosa')
		self.assertNotContains(response, 'Revisión de bache en avenida principal')

	def test_inicio_muestra_cantidades_orm(self):
		response = self.client.get(reverse('home'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Solicitudes registradas')
		self.assertContains(response, 'Servicios disponibles')
		self.assertContains(response, f'>{Solicitud.objects.count()}</p>')
		self.assertContains(response, f'>{Servicio.objects.count()}</p>')
