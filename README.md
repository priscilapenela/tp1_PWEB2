# 🍦 Sweet Frost - SPA de Heladería

**Sweet Frost** es una aplicación web **Single Page Application** desarrollada para el trabajo práctico de **PWEB2**.

El proyecto está inspirado en la aplicación **Coffee Cart**, pero fue adaptado a una temática de **heladería artesanal** para darle una identidad visual más creativa, colorida y atractiva.

La aplicación permite visualizar productos, agregar productos al carrito, eliminar productos, calcular el total de la compra, finalizar un pedido simulado y mantener la persistencia de datos mediante una base SQLite.

---

## 📌 Objetivo del proyecto

El objetivo del trabajo práctico fue desarrollar una aplicación web SPA en dos etapas progresivas:

### Etapa 1 - Backend con APIs

En esta primera etapa se desarrolló un servidor backend que expone una API REST para gestionar productos y carrito de compras.

La API permite:

- listar productos disponibles;
- agregar productos al carrito;
- eliminar productos del carrito;
- calcular el total de la compra;
- documentar los endpoints con Swagger;
- validar los endpoints mediante tests unitarios.

### Etapa 2 - Frontend, base de datos y pruebas E2E

En la segunda etapa se incorporó:

- una interfaz web SPA;
- persistencia con base de datos SQLite;
- integración real entre frontend y backend;
- pruebas end-to-end con Playwright;
- preparación del proyecto para deploy.

---

## 🎨 Identidad visual

Aunque el enunciado propone una aplicación inspirada en Coffee Cart, se decidió cambiar la temática a una **tiendita de helados**.

La idea fue mantener la lógica de carrito de compras, pero darle una experiencia visual más creativa:

- colores pastel;
- estética cute;
- imágenes de helados;
- corazones decorativos;
- tarjetas redondeadas;
- mensajes tipo toast;
- diseño responsive;
- layout estilo landing e-commerce.

Esto busca mejorar la experiencia de usuario y aportar creatividad a la interfaz.

---

## 🧱 Arquitectura del proyecto

El proyecto está dividido en tres partes principales:

```txt
coffee_cart_tp/
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── requirements.txt
│   └── tests/
│       └── test_app.py
│
├── frontend/
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   └── assets/
│
├── e2e/
│   ├── package.json
│   ├── package-lock.json
│   ├── playwright.config.js
│   └── tests/
│       └── compra.spec.js
│
├── .gitignore
└── README.md
```

---

## 🧩 Descripción de cada carpeta

### `backend/`

Contiene la API REST desarrollada con Flask.

Se encarga de:

- exponer los endpoints;
- conectarse con SQLite;
- gestionar productos;
- gestionar el carrito;
- calcular totales;
- documentar la API;
- ejecutar tests unitarios.

Archivos principales:

```txt
backend/app.py
backend/database.py
backend/requirements.txt
backend/tests/test_app.py
```

---

### `frontend/`

Contiene la SPA desarrollada con HTML, CSS, JavaScript y Vue 3 por CDN.

Se encarga de:

- mostrar productos;
- consumir la API REST;
- agregar productos al carrito;
- eliminar productos;
- mostrar el total;
- finalizar una compra simulada;
- mostrar mensajes interactivos al usuario.

Archivos principales:

```txt
frontend/index.html
frontend/styles.css
frontend/app.js
frontend/assets/
```

---

### `e2e/`

Contiene las pruebas end-to-end desarrolladas con Playwright.

Estas pruebas validan el flujo completo de uso de la aplicación desde el navegador.

Archivo principal:

```txt
e2e/tests/compra.spec.js
```

---

## 🛠️ Tecnologías utilizadas

### Backend

| Tecnología | Uso |
|---|---|
| Python | Lenguaje principal del backend |
| Flask | Framework para crear la API REST |
| SQLite | Base de datos local |
| Flasgger / Swagger | Documentación interactiva de la API |
| Flask-CORS | Permitir comunicación entre frontend y backend |
| Pytest | Tests unitarios |
| Gunicorn | Servidor WSGI para deploy |

---

### Frontend

| Tecnología | Uso |
|---|---|
| HTML | Estructura de la aplicación |
| CSS | Diseño visual y responsive |
| JavaScript | Lógica del frontend |
| Vue 3 CDN | Reactividad y manejo de estado |
| Fetch API | Comunicación con el backend |

---

### Testing

| Herramienta | Uso |
|---|---|
| Pytest | Tests unitarios del backend |
| Playwright | Pruebas end-to-end del flujo completo |

---

### Deploy

| Plataforma | Uso |
|---|---|
| Render | Deploy del backend Flask |
| Netlify | Deploy del frontend estático |

---

## ⚙️ Funcionamiento general

La aplicación funciona con una arquitectura cliente-servidor.

```txt
Usuario
   ↓
Frontend SPA
   ↓ fetch
Backend Flask API
   ↓
SQLite
```

El usuario interactúa con el frontend.  
El frontend realiza peticiones HTTP al backend.  
El backend consulta o modifica los datos en SQLite.  
Luego devuelve una respuesta JSON que el frontend usa para actualizar la interfaz.

---

## 🗄️ Base de datos

La base de datos utilizada es **SQLite**.

Se eligió SQLite porque:

- no requiere servidor externo;
- es fácil de configurar;
- permite persistencia real;
- es suficiente para el alcance académico del proyecto;
- se integra fácilmente con Python.

La base se crea automáticamente al iniciar el backend mediante la función `init_db()`.

---

## 📋 Tablas principales

### Tabla `productos`

Guarda los productos disponibles.

| Campo | Tipo | Descripción |
|---|---|---|
| id | INTEGER | Identificador único del producto |
| nombre | TEXT | Nombre del producto |
| precio | REAL | Precio del producto |

---

### Tabla `carrito`

Guarda los productos agregados al carrito.

| Campo | Tipo | Descripción |
|---|---|---|
| id | INTEGER | Identificador del registro |
| producto_id | INTEGER | ID del producto agregado |
| cantidad | INTEGER | Cantidad agregada |

La tabla `carrito` se relaciona con la tabla `productos` mediante `producto_id`.

---

## 🔗 Endpoints disponibles

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/api/productos` | Lista todos los productos disponibles |
| GET | `/api/carrito` | Devuelve el carrito actual |
| POST | `/api/carrito` | Agrega un producto al carrito |
| DELETE | `/api/carrito/{producto_id}` | Elimina un producto del carrito |
| GET | `/api/carrito/total` | Calcula el total de la compra |

---

## 📘 Detalle de endpoints

### GET `/api/productos`

Devuelve la lista de productos disponibles.

Ejemplo de respuesta:

```json
[
  {
    "id": 1,
    "nombre": "Vanilla Dream",
    "precio": 1500
  },
  {
    "id": 2,
    "nombre": "Strawberry Bliss",
    "precio": 2000
  }
]
```

---

### GET `/api/carrito`

Devuelve el estado actual del carrito.

Ejemplo de respuesta:

```json
[
  {
    "id": 1,
    "producto_id": 1,
    "nombre": "Vanilla Dream",
    "precio": 1500,
    "cantidad": 2,
    "subtotal": 3000
  }
]
```

---

### POST `/api/carrito`

Agrega un producto al carrito.

Body esperado:

```json
{
  "id": 1,
  "cantidad": 1
}
```

Si el producto ya existe en el carrito, se actualiza la cantidad.  
Si no existe, se agrega como nuevo ítem.

Respuesta esperada:

```json
{
  "mensaje": "Producto agregado al carrito"
}
```

---

### DELETE `/api/carrito/{producto_id}`

Elimina un producto del carrito.

Ejemplo:

```txt
DELETE /api/carrito/1
```

Respuesta esperada:

```json
{
  "mensaje": "Producto eliminado del carrito"
}
```

---

### GET `/api/carrito/total`

Calcula el total de la compra.

Ejemplo de respuesta:

```json
{
  "total": 3000,
  "moneda": "ARS",
  "cantidad_items": 2
}
```

---

## 📄 Documentación Swagger

La API cuenta con documentación interactiva generada con **Swagger / Flasgger**.

Para acceder, primero se debe levantar el backend y luego abrir:

```txt
http://localhost:5000/apidocs
```

Desde Swagger se pueden probar los endpoints directamente desde el navegador.

---

## 💻 Ejecución local

### 1. Clonar el repositorio

```bash
git clone URL_DEL_REPOSITORIO
cd coffee_cart_tp
```

---

## ▶️ Ejecutar backend

Entrar a la carpeta del backend:

```bash
cd backend
```

Crear entorno virtual:

```bash
python -m venv venv
```

Activar entorno virtual en Windows:

```bash
venv\Scripts\activate
```

Activar entorno virtual en Linux/Mac:

```bash
source venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar servidor:

```bash
python app.py
```

El backend queda disponible en:

```txt
http://localhost:5000
```

Swagger queda disponible en:

```txt
http://localhost:5000/apidocs
```

---

## 🌐 Ejecutar frontend

En otra terminal, desde la raíz del proyecto:

```bash
cd frontend
python -m http.server 5500
```

El frontend queda disponible en:

```txt
http://localhost:5500
```

---

## ✅ Tests unitarios del backend

Los tests unitarios están ubicados en:

```txt
backend/tests/test_app.py
```

Para ejecutarlos:

```bash
cd backend
venv\Scripts\activate
python -m pytest
```

Los tests unitarios validan:

- listado de productos;
- obtención del carrito vacío;
- agregado de productos al carrito;
- validación de producto inexistente;
- validación de cantidad inválida;
- cálculo del total;
- eliminación de productos;
- eliminación de producto inexistente.

Resultado esperado:

```txt
8 passed
```

---

## 🧪 Pruebas E2E

Las pruebas E2E fueron realizadas con **Playwright**.

Se encuentran en:

```txt
e2e/tests/compra.spec.js
```

Antes de ejecutarlas, deben estar levantados:

```txt
Backend: http://localhost:5000
Frontend: http://localhost:5500
```

Luego, desde la carpeta `e2e`:

```bash
cd e2e
npm install
npm test
```

También se pueden ejecutar con navegador visible:

```bash
npm run test:headed
```

Y ver el reporte con:

```bash
npm run report
```

---

## 🔍 Qué validan las pruebas E2E

La prueba principal valida el flujo real de compra:

1. El usuario ingresa al sitio.
2. El frontend carga correctamente.
3. Se visualizan los productos disponibles.
4. Se agrega un producto al carrito.
5. El producto aparece en el carrito.
6. Se recarga la página.
7. El producto sigue en el carrito, validando persistencia.
8. Se finaliza la compra.
9. El carrito queda vacío.

Estas pruebas validan:

- flujo de compra completo;
- persistencia de datos;
- correcta interacción entre frontend y backend.

---

## 🔄 Persistencia de datos

La persistencia se valida de dos maneras:

### Desde la aplicación

Cuando el usuario agrega un producto al carrito y recarga la página, el producto sigue apareciendo.

Esto demuestra que el estado no está solamente en el frontend, sino que se guarda en la base SQLite.

### Desde las pruebas E2E

El test agrega un producto, recarga la página y verifica que el producto siga en el carrito.

---

## 🚀 Deploy

El proyecto está preparado para deploy en plataformas accesibles.

### Backend - Render

Configuración recomendada:

```txt
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

URL del backend:

```txt
LINK_BACKEND
```

---

### Frontend - Netlify

Como el frontend es estático, se puede desplegar directamente la carpeta `frontend`.

URL del frontend:

```txt
LINK_FRONTEND
```

---

## ⚠️ Configuración importante para producción

En desarrollo, el frontend consume la API local:

```js
const API_URL = "http://localhost:5000";
```

Para producción, se debe cambiar por la URL del backend desplegado:

```js
const API_URL = "https://mi-backend.onrender.com";
```

---

## 🧠 Decisiones de diseño y desarrollo

### Uso de Vue por CDN

Se utilizó Vue 3 por CDN porque permite construir una SPA sin necesidad de herramientas de build como Vite.

Esto simplifica la ejecución del frontend, ya que solo se necesita servir archivos estáticos.

---

### Uso de SQLite

SQLite fue elegido por su simplicidad.  
Para el alcance del TP, permite demostrar persistencia sin requerir configuración adicional de servidores de base de datos.

---

### Separación en carpetas

El proyecto se dividió en `backend`, `frontend` y `e2e` para separar responsabilidades y facilitar la comprensión del código.

---

### Estética de heladería

Se decidió transformar la idea original de Coffee Cart en una heladería para mejorar la creatividad de la interfaz y la experiencia visual.

---

## 🧩 Dificultades encontradas y soluciones

### 1. Migración de memoria a SQLite

Al principio, el backend manejaba los productos y el carrito con listas en memoria.  
Esto era suficiente para una primera etapa, pero los datos se perdían al reiniciar el servidor.

Para solucionarlo, se implementó SQLite y se migraron los endpoints para que consulten y modifiquen la base de datos.

---

### 2. Creación automática de la base

En un primer momento, el archivo `heladitos.db` no se creaba automáticamente.

La solución fue llamar a `init_db()` al iniciar la aplicación Flask.  
De esta forma, la base y las tablas se crean automáticamente si no existen.

---

### 3. Productos iniciales no actualizados

Al modificar los productos iniciales, los cambios no se veían reflejados si la base ya existía.

Se resolvió utilizando `INSERT OR IGNORE`, evitando duplicados y permitiendo cargar productos iniciales de manera segura.

---

### 4. Problemas de CORS

El frontend y el backend corren en puertos distintos durante el desarrollo:

```txt
Frontend: http://localhost:5500
Backend: http://localhost:5000
```

Esto podía bloquear las peticiones entre ambos.

Se resolvió agregando `Flask-CORS` al backend.

---

### 5. Sincronización del carrito

Después de agregar o eliminar productos, el frontend debía actualizar el carrito y el total.

Se resolvió haciendo nuevas peticiones a:

```txt
/api/carrito
/api/carrito/total
```

después de cada acción.

---

### 6. Tests E2E con datos persistentes

Como SQLite mantiene los datos entre ejecuciones, los tests podían fallar si el carrito no estaba vacío al comenzar.

Se resolvió limpiando el carrito antes de cada test E2E mediante llamadas a la API.

---

### 7. Diseño y usabilidad

La interfaz fue evolucionando desde una versión simple hacia una landing e-commerce más cuidada.

Se eliminaron elementos que no aportaban funcionalidad, como filtros no implementados, y se agregaron detalles visuales como imágenes, corazones decorativos y mensajes toast.

---

## 👤 Autor: Priscila Penela

Trabajo práctico desarrollado para la materia **PWEB2**.