# Sweet Frost - SPA de Heladería

Sweet Frost es una aplicación web Single Page Application desarrollada para el TP de PWEB2. La aplicación está inspirada en Coffee Cart, pero adaptada a una temática de heladería.

Permite visualizar productos, agregar y eliminar productos del carrito, calcular el total de la compra y finalizar un pedido simulado. El proyecto incluye backend con API REST, frontend SPA, persistencia en base de datos SQLite, documentación Swagger, tests unitarios y pruebas E2E.

---

## Tecnologías utilizadas

### Backend

- Python
- Flask
- SQLite
- Flasgger / Swagger
- Flask-CORS
- Pytest
- Gunicorn

### Frontend

- HTML
- CSS
- JavaScript
- Vue 3 por CDN

### Testing

- Pytest para tests unitarios del backend
- Playwright para pruebas E2E

### Deploy

- Backend: Render
- Frontend: Netlify

---

## Estructura del proyecto

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
│   ├── playwright.config.js
│   └── tests/
│       └── compra.spec.js
│
├── .gitignore
└── README.md