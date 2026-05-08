const { test, expect } = require("@playwright/test");

const FRONTEND_URL = "http://localhost:5500";
const BACKEND_URL = "http://localhost:5000";

async function limpiarCarrito(request) {
  const response = await request.get(`${BACKEND_URL}/api/carrito`);
  const carrito = await response.json();

  for (const item of carrito) {
    await request.delete(`${BACKEND_URL}/api/carrito/${item.producto_id}`);
  }
}

test.beforeEach(async ({ request }) => {
  await limpiarCarrito(request);
});

test("flujo completo de compra", async ({ page }) => {
  await page.goto(FRONTEND_URL);

  await expect(page.getByRole("link", { name: /Sweet Frost/ })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Sabores destacados" })).toBeVisible();

  const carrito = page.locator("#carrito");

  await expect(carrito.getByText("Tu carrito está vacío")).toBeVisible();

  const primerProducto = page.locator(".product-card").first();
  const nombreProducto = await primerProducto.locator("h3").innerText();

  await primerProducto.getByRole("button", { name: "Agregar" }).click();

  await expect(page.locator(".toast")).toContainText(/agregado al carrito/i);

  await expect(carrito.getByRole("heading", { name: "Carrito", exact: true })).toBeVisible();
  await expect(carrito.getByText(nombreProducto)).toBeVisible();

  await page.reload();

  const carritoDespuesDeRecargar = page.locator("#carrito");

  await expect(carritoDespuesDeRecargar.getByText(nombreProducto)).toBeVisible();

  await page.getByRole("button", { name: "Finalizar compra" }).click();

  await expect(page.getByRole("button", { name: /Procesando pedido/i })).toBeVisible();

  await expect(page.locator(".toast")).toContainText(/Compra finalizada/i);

  await expect(page.locator("#carrito").getByText("Tu carrito está vacío")).toBeVisible();
});