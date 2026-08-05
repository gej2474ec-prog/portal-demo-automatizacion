# -*- coding: utf-8 -*-
"""
PORTAL DEMO  ·  Automatización
==============================
Copia de MUESTRA del portal, con datos 100% INVENTADOS y marca propia.
No usa ningún dato real. Sirve para enseñárselo a clientes potenciales.

Para correrlo:  doble clic en  "INICIAR DEMO.cmd"
"""
import os
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "logo.png")
NEGOCIO_DEMO = "Tienda Demo"      # nombre inventado de ejemplo

st.set_page_config(
    page_title="Portal · Automatización (DEMO)",
    page_icon=LOGO if os.path.exists(LOGO) else "⚡",
    layout="wide",
    initial_sidebar_state="auto",
)

# --------------------------------------------------------------------------- #
# Bloquear zoom (pellizco en celular, doble toque y Ctrl+rueda en PC)
# --------------------------------------------------------------------------- #
def bloquear_zoom() -> None:
    # El componente vive en un iframe, pero alcanzamos la pagina real con
    # window.parent para fijar el viewport y frenar los gestos de zoom.
    components.html(
        """
        <script>
        (function () {
          const doc = window.parent.document;

          // 1) Viewport: impide el pellizco para hacer zoom en moviles.
          let meta = doc.querySelector('meta[name="viewport"]');
          if (!meta) {
            meta = doc.createElement('meta');
            meta.name = 'viewport';
            doc.head.appendChild(meta);
          }
          meta.setAttribute(
            'content',
            'width=device-width, initial-scale=1.0, maximum-scale=1.0, ' +
            'minimum-scale=1.0, user-scalable=no'
          );

          // 2) touch-action: evita el zoom por doble toque.
          const st = doc.createElement('style');
          st.textContent = 'html,body{touch-action:manipulation;}';
          doc.head.appendChild(st);

          // 3) Ctrl/Cmd + rueda y gestos de trackpad en escritorio.
          const stop = (e) => { if (e.ctrlKey || e.metaKey) { e.preventDefault(); } };
          doc.addEventListener('wheel', stop, { passive: false });
          ['gesturestart', 'gesturechange', 'gestureend'].forEach((ev) =>
            doc.addEventListener(ev, (e) => e.preventDefault(), { passive: false })
          );

          // 4) Ctrl/Cmd +, - y 0 desde el teclado.
          doc.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) &&
                ['+', '-', '=', '0'].includes(e.key)) {
              e.preventDefault();
            }
          });
        })();
        </script>
        """,
        height=0,
    )


bloquear_zoom()

# --------------------------------------------------------------------------- #
# Estilo
# --------------------------------------------------------------------------- #
st.markdown(
    """
    <style>
      [data-testid="stToolbar"], [data-testid="stDecoration"], #MainMenu { display:none !important; }
      header[data-testid="stHeader"] { background:transparent; }
      footer { visibility:hidden; }
      .stApp { background:
        radial-gradient(120% 60% at 50% -5%, #16223a 0%, rgba(14,19,32,0) 55%),
        radial-gradient(90% 60% at 115% 110%, #1c1636 0%, rgba(14,19,32,0) 50%), #0E1320; }
      .demo-badge { display:inline-block; background:#F0885A22; color:#F0885A;
        border:1px solid #F0885A55; padding:3px 12px; border-radius:999px;
        font-size:12px; font-weight:700; letter-spacing:.12em; }
      .brand { font-weight:800; letter-spacing:-.01em; }
      .muted { color:#96A3B8; }
      .card { background:#151D2C; border:1px solid #ffffff14; border-radius:16px;
        padding:18px 20px; }
      div[data-testid="stMetricValue"] { color:#5FE0B0; }
      .login-title { font-size:26px; font-weight:800; margin:6px 0 2px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------- #
# Estado
# --------------------------------------------------------------------------- #
if "logged" not in st.session_state:
    st.session_state.logged = False
if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"


# --------------------------------------------------------------------------- #
# Datos INVENTADOS (nada real)
# --------------------------------------------------------------------------- #
def datos_ventas() -> pd.DataFrame:
    filas = [
        ("Refresco Cola 600ml", 1240, 18600, 9920, "Impulsar"),
        ("Galletas Surtido 1kg", 860, 25800, 15480, "Impulsar"),
        ("Aceite Vegetal 1L", 540, 16200, 11340, "Descuento crítico"),
        ("Jabón de tocador", 1520, 12160, 6080, "Impulsar"),
        ("Atún en lata 140g", 980, 17640, 11760, "Impulsar"),
        ("Papel higiénico 4p", 430, 12900, 9030, "Revisar"),
        ("Leche entera 1L", 1310, 26200, 18340, "Impulsar"),
        ("Cereal 500g", 360, 14400, 7200, "Descuento crítico"),
        ("Café soluble 200g", 290, 20300, 12180, "Impulsar"),
        ("Detergente 1kg", 610, 18300, 10980, "Revisar"),
    ]
    df = pd.DataFrame(filas, columns=["Producto", "Piezas", "Venta ($)", "Utilidad ($)", "Decisión"])
    df["Margen %"] = (df["Utilidad ($)"] / df["Venta ($)"] * 100).round(1)
    return df


def datos_tiendas() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("Sucursal Centro", 3420, 1980, 5400),
            ("Sucursal Norte", 2610, 1240, 3850),
            ("Sucursal Sur", 1890, 990, 2880),
            ("Sucursal Poniente", 2230, 1510, 3740),
        ],
        columns=["Sucursal", "Tickets ($ miles)", "Facturas ($ miles)", "Total ($ miles)"],
    )


def datos_cuadre() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("7501000010", 120, 120, "✔ Cuadra"),
            ("7501000027", 80, 80, "✔ Cuadra"),
            ("7501000034", 60, 54, "✗ Diferencia -6"),
            ("7501000041", 200, 200, "✔ Cuadra"),
            ("7501000058", 45, 50, "✗ Diferencia +5"),
            ("7501000065", 90, 90, "✔ Cuadra"),
        ],
        columns=["Código de barras", "Ordenado", "Recibido", "Estatus"],
    )


def datos_notas() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("Proveedor A", "01/08/2026", "Entrega parcial, faltan 3 cajas", "Pendiente"),
            ("Proveedor B", "31/07/2026", "Nota de crédito por producto dañado", "Resuelta"),
            ("Proveedor C", "30/07/2026", "Cambio de precio a partir de agosto", "Pendiente"),
            ("Proveedor A", "29/07/2026", "Devolución de mercancía caduca", "Resuelta"),
        ],
        columns=["Proveedor", "Fecha", "Nota", "Estatus"],
    )


def datos_compras() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("Proveedor A", 18, 42300),
            ("Proveedor B", 11, 27600),
            ("Proveedor C", 7, 15400),
            ("Proveedor D", 22, 51800),
        ],
        columns=["Proveedor", "Facturas", "Total comprado ($)"],
    )


CATALOGO = [
    ("🥤", "Refresco Cola 600ml", 15.0, "Disp: 320"),
    ("🍪", "Galletas Surtido 1kg", 30.0, "Disp: 140"),
    ("🛢️", "Aceite Vegetal 1L", 30.0, "Disp: 90"),
    ("🧼", "Jabón de tocador", 8.0, "Disp: 500"),
    ("🐟", "Atún en lata 140g", 18.0, "Disp: 260"),
    ("🥛", "Leche entera 1L", 20.0, "Disp: 410"),
]


# --------------------------------------------------------------------------- #
# LOGIN
# --------------------------------------------------------------------------- #
def pantalla_login() -> None:
    izq, cen, der = st.columns([1, 1.15, 1])
    with cen:
        st.write("")
        st.write("")
        if os.path.exists(LOGO):
            l, m, r = st.columns([1, 1, 1])
            with m:
                st.image(LOGO, use_container_width=True)
        st.markdown(
            "<p style='text-align:center' class='muted'>Bienvenido a tu Portal</p>",
            unsafe_allow_html=True,
        )
        with st.container(border=True):
            st.text_input("Usuario", value="demo", key="u")
            st.text_input("Contraseña", value="demo123", type="password", key="p")
            if st.button("Entrar", type="primary", use_container_width=True):
                st.session_state.logged = True
                st.session_state.pagina = "inicio"
                st.rerun()
        st.markdown(
            "<p style='text-align:center;margin-top:10px'>"
            "<span class='demo-badge'>VERSIÓN DEMO</span></p>"
            "<p style='text-align:center' class='muted'>usuario: <b>demo</b> · contraseña: <b>demo123</b></p>"
            "<p style='text-align:center;margin-top:14px' class='muted'>powered by Automatización</p>",
            unsafe_allow_html=True,
        )


# --------------------------------------------------------------------------- #
# MENU
# --------------------------------------------------------------------------- #
MENU = [
    ("inicio", "🏠 Inicio"),
    ("ventas", "📈 Ventas y Análisis"),
    ("ventas_tienda", "🏪 Ventas por tienda"),
    ("cuadre", "📦 Cuadre de órdenes"),
    ("prov_bandeja", "📥 Notas de proveedores"),
    ("prov_compras", "🚚 Compras por proveedor"),
    ("catalogo", "🛒 Catálogo"),
]


def barra_lateral() -> None:
    with st.sidebar:
        if os.path.exists(LOGO):
            st.image(LOGO, width=110)
        st.markdown(f"**{NEGOCIO_DEMO}**  \n<span class='muted'>Portal de automatización</span>",
                    unsafe_allow_html=True)
        st.markdown("### Programas")
        for key, label in MENU:
            tipo = "primary" if st.session_state.pagina == key else "secondary"
            if st.button(label, key="m_" + key, use_container_width=True, type=tipo):
                st.session_state.pagina = key
                st.rerun()
        st.divider()
        if st.button("Cerrar sesión", use_container_width=True):
            st.session_state.logged = False
            st.rerun()


def encabezado(titulo: str, sub: str) -> None:
    # Boton para regresar al menu (util sobre todo en celular, donde la barra se esconde)
    if st.session_state.get("pagina", "inicio") != "inicio":
        if st.button("← Volver al inicio", key="volver_" + titulo):
            st.session_state.pagina = "inicio"
            st.rerun()
    c1, c2 = st.columns([4, 1])
    with c1:
        st.markdown(f"## {titulo}")
        st.caption(sub)
    with c2:
        st.markdown("<p style='text-align:right'><span class='demo-badge'>DEMO</span></p>",
                    unsafe_allow_html=True)
    st.divider()


# --------------------------------------------------------------------------- #
# PAGINAS
# --------------------------------------------------------------------------- #
def pagina_inicio() -> None:
    encabezado(f"Bienvenido, {NEGOCIO_DEMO}", "Toca un programa del menú para abrirlo. (Datos de ejemplo)")
    st.write("Todos tus programas en un solo lugar, con tu acceso privado:")
    cols = st.columns(3)
    tarjetas = [m for m in MENU if m[0] != "inicio"]
    for i, (key, label) in enumerate(tarjetas):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"### {label}")
                st.caption("Automático · en segundos")
                if st.button("Abrir", key="c_" + key, use_container_width=True):
                    st.session_state.pagina = key
                    st.rerun()


def pagina_ventas() -> None:
    encabezado("Ventas y Análisis", "Reporte automático de ventas, márgenes y decisiones.")
    df = datos_ventas()
    a, b, c = st.columns(3)
    a.metric("Venta total", f"${df['Venta ($)'].sum():,.0f}")
    b.metric("Utilidad", f"${df['Utilidad ($)'].sum():,.0f}")
    c.metric("Margen promedio", f"{df['Margen %'].mean():.1f}%")
    st.markdown("#### Top productos por venta")
    st.bar_chart(df.set_index("Producto")["Venta ($)"], color="#5B8DEF")
    st.markdown("#### Detalle")
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.button("⬇ Descargar reporte PDF", disabled=True, help="Función de ejemplo en la demo")


def pagina_tiendas() -> None:
    encabezado("Ventas por tienda", "Comparativo de sucursales del periodo.")
    df = datos_tiendas()
    st.bar_chart(df.set_index("Sucursal")["Total ($ miles)"], color="#2ED18E")
    st.dataframe(df, use_container_width=True, hide_index=True)


def pagina_cuadre() -> None:
    encabezado("Cuadre de órdenes", "Compara lo ordenado contra lo recibido, por código de barras.")
    df = datos_cuadre()
    ok = (df["Estatus"].str.startswith("✔")).sum()
    st.metric("Productos que cuadran", f"{ok} de {len(df)}")
    st.dataframe(df, use_container_width=True, hide_index=True)


def pagina_notas() -> None:
    encabezado("Notas de proveedores", "Los proveedores registran sus notas; tú las revisas aquí.")
    df = datos_notas()
    st.dataframe(df, use_container_width=True, hide_index=True)


def pagina_compras() -> None:
    encabezado("Compras por proveedor", "Cuánto le has comprado a cada proveedor.")
    df = datos_compras()
    st.bar_chart(df.set_index("Proveedor")["Total comprado ($)"], color="#9A7BFF")
    st.dataframe(df, use_container_width=True, hide_index=True)


def pagina_catalogo() -> None:
    encabezado("Catálogo", "Tu catálogo en línea; los clientes piden por WhatsApp.")
    cols = st.columns(3)
    for i, (emoji, nombre, precio, disp) in enumerate(CATALOGO):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"<div style='font-size:44px'>{emoji}</div>", unsafe_allow_html=True)
                st.markdown(f"**{nombre}**")
                st.markdown(f"### ${precio:,.2f}")
                st.caption(disp)
                st.button("🛒 Agregar", key="cat_" + str(i), use_container_width=True, disabled=True)


PAGINAS = {
    "inicio": pagina_inicio,
    "ventas": pagina_ventas,
    "ventas_tienda": pagina_tiendas,
    "cuadre": pagina_cuadre,
    "prov_bandeja": pagina_notas,
    "prov_compras": pagina_compras,
    "catalogo": pagina_catalogo,
}


# --------------------------------------------------------------------------- #
# MAIN
# --------------------------------------------------------------------------- #
if not st.session_state.logged:
    pantalla_login()
else:
    barra_lateral()
    PAGINAS.get(st.session_state.pagina, pagina_inicio)()
