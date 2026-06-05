# VetAPI

API REST para la gestión integral de una clínica veterinaria, desarrollada con **Django**, **Django REST Framework**, **PostgreSQL** y autenticación **JWT**. El sistema permite administrar usuarios, mascotas, servicios, inventario clínico, vacunas y tickets de atención bajo un modelo de control de acceso basado en roles (RBAC).

---

# Características Principales

* Autenticación y autorización mediante JWT.
* Gestión de usuarios con roles.
* CRUD completo para todas las entidades principales.
* Gestión de mascotas e historial clínico.
* Control de inventario e insumos veterinarios.
* Registro y seguimiento de vacunas.
* Sistema de tickets de atención veterinaria.
* Filtros, búsqueda, ordenamiento y paginación.
* Estadísticas por módulo.
* API REST lista para integrarse con aplicaciones web o móviles.

---

# Arquitectura de Roles

| Rol           | Alcance     | Permisos Principales                                                         |
| ------------- | ----------- | ---------------------------------------------------------------------------- |
| Administrador | Total       | Gestión de usuarios, auditoría, configuración y control general del sistema. |
| Veterinario   | Clínico     | Gestión de mascotas, vacunas, insumos, servicios y tickets de atención.      |
| Cliente       | Autogestión | Consulta de mascotas y seguimiento de atenciones.                            |

---

# Requisitos Cubiertos

* Django conectado a PostgreSQL.
* Django REST Framework para toda la API.
* Modelos y serializers para las entidades del proyecto.
* CRUD completo para usuarios, servicios, ítems clínicos, tickets de atención, mascotas y vacunas.
* Filtros, búsqueda y paginación.
* Autenticación JWT con login, refresh, verify y logout.
* Permisos para usuarios normales, veterinarios y administradores.

---

# Tecnologías

* Django
* Django REST Framework
* Django Filter
* Simple JWT
* PostgreSQL
* CORS Headers
* uv

---

# Estructura del Proyecto

```text
vetapi/
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── veterinaria/
│   ├── models/
│   ├── serializers/
│   ├── views/
│   ├── permissions/
│   ├── migrations/
│   └── urls.py
│
├── postman/
├── tests/
├── manage.py
├── pyproject.toml
└── README.md
```

---

# Módulos de la API

| Módulo              | Funcionalidades                                           |
| ------------------- | --------------------------------------------------------- |
| Auth                | Login, registro, refresh, verify y logout mediante JWT.   |
| Usuarios            | Gestión de perfiles, roles y administración de usuarios.  |
| Mascotas            | Registro, historial médico y asociación con propietarios. |
| Servicios           | Catálogo de servicios veterinarios y costos base.         |
| Items Clínicos      | Inventario, stock y control de insumos médicos.           |
| Vacunas             | Registro de dosis, fechas y próximos refuerzos.           |
| Tickets de Atención | Diagnósticos, tratamientos, uso de insumos y facturación. |

---

# Gestión de Costos

El sistema calcula automáticamente el costo total de una atención veterinaria mediante la siguiente fórmula:

```text
Total Ticket =
Precio Servicio Base
+ Σ(Costo de Insumos Utilizados)
+ Σ(Precio de Vacunas Aplicadas)
```

---

# Instalación

## 1. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=tu_clave_secreta
DEBUG=True

ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=vetapi
DB_USER=postgres
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432

CORS_ALLOW_ALL_ORIGINS=True
```

## 2. Instalar dependencias y aplicar migraciones

```bash
uv sync
uv run python manage.py migrate
```

## 3. Crear superusuario (opcional)

```bash
uv run python manage.py createsuperuser
```

## 4. Ejecutar el servidor

```bash
uv run python manage.py runserver
```

Servidor disponible en:

```text
http://127.0.0.1:8000/
```

---

# Autenticación

La API utiliza JWT.

## Endpoints de autenticación

| Método | Endpoint                 |
| ------ | ------------------------ |
| POST   | /api/auth/login/         |
| POST   | /api/auth/register/      |
| POST   | /api/auth/token/refresh/ |
| POST   | /api/auth/token/verify/  |
| POST   | /api/auth/logout/        |

Después del login o registro, utilizar el token de acceso en cada petición protegida:

```http
Authorization: Bearer <access_token>
```

Para probar todas las funcionalidades administrativas se recomienda utilizar una cuenta con rol `VET` o `ADMIN`.

---

# Recursos Expuestos

* `/api/users/`
* `/api/servicios/`
* `/api/items-clinicos/`
* `/api/tickets-atencion/`
* `/api/mascotas/`
* `/api/vacunas/`

---

# Filtros y Búsqueda

La API incluye:

* Búsquedas mediante `search`.
* Filtros por rol, estado, especie, mascota, fechas, precios y stock.
* Ordenamiento configurable.
* Paginación global.

---

# Acciones Adicionales

## Usuarios

* `GET /api/users/profile/`
* `PATCH /api/users/profile/`
* `POST /api/users/change-password/`
* `POST /api/users/{id}/toggle-active/`
* `GET /api/users/stats/`

## Items Clínicos

* `GET /api/items-clinicos/available/`
* `POST /api/items-clinicos/{id}/restock/`
* `GET /api/items-clinicos/stats/`

## Servicios

* `GET /api/servicios/stats/`

## Tickets de Atención

* `POST /api/tickets-atencion/{id}/add-item/`
* `POST /api/tickets-atencion/{id}/confirm/`
* `POST /api/tickets-atencion/{id}/update-status/`
* `GET /api/tickets-atencion/stats/`

## Mascotas

* `GET /api/mascotas/{id}/vacunas/`
* `GET /api/mascotas/stats/`

## Vacunas

* `GET /api/vacunas/stats/`

---

# Colección de Postman

Importa la colección incluida en:

```text
postman/veterinaria-api.postman_collection.json
```

Incluye:

* Login y registro.
* Gestión automática de tokens JWT.
* CRUD completo de todas las entidades.
* Filtros y búsquedas.
* Acciones personalizadas del sistema.

---

# Pruebas

Ejecutar pruebas automatizadas:

```bash
uv run python manage.py test
```

---

# Dependencias

El proyecto utiliza **uv** para la gestión de dependencias.

Toda la configuración se encuentra en:

```text
pyproject.toml
```

No es necesario utilizar `requirements.txt` mientras se trabaje con `uv`.

---

# Autor

Proyecto académico desarrollado para la gestión de clínicas veterinarias utilizando Django, PostgreSQL y Django REST Framework.
