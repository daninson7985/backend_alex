# Documento técnico

## Portal de Solicitudes y Servicios Municipales

**Evaluación:** Aplicación Django con persistencia relacional
**Repositorio:** [daninson7985/backend_alex](https://github.com/daninson7985/backend_alex)
**Rama de esta evaluación:** `evaluacion-django`
**Estudiante:** Completar con nombre
**Fecha de revisión:** Completar

> Este documento describe la implementación del repositorio. Las capturas marcadas como pendientes deben obtenerse del despliegue real; no se presentan imágenes simuladas como evidencia.

## 1. Descripción del proyecto

El portal permite consultar solicitudes ciudadanas y trámites municipales de La Serena. La solución conserva dos aplicaciones Django independientes y cambia la lectura de información desde archivos a consultas realizadas mediante Django ORM sobre una base de datos relacional.

### Objetivo

Persistir y administrar la información de solicitudes y servicios desde Django Admin, y presentarla al usuario en plantillas HTML con navegación y componentes Bootstrap.

### Funcionalidades implementadas

- Página de inicio con totales de solicitudes y servicios consultados desde la base.
- Listado de solicitudes y búsqueda por nombre, estado, sector o descripción.
- Catálogo de servicios y búsqueda por nombre, categoría o descripción.
- Detalle de servicio con su categoría y requisitos relacionados.
- Administración CRUD, filtros y búsqueda en Django Admin para las cuatro entidades.
- Controles Agregar, Modificar, Eliminar y Buscar en los listados; las operaciones de escritura se administran desde Django Admin.
- Migraciones para crear el esquema; los registros se ingresan desde Django Admin.

## 2. Arquitectura

El repositorio contiene un único proyecto Django (`config`) y las siguientes aplicaciones:

| Componente | Responsabilidad |
| --- | --- |
| `config/` | Configuración, URLs y puntos de entrada WSGI/ASGI del proyecto. |
| `solicitudesApp/` | Modelo, administración, consultas, rutas, pruebas y migraciones de solicitudes ciudadanas. |
| `serviciosApp/` | Modelos, administración, consultas, rutas, pruebas y migraciones de servicios, categorías y requisitos. |
| `templates/` | Plantillas compartidas renderizadas por Django. |
| `static/` | Bootstrap, imágenes y JavaScript estáticos. |
| `manage.py` | Comandos Django para verificar, migrar, probar y ejecutar el proyecto. |

En desarrollo se utiliza SQLite. Para el despliegue descrito en `DESPLIEGUE_EC2.md` se puede configurar MySQL/MariaDB con variables de entorno y verificar las tablas desde phpMyAdmin.

## 3. Modelo de datos

| Tabla Django | Entidad | Relación | Uso |
| --- | --- | --- | --- |
| `solicitudesApp_solicitud` | `Solicitud` | Sin relación con otras entidades | Guarda el nombre, estado, sector y descripción de una solicitud. |
| `serviciosApp_categoria` | `Categoria` | Uno a muchos con `Servicio` | Agrupa trámites por categoría. |
| `serviciosApp_servicio` | `Servicio` | ForeignKey a `Categoria` | Guarda descripción, días hábiles, costo y categoría de un servicio. |
| `serviciosApp_requisito` | `Requisito` | ForeignKey a `Servicio` | Guarda cada requisito asociado a un servicio. |

Las relaciones usan `ForeignKey` con borrado en cascada para que los servicios pertenezcan a una categoría y los requisitos a un servicio. Django Admin muestra servicios dentro de su categoría y requisitos dentro del servicio correspondiente.

Las migraciones están en `solicitudesApp/migrations/` y `serviciosApp/migrations/`. Hay migraciones históricas de datos de ejemplo; `0008_dejar_catalogos_vacios` deja vacías las cuatro tablas del dominio una única vez, para que el administrador ingrese los registros propios desde Admin. Las migraciones se aplican antes de ingresar esos datos.

## 4. Instalación y ejecución local

Desde la raíz del repositorio:

```powershell
git clone https://github.com/daninson7985/backend_alex.git
cd backend_alex
git switch evaluacion-django
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edita `.env` para asignar una clave secreta propia. Para SQLite local usa `DB_USE_MYSQL=0`; `DEBUG=True` permite ejecutar la página con `python manage.py runserver`.

```powershell
python manage.py check
python manage.py migrate
python manage.py createsuperuser
python manage.py test solicitudesApp serviciosApp
python manage.py runserver
```

Rutas principales: `/`, `/solicitudes/`, `/servicios/`, `/acerca/` y `/admin/`.

## 5. Variables de entorno

Las variables están documentadas en `.env.example`; el archivo `.env` real está excluido de Git:

| Variable | Uso |
| --- | --- |
| `SECRET_KEY` | Clave secreta única de Django; no compartir ni versionar. |
| `DEBUG` | Activar solo durante desarrollo local. |
| `ALLOWED_HOSTS` | IP o dominios permitidos para servir Django. |
| `CSRF_TRUSTED_ORIGINS` | Orígenes completos de confianza si se usa HTTPS/proxy. |
| `DB_USE_MYSQL` | `1` usa MySQL; `0` usa SQLite. |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` | Conexión MySQL/MariaDB. |

## 6. Despliegue y evidencias de revisión

Los pasos para crear una instancia Linux EC2, instalar Python y Git, clonar el repositorio, configurar MySQL/MariaDB, migrar y ejecutar Django están en `DESPLIEGUE_EC2.md`.

Completar esta sección con capturas reales del entorno desplegado:

1. **AWS EC2 y Linux:** `[PENDIENTE: captura de la instancia y terminal SSH]`
2. **Clonación e historial Git:** `[PENDIENTE: captura de git remote -v, rama y git log]`
3. **Entorno y migraciones:** `[PENDIENTE: captura de venv, python --version, showmigrations y migrate]`
4. **Aplicación en EC2:** `[PENDIENTE: captura del sitio y sus listados en el navegador]`
5. **Django Admin:** `[PENDIENTE: capturas de entidades y operaciones CRUD]`
6. **phpMyAdmin:** `[PENDIENTE: capturas de tablas, relaciones y registros]`

No incluir contraseñas, `.env`, llaves privadas ni datos personales en las capturas. Para generar el entregable PDF, abre este Markdown en el editor o visor que uses, imprímelo/exporta a PDF y agrega las capturas reales en los espacios anteriores.

## 7. Evidencia de uso de IA

Registrar evidencia del trabajo realizado con IA, contrastándola con el historial real de la conversación:

- **Solicitud inicial:** aplicar la pauta de evaluación completa al proyecto Django compartido y mantener el contenido únicamente en el repositorio `backend_alex`.
- **Solicitud de seguimiento:** revisar si faltan requisitos y agregarlos.
- **Respuesta aplicada al código:** depuración del árbol del proyecto; actualización de la documentación y configuración para EC2/MySQL; protección de migraciones frente a borrado de datos; datos iniciales idempotentes; navegación a entidades relacionadas en Admin; y pruebas para listados, búsquedas y enlaces de administración.
- **Limitación informada:** la instancia EC2, las capturas reales y la verificación final de ejecución requieren acceso al entorno AWS y un intérprete Python funcional.

Agregar capturas de los prompts y respuestas desde la herramienta de IA utilizada durante el desarrollo: `[PENDIENTE: evidencia de la conversación]`.
