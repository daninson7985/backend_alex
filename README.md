# Portal de Solicitudes y Servicios Municipales

Aplicación Django para publicar servicios municipales y consultar solicitudes ciudadanas. El proyecto conserva dos aplicaciones independientes, `solicitudesApp` y `serviciosApp`, y usa Django ORM para leer y guardar la información.

## Funcionalidades

- Inicio y navegación responsive con Bootstrap.
- Listados de solicitudes y servicios leídos desde la base de datos.
- Búsqueda por texto en ambos listados.
- Detalle de cada servicio con su categoría y requisitos.
- Administración CRUD, búsqueda y filtros desde Django Admin.
- Migraciones para crear la base de datos sin registros de ejemplo; los datos se ingresan desde Django Admin.

Los botones Agregar, Modificar y Eliminar de los listados enlazan a las pantallas correspondientes de Django Admin. Las operaciones de escritura se realizan desde ese panel.

## Aplicaciones y modelo de datos

| Aplicación | Entidad | Relación | Finalidad |
| --- | --- | --- | --- |
| `solicitudesApp` | `Solicitud` | Independiente | Registra nombre, estado, sector y descripción de cada solicitud. |
| `serviciosApp` | `Categoria` | Una categoría tiene muchos servicios | Clasifica los trámites y servicios municipales. |
| `serviciosApp` | `Servicio` | ForeignKey a `Categoria` | Describe el trámite, plazo, costo y categoría. |
| `serviciosApp` | `Requisito` | ForeignKey a `Servicio` | Almacena cada requisito como fila relacionada al servicio. |

Las cuatro entidades están registradas en Django Admin. Las migraciones viven en `solicitudesApp/migrations/` y `serviciosApp/migrations/`.

## Requisitos

- Python 3.12 o superior compatible con Django 6.1.
- Git.
- SQLite para desarrollo local y EC2. La base persistente está en `db.sqlite3`.

## Ejecución local

Desde la raíz del repositorio:

```powershell
git clone https://github.com/daninson7985/backend_alex.git
cd backend_alex
git switch main
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edita `.env` y reemplaza `SECRET_KEY` por un valor aleatorio. En desarrollo puedes usar `DEBUG=True`; Django usa SQLite y crea `db.sqlite3` automáticamente al aplicar las migraciones.

```powershell
python manage.py check
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Abre `http://127.0.0.1:8000/`, `http://127.0.0.1:8000/solicitudes/`, `http://127.0.0.1:8000/servicios/` y `http://127.0.0.1:8000/admin/`.

Las migraciones históricas `0002_datos_iniciales`, `0005_reponer_datos_iniciales` y `0007_reponer_datos_iniciales` cargaban registros de ejemplo. `0008_dejar_catalogos_vacios` los elimina para iniciar la evaluación con las tablas vacías y permite ingresar tus propios registros desde Admin. Esta limpieza se ejecuta una sola vez al migrar; los datos que agregues después no se borran al iniciar el servidor.

## Pruebas

```powershell
python manage.py test solicitudesApp serviciosApp
python manage.py makemigrations --check --dry-run
```

## Despliegue y evidencias

Consulta [DESPLIEGUE_EC2.md](DESPLIEGUE_EC2.md) para clonar el repositorio y ejecutar Django con SQLite en EC2. SQLite no es compatible con phpMyAdmin; usa `sqlite3` o DB Browser for SQLite para inspeccionar las tablas.

El borrador del entregable técnico con arquitectura, modelo de datos y espacios para las evidencias está en [DOCUMENTO_TECNICO.md](DOCUMENTO_TECNICO.md). Complétalo con tu nombre y capturas reales, y expórtalo a PDF o Word para entregar.

El repositorio no contiene `.env`, bases de datos locales ni credenciales. Las capturas de AWS, SQLite, GitHub y la instancia deben tomarse del entorno real durante el despliegue; no se incluyen evidencias simuladas.
