# Despliegue de la evaluación en AWS EC2 con SQLite

Esta guía instala el proyecto de GitHub en una instancia Ubuntu EC2 y utiliza SQLite, igual que la configuración local de Django. SQLite guarda todas las tablas en el archivo `db.sqlite3`; no requiere instalar ni configurar MariaDB/MySQL. phpMyAdmin no sirve para SQLite: para inspeccionar las tablas usa `sqlite3` o DB Browser for SQLite.

No publiques `.env`, `db.sqlite3`, contraseñas ni llaves `.pem` en GitHub.

## 1. Crear y conectar la instancia

Usa una instancia Ubuntu LTS. En su grupo de seguridad permite:

- TCP 22 solo desde tu IP para SSH.
- TCP 8000 desde tu IP y la del revisor mientras haces la demostración. `0.0.0.0/0` permite acceso desde cualquier dirección; evita dejarlo abierto después.

Conéctate desde tu computador:

```powershell
ssh -i "C:\ruta\a\tu-llave.pem" ubuntu@IP_PUBLICA
```

## 2. Instalar Python, Git y clonar `main`

En la terminal SSH de EC2:

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip
git clone --branch main https://github.com/daninson7985/backend_alex.git
cd backend_alex
git remote -v
git log --oneline -5
```

El repositorio es público; para clonarlo por HTTPS no necesitas configurar un token personal de GitHub.

## 3. Crear el entorno virtual e instalar Django

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python --version
python -m django --version
```

## 4. Configurar Django

Genera una `SECRET_KEY` nueva y crea el archivo `.env`:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
cp .env.example .env
chmod 600 .env
nano .env
```

Configura las variables. Sustituye la IP y la clave secreta por los valores reales:

```env
SECRET_KEY=PEGA_AQUI_LA_CLAVE_ALEATORIA
DEBUG=False
ALLOWED_HOSTS=IP_PUBLICA_EC2
CSRF_TRUSTED_ORIGINS=
```

Guarda en `nano` con **Ctrl+O**, Enter, y sal con **Ctrl+X**. Si usas un dominio con HTTPS, agrega su origen completo, por ejemplo `https://ejemplo.cl`, a `CSRF_TRUSTED_ORIGINS`.

## 5. Crear y verificar la base SQLite

Desde la raíz del repositorio y con el entorno virtual activo:

```bash
python manage.py check
python manage.py showmigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

La base de datos queda en `db.sqlite3`. La migración `serviciosApp.0008_dejar_catalogos_vacios` deja vacías las cuatro tablas del dominio durante la instalación para que puedas ingresar categorías, servicios, requisitos y solicitudes desde Django Admin. Se ejecuta una sola vez: no vuelvas a eliminar el archivo de base de datos después de crear registros.

Para comprobar que las tablas existen:

```bash
python manage.py dbshell
```

En la consola SQLite que se abre:

```sql
.tables
SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name;
```

La instancia Ubuntu necesita el paquete `sqlite3` para abrir la consola mediante `dbshell`. Si no está instalado:

```bash
sudo apt install -y sqlite3
```

También puedes consultar conteos desde Django:

```bash
python manage.py shell -c "from solicitudesApp.models import Solicitud; from serviciosApp.models import Categoria, Servicio, Requisito; print('solicitudes:', Solicitud.objects.count(), 'categorias:', Categoria.objects.count(), 'servicios:', Servicio.objects.count(), 'requisitos:', Requisito.objects.count())"
```

Para ver visualmente el archivo `db.sqlite3`, descárgalo a tu computador y ábrelo con DB Browser for SQLite. No necesitas phpMyAdmin.

## 6. Ejecutar el sitio para la demostración

```bash
python manage.py runserver --insecure 0.0.0.0:8000
```

Deja la sesión SSH y el proceso abiertos durante la demostración. Visita:

- `http://IP_PUBLICA_EC2:8000/`
- `http://IP_PUBLICA_EC2:8000/solicitudes/`
- `http://IP_PUBLICA_EC2:8000/servicios/`
- `http://IP_PUBLICA_EC2:8000/admin/`

Inicia sesión en `/admin/` con el superusuario creado y agrega allí los registros.

`runserver --insecure` es únicamente para la evaluación/demostración, no para un despliegue de producción permanente. Para producción se recomienda Gunicorn detrás de Nginx y un servicio `systemd`.

## 7. Actualizar el código en EC2

Cuando publiques cambios en GitHub, actualiza el código sin borrar la base SQLite:

```bash
cd ~/backend_alex
git pull origin main
source venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Detén Django con **Ctrl+C** y vuelve a ejecutar `runserver` para cargar el nuevo código. Haz una copia de seguridad de `db.sqlite3` antes de cambios importantes; nunca reemplaces la base por un archivo vacío si deseas conservar tus registros.

## 8. Evidencias para la revisión

Captura evidencia real y legible de:

- Instancia EC2, conexión SSH, entorno virtual y sistema Linux.
- Clonación, `git remote -v`, rama `main` e historial de commits.
- `python manage.py showmigrations` con las migraciones aplicadas.
- Sitio respondiendo desde la IP pública y operaciones en Django Admin.
- Tablas y registros en `db.sqlite3`, usando `sqlite3`, `dbshell` o DB Browser for SQLite.

No incluyas `.env`, contraseñas, llaves privadas ni datos personales en las capturas.
