import reflex as rx
from app.state import AppState
from app import styles


def login_page() -> rx.Component:
    return rx.center(
        rx.box(
            rx.vstack(
                rx.image(
                    src="/imatge_castellers.png", 
                    width="80px", 
                    height="auto",
                    border_radius="15px",
                ),
                rx.text("CastellOpt", font_size="22px", font_weight="500", color=styles.TEXT_PRIMARY),
                rx.text("Optimitzador de castells", font_size="13px", color=styles.TEXT_SECONDARY),
                spacing="1",
                align_items="center",
                margin_bottom="24px",
            ),
            rx.vstack(
                rx.vstack(
                    rx.text("Usuari", style=styles.label_style),
                    rx.input(
                        placeholder="el teu usuari",
                        value=AppState.login_username,
                        on_change=AppState.set_login_username,
                        width="100%",
                        font_size="13px",
                    ),
                    spacing="1",
                    width="100%",
                    align_items="flex_start",
                ),
                rx.vstack(
                    rx.text("Contrasenya", style=styles.label_style),
                    rx.input(
                        type="password",
                        placeholder="••••••••",
                        value=AppState.login_password,
                        on_change=AppState.set_login_password,
                        width="100%",
                        font_size="13px",
                    ),
                    spacing="1",
                    width="100%",
                    align_items="flex_start",
                ),
                rx.cond(
                    AppState.login_error != "",
                    rx.text(AppState.login_error, font_size="12px", color="red"),
                ),
                rx.button(
                    "Entra",
                    on_click=AppState.do_login,
                    width="100%",
                    background_color=styles.PURPLE_MID,
                    color="white",
                    border="none",
                    border_radius="8px",
                    padding="10px",
                    font_size="14px",
                    font_weight="500",
                    cursor="pointer",
                    _hover={"background_color": styles.PURPLE_DARK},
                ),
                spacing="3",
                width="100%",
            ),
            rx.hstack(
                rx.divider(width="100%"),
                rx.text("feina de formiga, força d'elefant", font_size="11px", color=styles.TEXT_SECONDARY, white_space="nowrap"),
                rx.divider(width="100%"),
                width="100%",
                align_items="center",
                margin_top="16px",
                gap="8px",
            ),
            background_color=styles.BG_PRIMARY,
            border=f"0.5px solid {styles.BORDER}",
            border_radius="12px",
            padding="32px",
            width="320px",
        ),
        height="100vh",
        background_color=styles.BG_TERTIARY,
    )
