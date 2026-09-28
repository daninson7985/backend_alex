# Despliegue de la evaluación en AWS EC2

Esta guía despliega el proyecto de este repositorio (`backend_alex`, rama `evaluacion-django`) en una instancia Linux. La configuración usa MySQL/MariaDB en EC2 para que las tablas puedan inspeccionarse desde phpMyAdmin. No publiques el archivo `.env`, contraseñas, llaves `.pem` ni la base de datos.

## 1. Crear y conectar la instancia

Usa una instancia Ubuntu LTS con Python, Git y acceso SSH. En el grupo de seguridad permite:

- TCP 22 solo desde tu IP para SSH.
- TCP 80 solo desde la IP del docente/revisor para phpMyAdmin.
- TCP 8000 solo desde la IP del docente/revisor durante la demostración.

Conéctate desde tu computador:

```bash
ssh -i RUTA_DE_LA_LLAVE.pem ubuntu@IP_PUBLICA
```

## 2. Instalar paquetes del sistema y clonar el repositorio

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip python3-dev build-essential pkg-config libmariadb-dev mariadb-server apache2 php php-mysql php-mbstring php-zip php-gd phpmyadmin
git clone --branch evaluacion-django https://github.com/daninson7985/backend_alex.git
cd backend_alex
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

El historial y la clonación se pueden demostrar con:

```bash
git remote -v
git log --oneline -5
```

## 3. Crear la base MySQL/MariaDB

Abre la consola de MariaDB:

```bash
sudo mariadb
```

Crea una base y un usuario propios. Reemplaza la contraseña de ejemplo por una segura:

```sql
CREATE DATABASE evaluacion CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'evaluacion_user'@'localhost' IDENTIFIED BY 'REEMPLAZAR_POR_UNA_CLAVE_SEGURA';
GRANT ALL PRIVILEGES ON evaluacion.* TO 'evaluacion_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

Durante la instalación de phpMyAdmin selecciona Apache2 cuando el instalador pregunte qué servidor web configurar. Si la selección no aparece, habilita la configuración de Apache para phpMyAdmin y reinicia Apache:

```bash
sudo phpenmod mbstring
sudo systemctl restart apache2
```

Ingresa a `http://IP_PUBLICA/phpmyadmin` con el usuario MariaDB creado arriba. Mantén el puerto 80 restringido al IP del revisor; no expongas phpMyAdmin a todo Internet.

## 4. Configurar variables de entorno

Crea `.env` en la raíz del repositorio. No lo subas a GitHub:

```bash
cp .env.example .env
chmod 600 .env
nano .env
```

Configura valores reales:

```env
SECRET_KEY=REEMPLAZAR_POR_UN_SECRETO_ALEATORIO
DEBUG=False
ALLOWED_HOSTS=IP_PUBLICA_O_DOMINIO
CSRF_TRUSTED_ORIGINS=
DB_USE_MYSQL=1
DB_NAME=evaluacion
DB_USER=evaluacion_user
DB_PASSWORD=REEMPLAZAR_POR_LA_CLAVE_MYSQL
DB_HOST=127.0.0.1
DB_PORT=3306
```

Genera una clave Django aleatoria sin reutilizar el valor de ejemplo:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Si usas HTTPS, agrega el origen completo a `CSRF_TRUSTED_ORIGINS`, por ejemplo `https://ejemplo.cl`. `ALLOWED_HOSTS` recibe nombres de host/IP sin esquema ni puerto.

## 5. Migrar y verificar

Con el entorno virtual activo y `.env` configurado:

```bash
python manage.py check
python manage.py showmigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

En phpMyAdmin selecciona la base `evaluacion`. Deben aparecer las tablas de Django y las tablas de las entidades: `solicitudesApp_solicitud`, `serviciosApp_categoria`, `serviciosApp_servicio` y `serviciosApp_requisito`. Confirma las relaciones `Servicio -> Categoria` y `Requisito -> Servicio`.

La migración `serviciosApp.0008_dejar_catalogos_vacios` deja vacías las tablas del dominio para que ingreses las categorías, servicios, requisitos y solicitudes desde `/admin/`. Comprueba que esté aplicada con `python manage.py showmigrations serviciosApp solicitudesApp`. No uses archivos JSON con sesiones o usuarios exportados.

## 6. Ejecutar para la demostración

Para la revisión presencial, ejecuta Django enlazado a la interfaz de red de la instancia:

```bash
python manage.py runserver --insecure 0.0.0.0:8000
```

Abre `http://IP_PUBLICA:8000/`, `/solicitudes/`, `/servicios/` y `/admin/`. Mantén abierta la terminal para demostrar el entorno virtual, las migraciones y los registros.

La opción `--insecure` permite servir los archivos estáticos durante la demostración aunque `DEBUG=False`. `runserver` y `--insecure` son solo para desarrollo/revisión, no para producción permanente. Para producción real usa un servidor WSGI como Gunicorn detrás de Nginx y un servicio `systemd`.

## 7. Evidencias para la revisión

Captura evidencia real y legible de:

- Instancia EC2, sistema Linux, conexión SSH y proyecto clonado.
- `git remote -v`, historial de commits y rama desplegada.
- Entorno virtual activo, `python --version`, Django y `showmigrations`.
- Sitio respondiendo desde EC2 y administración Django.
- Creación, búsqueda, modificación y eliminación desde Django Admin.
- Tablas, relaciones y registros en phpMyAdmin.

No incluyas contraseñas, claves privadas, `.env` ni información personal en las capturas.
