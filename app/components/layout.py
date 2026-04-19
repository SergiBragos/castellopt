#app/components/layout.py
import reflex as rx
from app.state import AppState
from app import styles


def nav_item(label: str, icon: str, route: str, active_route: str) -> rx.Component:
    is_active = active_route == route
    item_style = styles.nav_item_active if is_active else styles.nav_item_base
    return rx.link(
        rx.text(icon, font_size="16px"),
        rx.text(label, font_size="13px"),
        href=route,
        style=item_style,
        display="flex",
        align_items="center",
        gap="10px",
        width="100%",
        text_decoration="none",
    )

def sidebar_footer() -> rx.Component:
    #Component per a la part inferior de la sidebar amb el switch de mode.
    return rx.vstack(
        rx.divider(border_color=styles.BORDER),
        rx.hstack(
            rx.text("Mode fosc", font_size="13px", color=styles.TEXT_SECONDARY),
            rx.spacer(),
            rx.color_mode.switch(), # El switch de Reflex que gestiona tot sol el canvi
            width="100%",
            padding="16px",
            align_items="center",
        ),
        width="100%",
    )


def sidebar(active_route: str) -> rx.Component:
    return rx.box(
        rx.box(
            rx.hstack(
                rx.image(
                    src="/imatge_castellers.png", 
                    width="50px", 
                    height="auto",
                    border_radius="15px",
                ),
                rx.vstack(
                    rx.text("CastellOpt", font_size="15px", font_weight="500", color=styles.TEXT_PRIMARY),
                    rx.text("Optimitzador de castells", font_size="11px", color=styles.TEXT_SECONDARY),
                    spacing="0",
                    align_items="flex_start",
                ),
                spacing="2",
                align_items="center",
            ),
            padding="16px",
            border_bottom=f"0.5px solid {styles.BORDER}",
            margin_bottom="8px",
        ),
        nav_item("Dashboard", "📈", "/dashboard", active_route),
        nav_item("Carregar CSV", "⬆️", "/upload", active_route),
        nav_item("Entrada manual", "✏️", "/manual", active_route),
        nav_item("Resultats", "📊", "/results", active_route),
        nav_item("Preferències", "⚙️", "/settings", active_route),
        rx.spacer(),
        sidebar_footer(),
        rx.box(
            rx.hstack(
                rx.box(
                    rx.text(AppState.user_initials, font_size="11px", font_weight="500", color=styles.PURPLE_DARK),
                    width="28px",
                    height="28px",
                    border_radius="50%",
                    background_color=styles.PURPLE_BORDER,
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
                rx.vstack(
                    rx.text(AppState.username, font_size="12px", font_weight="500", color=styles.TEXT_PRIMARY),
                    rx.text(
                        "Sign out",
                        font_size="11px",
                        color=styles.TEXT_SECONDARY,
                        cursor="pointer",
                        on_click=AppState.do_logout,
                        _hover={"color": styles.PURPLE_MID},
                    ),
                    spacing="0",
                    align_items="flex_start",
                ),
                spacing="2",
                align_items="center",
            ),
            padding="12px 16px",
            border_top=f"0.5px solid {styles.BORDER}",
        ),
        style=styles.sidebar_style,
        display="flex",
        flex_direction="column",
    )


def app_layout(content: rx.Component, active_route: str) -> rx.Component:
    return rx.cond(
        AppState.is_logged_in,
        rx.hstack(
            sidebar(active_route),
            rx.box(
                content,
                flex="1",
                padding="24px",
                overflow_y="auto",
                height="100vh",
                background_color=styles.BG_TERTIARY,
            ),
            background_color=styles.BG_TERTIARY,
            spacing="0",
            align_items="flex_start",
            height="100vh",
            width="100%",
        ),
        rx.box(
            rx.script("window.location.href='/'"),
        ),
    )
