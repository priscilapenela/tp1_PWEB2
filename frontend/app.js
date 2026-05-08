const API_URL = "http://localhost:5000";
const { createApp } = Vue;

createApp({
  data() {
    return {
      productos: [],
      carrito: [],
      total: {
        total: 0,
        moneda: "ARS",
        cantidad_items: 0
      },
      cargando: true,
      mensaje: "",
      busqueda: "",
      toastTimeout: null,
      procesandoCompra: false
    };
  },

  computed: {
    productoDestacado() {
      return this.productos.length > 0 ? this.productos[0] : null;
    },

    productosFiltrados() {
      const texto = this.busqueda.trim().toLowerCase();

      if (!texto) {
        return this.productos;
      }

      return this.productos.filter((producto) =>
        producto.nombre.toLowerCase().includes(texto)
      );
    }
  },

  mounted() {
    this.cargarDatos();
  },

  methods: {
    async cargarDatos() {
      try {
        this.cargando = true;

        await Promise.all([
          this.cargarProductos(),
          this.cargarCarrito(),
          this.cargarTotal()
        ]);
      } catch (error) {
        console.error(error);
        this.mensaje = "Error al cargar los datos.";
      } finally {
        this.cargando = false;
      }
    },

    async cargarProductos() {
      const respuesta = await fetch(`${API_URL}/api/productos`);
      const data = await respuesta.json();
      this.productos = data;
    },

    async cargarCarrito() {
      const respuesta = await fetch(`${API_URL}/api/carrito`);
      const data = await respuesta.json();
      this.carrito = data;
    },

    async cargarTotal() {
      const respuesta = await fetch(`${API_URL}/api/carrito/total`);
      const data = await respuesta.json();
      this.total = data;
    },

    async agregarAlCarrito(productoId) {
      try {
        const respuesta = await fetch(`${API_URL}/api/carrito`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            id: productoId,
            cantidad: 1
          })
        });

        if (!respuesta.ok) {
          throw new Error("No se pudo agregar el producto.");
        }

        this.mostrarMensaje("Producto agregado al carrito 🍦");

        await this.cargarCarrito();
        await this.cargarTotal();
      } catch (error) {
        console.error(error);
        this.mostrarMensaje("Error al agregar el producto.");
      }
    },

    async eliminarDelCarrito(productoId) {
      try {
        const respuesta = await fetch(`${API_URL}/api/carrito/${productoId}`, {
          method: "DELETE"
        });

        if (!respuesta.ok) {
          throw new Error("No se pudo eliminar el producto.");
        }

        this.mostrarMensaje("Producto eliminado del carrito.");

        await this.cargarCarrito();
        await this.cargarTotal();
      } catch (error) {
        console.error(error);
        this.mostrarMensaje("Error al eliminar el producto.");
      }
    },

    formatearPrecio(precio) {
      return new Intl.NumberFormat("es-AR", {
        style: "currency",
        currency: "ARS",
        maximumFractionDigits: 0
      }).format(precio);
    },

    mostrarMensaje(texto) {
      this.mensaje = texto;

      if (this.toastTimeout) {
        clearTimeout(this.toastTimeout);
      }

      this.toastTimeout = setTimeout(() => {
        this.mensaje = "";
        this.toastTimeout = null;
      }, 3000);
    },

    async finalizarCompra() {
      if (this.carrito.length === 0) {
         this.mostrarMensaje("Tu carrito está vacío 🛍️");
         return;
      }

      try {
        this.procesandoCompra = true;
        this.mostrarMensaje("Procesando pedido... 🍦");

        await new Promise((resolve) => setTimeout(resolve, 1500));

        for (const item of this.carrito) {
          await fetch(`${API_URL}/api/carrito/${item.producto_id}`, {
            method: "DELETE"
           });
         }

         await this.cargarCarrito();
         await this.cargarTotal();

         this.mostrarMensaje("Compra finalizada con éxito 💗");
       } catch (error) {
         console.error(error);
         this.mostrarMensaje("Error al finalizar la compra.");
       } finally {
         this.procesandoCompra = false;
       }
     },

    getEmoji(id) {
      const emojis = {
        1: "🍦",
        2: "🍨",
        3: "🍧",
        4: "🧁",
        5: "🍫",
        6: "🍓"
      };

      return emojis[id] || "🍦";
    },

    getImagen(id) {
      const imagenes = {
        1: "./assets/vanilla.png",
        2: "./assets/strawberry.png",
        3: "./assets/blueberry.png",
        4: "./assets/chocolate.png"
      };

      return imagenes[id] || "./assets/vanilla.png";
    },

    getDescripcion(id) {
      const descripciones = {
        1: "Cremoso, suave y perfecto para cualquier momento.",
        2: "Dulce, fresco y con una textura irresistible.",
        3: "Frutal, colorido y súper refrescante.",
        4: "Chocolate intenso para verdaderos fanáticos."
      };

      return descripciones[id] || "Dulce, cremoso y delicioso.";
    }
  }
}).mount("#app");