# app/pages/results.py
import reflex as rx
from app.state import AppState
from app import styles
from app.components.layout import app_layout

# FORMATION es manté com a diccionari estàtic per a la vista "Visual" 
# fins que implementis l'algoritme que assigni els membres de la DB a cada pis.
FORMATION = [
    {"floor": "Enxaneta",   "members": ["Laia"],           "bg": styles.PURPLE_LIGHT, "fg": styles.PURPLE_DARK},
    {"floor": "Acotxador",   "members": ["Jana"],           "bg": styles.PURPLE_LIGHT, "fg": styles.PURPLE_DARK},
    {"floor": "Pom de dalt","members": ["Mireia A", "Anna"],  "bg": styles.TEAL_LIGHT,   "fg": styles.TEAL_DARK},
    {"floor": "Quarts",     "members": ["Mireia B", "Núria", "Rosa", "Marta"], "bg": styles.CORAL_LIGHT,  "fg": styles.CORAL_DARK},
    {"floor": "Terços",     "members": ["Sergi", "Joan", "Jordi", "Pere"], "bg": styles.BLUE_LIGHT, "fg": styles.BLUE_DARK},
    {"floor": "Segons",      "members": ["Albert", "Pau", "Ferran", "Miki"], "bg": styles.PURPLE_LIGHT, "fg": styles.PURPLE_DARK},
    {"floor": "Baixos",      "members": ["Xavi", "Antoni", "Ona", "Martina"], "bg": styles.PURPLE_LIGHT, "fg": styles.PURPLE_DARK},
]

def chip(name: str, bg: str, fg: str) -> rx.Component:
    """Component visual per als membres del tronc."""
    return rx.box(
        rx.text(name, font_size="10px", font_weight="500"),
        background_color=bg, 
        color=fg,
        border_radius="14px", 
        padding="4px 10px", 
        white_space="nowrap",
    )

def results_page() -> rx.Component:
    return app_layout(
        rx.box(
            rx.text("Resultats", style=styles.page_title_style),
            rx.text("Formació òptima del castell", style=styles.page_sub_style),

            # --- TAB BAR ---
            rx.hstack(
                rx.button(
                    "Visual",
                    on_click=lambda: AppState.set_results_tab("visual"),
                    font_size="13px", padding="8px 14px", border_radius="0",
                    background_color="transparent", border="none",
                    border_bottom=rx.cond(AppState.results_tab == "visual", f"2px solid {styles.PURPLE_MID}", "2px solid transparent"),
                    color=rx.cond(AppState.results_tab == "visual", styles.PURPLE_MID, styles.TEXT_SECONDARY),
                    font_weight=rx.cond(AppState.results_tab == "visual", "500", "400"),
                    cursor="pointer",
                ),
                rx.button(
                    "Llista de castellers",
                    on_click=lambda: AppState.set_results_tab("list"),
                    font_size="13px", padding="8px 14px", border_radius="0",
                    background_color="transparent", border="none",
                    border_bottom=rx.cond(AppState.results_tab == "list", f"2px solid {styles.PURPLE_MID}", "2px solid transparent"),
                    color=rx.cond(AppState.results_tab == "list", styles.PURPLE_MID, styles.TEXT_SECONDARY),
                    font_weight=rx.cond(AppState.results_tab == "list", "500", "400"),
                    cursor="pointer",
                ),
                spacing="0",
                border_bottom=f"0.5px solid {styles.BORDER}",
                margin_bottom="20px",
                width="100%",
            ),

            # --- CONTINGUT DINÀMIC SEGONS LA TAB SELECCIONADA ---
            rx.cond(
                AppState.results_tab == "visual",
                # VISTA VISUAL (TRONC)
                rx.box(
                    rx.text("4d8 — formació òptima", style=styles.card_title_style),
                    rx.text("Tronc", font_size="11px", color=styles.TEXT_SECONDARY, text_align="center", margin_bottom="12px"),
                    rx.vstack(
                        *[
                            rx.hstack(
                                rx.text(row["floor"], font_size="10px", color=styles.TEXT_SECONDARY, width="72px", text_align="right"),
                                rx.hstack(*[chip(m, row["bg"], row["fg"]) for m in row["members"]], spacing="1", flex_wrap="wrap"),
                                spacing="2", align_items="center", justify_content="center", width="100%",
                            )
                            for row in FORMATION
                        ],
                        spacing="2", align_items="center", width="100%",
                    ),
                    rx.center(rx.box(rx.text("Score: 94 / 100", **styles.badge_success), margin_top="16px")),
                    style=styles.card_style,
                ),

                # VISTA LLISTA (BASE DE DADES REAL)
                rx.box(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell(rx.text("Nom", font_size="12px", color=styles.TEXT_SECONDARY)),
                                rx.table.column_header_cell(rx.text("Sobrenom", font_size="12px", color=styles.TEXT_SECONDARY)),
                                rx.table.column_header_cell(rx.text("Alçada", font_size="12px", color=styles.TEXT_SECONDARY)),
                                rx.table.column_header_cell(rx.text("Pes", font_size="12px", color=styles.TEXT_SECONDARY)),
                                rx.table.column_header_cell(rx.text("Talla", font_size="12px", color=styles.TEXT_SECONDARY)),
                                rx.table.column_header_cell(rx.text("Accions", font_size="12px", color=styles.TEXT_SECONDARY))
                            )
                        ),
                        rx.table.body(
                            # rx.foreach llegeix directament de la DB via AppState.castellers_colla
                            rx.foreach(
                                AppState.castellers_colla,
                                lambda casteller: rx.table.row(
                                    rx.table.cell(rx.text(casteller.name, font_size="12px")),
                                    rx.table.cell(
                                        rx.box(
                                            rx.text(casteller.nickname, font_size="12px", color=styles.TEXT_SECONDARY),
                                            background_color=styles.PURPLE_LIGHT,
                                            color=styles.PURPLE_DARK,
                                            text_align="center",
                                            font_weight="bold",
                                            padding="2px 2px",
                                            border_radius="10px")),
                                    rx.table.cell(rx.text(f"{casteller.height} cm", font_size="12px", color=styles.TEXT_SECONDARY)),
                                    rx.table.cell(rx.text(f"{casteller.weight} kg", font_size="12px", color=styles.TEXT_SECONDARY)),
                                    rx.table.cell(rx.text(casteller.talla, font_size="10px", font_weight="bold")),
                                    rx.table.cell(
                                        rx.button(
                                            rx.icon(tag="square_pen", size=16), # Icona d'editar
                                            on_click=lambda: AppState.goto_edit_casteller(casteller),
                                            variant="ghost",
                                            color_scheme="gray",
                                            cursor="pointer",))
                                    ),
                                )
                        ),
                        width="100%",
                    ),
                    style=styles.card_style,
                ),
            ),

            # --- ACCIONS FINALS ---
            rx.hstack(
                rx.button(
                    "Optimitzar (coming soon)", 
                    style={**styles.btn_primary, "opacity": "0.6", "cursor": "not-allowed"}
                ),
                rx.button("Exporta com a PDF (coming soon)", style=styles.btn_secondary),
                spacing="2", 
                margin_top="16px", # Una mica més de marge per respirar
            ),
            width="100%",
        ),
        # Aquest segon argument d'app_layout sol ser la ruta activa per al menú
        "/results", 
    )