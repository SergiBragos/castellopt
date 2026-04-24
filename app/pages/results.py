# app/pages/results.py
import reflex as rx
from app.state import AppState
from app import styles
from app.components.layout import app_layout

#------------DADES ESTÀTIQUES (Per a la vista Visual)------------
FORMATION = [
    {"floor": "Enxaneta",   "members": ["Laia"],           "bg": styles.PURPLE_LIGHT, "fg": styles.PURPLE_DARK},
    {"floor": "Acotxador",   "members": ["Jana"],           "bg": styles.PURPLE_LIGHT, "fg": styles.PURPLE_DARK},
    {"floor": "Pom de dalt","members": ["Mireia A", "Anna"],  "bg": styles.TEAL_LIGHT,   "fg": styles.TEAL_DARK},
]

#------------FUNCIONS------------

def chip(name: str, bg: str, fg: str) -> rx.Component:
    #Component visual per als membres del tronc.
    return rx.box(
        rx.text(name, font_size="10px", font_weight="500"),
        background_color=bg, 
        color=fg,
        border_radius="14px", 
        padding="4px 10px", 
        white_space="nowrap",
    )

def dades_header():
    #Mostra les dades tècniques del castell seleccionat.
    return rx.cond(
        AppState.dades_castell_actiu,
        rx.grid(
            rx.vstack(
                rx.text("Posicions", font_size="10px", color=styles.TEXT_SECONDARY),
                rx.text(AppState.dades_castell_actiu.posicions.to(str), font_weight="bold"),
                align_items="start",
            ),
            rx.vstack(
                rx.text("Castellers", font_size="10px", color=styles.TEXT_SECONDARY),
                rx.text(AppState.dades_castell_actiu.num_castellers.to(str), font_weight="bold"),
                align_items="start",
            ),
            rx.vstack(
                rx.text("Tipus Tronc", font_size="10px", color=styles.TEXT_SECONDARY),
                rx.text(AppState.dades_castell_actiu.tipus_tronc, font_weight="bold"),
                align_items="start",
            ),
            columns="3",
            spacing="4",
            width="100%",
            padding="15px",
            background=styles.BG_SECONDARY,
            border_radius="8px",
            margin_bottom="20px",
        )
    )

def taula_estructura():
    """Genera la taula buida basada en pisos i rengles."""
    return rx.cond(
        AppState.dades_castell_actiu,
        rx.vstack(
            rx.text("Esquema del Tronc", style=styles.card_title_style),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Pis"),
                        rx.foreach(
                            AppState.llista_rengles_rang,
                            lambda i: rx.table.column_header_cell(f"R{i}")
                        )
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        AppState.llista_pisos_rang,
                        lambda p: rx.table.row(
                            rx.table.cell(rx.text(f"Pis {p}", font_weight="bold")),
                            rx.foreach(
                                AppState.llista_rengles_rang,
                                lambda r: rx.table.cell(
                                    rx.box(
                                        width="80px", 
                                        height="35px", 
                                        border=f"1px dashed {styles.BORDER}",
                                        border_radius="4px"
                                    )
                                )
                            )
                        )
                    )
                ),
                variant="surface",
                width="100%",
            ),
            align_items="start",
            width="100%",
        )
    )


#-----------LAYOUT-------------

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
                    background_color="transparent", border="BORDER",
                    border_bottom=rx.cond(AppState.results_tab == "visual", f"2px solid {styles.PURPLE_MID}", "2px solid transparent"),
                    color=rx.cond(AppState.results_tab == "visual", styles.PURPLE_MID, styles.TEXT_SECONDARY),
                    font_weight=rx.cond(AppState.results_tab == "visual", "500", "400"),
                    cursor="pointer",
                ),
                rx.button(
                    "Llista de castellers",
                    on_click=lambda: AppState.set_results_tab("list"),
                    font_size="13px", padding="8px 14px", border_radius="0",
                    background_color="transparent", border="BORDER",
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
                # VISTA VISUAL
                rx.vstack(
                    rx.box(
                        rx.hstack(
                            rx.vstack(
                                rx.text("Castell", style=styles.card_title_style),
                                rx.select(
                                    AppState.llista_noms_castells,
                                    value=AppState.selected_castell,
                                    on_change=AppState.set_selected_castell,
                                    placeholder="Tria un castell...",
                                    width="180px",
                                ),
                                align_items="start",
                            ),
                            rx.vstack(
                                rx.text("Iteracions", style=styles.card_title_style),
                                rx.select(
                                    ["1.000", "10.000", "100.000", "1.000.000"],
                                    value=AppState.iteracions_triades, # Recorda definir aquesta var a l'State
                                    on_change=AppState.set_iteracions_triades,
                                    width="140px",
                                ),
                                align_items="start",
                            ),
                            spacing="4",
                            align_items="end",
                        ),
                        style=styles.card_style, width="100%", margin_bottom="10px",
                    ),
                    
                    # Dades tècniques (Horitzontal)
                    dades_header(),

                    # Taula dinàmica (Esquema buit)
                    rx.box(
                        taula_estructura(),
                        style=styles.card_style, width="100%",
                    ),

                    # Mantenim el "Tronc" de prova que ja tenies (FORMATION) per sota
                    rx.box(
                        rx.text("Tronc (Vista Prèvia)", font_size="12px", color=styles.TEXT_SECONDARY, text_align="center", margin_bottom="12px"),
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
                        rx.center(rx.box(rx.text("Castell optimitzat correctament", **styles.badge_success), margin_top="16px")),
                        style=styles.card_style, width="100%",
                    ),
                    width="100%", spacing="4",
                ),

                # VISTA LLISTA (Es manté igual)
                rx.box(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell(rx.text("id", font_size="12px", color=styles.TEXT_SECONDARY)),
                                rx.table.column_header_cell(rx.text("Nom", font_size="12px", color=styles.TEXT_SECONDARY)),
                                rx.table.column_header_cell(rx.text("Sobrenom", font_size="12px", color=styles.TEXT_SECONDARY)),
                                rx.table.column_header_cell(rx.text("Alçada", font_size="12px", color=styles.TEXT_SECONDARY)),
                                rx.table.column_header_cell(rx.text("Pes", font_size="12px", color=styles.TEXT_SECONDARY)),
                                rx.table.column_header_cell(rx.text("Talla", font_size="12px", color=styles.TEXT_SECONDARY)),
                                rx.table.column_header_cell(rx.text("Accions", font_size="12px", color=styles.TEXT_SECONDARY))
                            )
                        ),
                        rx.table.body(
                            rx.foreach(
                                AppState.castellers_colla,
                                lambda casteller: rx.table.row(
                                    rx.table.cell(rx.text(casteller.id, font_size="12px")),
                                    rx.table.cell(rx.text(casteller.name, font_size="12px")),
                                    rx.table.cell(
                                        rx.box(
                                            rx.text(casteller.nickname, font_size="12px", color=styles.PURPLE_LIGHT),
                                            background_color=styles.PURPLE_DARK,
                                            color=styles.PURPLE_LIGHT,
                                            text_align="center",
                                            font_weight="bold",
                                            padding="2px 2px",
                                            border_radius="10px")),
                                    rx.table.cell(rx.text(f"{casteller.height} cm", font_size="12px", color=styles.TEXT_SECONDARY)),
                                    rx.table.cell(rx.text(f"{casteller.weight} kg", font_size="12px", color=styles.TEXT_SECONDARY)),
                                    rx.table.cell(rx.text(casteller.talla, font_size="10px", font_weight="bold")),
                                    rx.table.cell(
                                        rx.button(
                                            rx.icon(tag="square_pen", size=16),
                                            on_click=lambda: AppState.goto_edit_casteller(casteller),
                                            variant="ghost",
                                            color_scheme="gray",
                                            cursor="pointer"))
                                )
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
                margin_top="16px",
            ),
            width="100%",
        ),
        "/results", 
    )