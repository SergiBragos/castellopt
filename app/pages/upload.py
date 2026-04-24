import reflex as rx
from app import styles
from app.components.layout import app_layout
from app.state import AppState

def upload_page() -> rx.Component:
    return app_layout(
        rx.vstack(
            rx.box(
                rx.text("Carrega CSV", style=styles.page_title_style),
                rx.text("Importa o modifica castellers massivament", style=styles.page_sub_style),
                width="100%",
            ),
            
            rx.card(
                rx.vstack(
                    rx.text("Selecciona fitxer", style=styles.card_title_style),
                    
                    # El component d'upload és el que rep l'estil de la vora i el hover
                    rx.upload(
                        rx.vstack(
                            rx.text("⬆️", font_size="28px"),
                            rx.text("Arrossega el teu CSV o clica per cercar-lo.", font_weight="500"),
                            rx.text("Format: id, name, nickname, height, weight, talla, action", font_size="11px", color=styles.TEXT_SECONDARY),
                            spacing="2",
                            align_items="center",
                            justify_content="center",
                        ),
                        id="csv_upload",
                        accept={
                            "text/csv": [".csv"],
                            "application/vnd.ms-excel": [".csv"], # Necessari perquè Windows sovint veu els CSV com Excel
                            "application/csv": [".csv"]
                        },
                        max_files=1,
                        multiple=False,
                        border=f"2px dashed {styles.BORDER_MID}",
                        border_radius="15px",
                        padding="40px",
                        width="100%",
                        transition="all 0.3s ease", # Transició suau
                        _hover={
                            "background_color": styles.PURPLE_LIGHT,
                            "border_color": styles.PURPLE_MID,
                            "cursor": "pointer",
                        },
                    ),
                    
                    # Llista de fitxers seleccionats
                    rx.vstack(
                        rx.foreach(rx.selected_files("csv_upload"), rx.text),
                        align_items="start",
                        width="100%",
                    ),
                    
                    rx.button(
                        "Processar i carregar dades",
                        on_click=AppState.handle_csv_upload(rx.upload_files(upload_id="csv_upload")),
                        loading=AppState.upload_processing,
                        style=styles.btn_primary,
                        width="100%", # Millor 100% o un min_width per usabilitat
                    ),
                    spacing="4",
                ),
                style=styles.card_style,
                width="100%",
            ),

            rx.card(
                rx.text("Estructura del CSV", style=styles.card_title_style),
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Columna"),
                            rx.table.column_header_cell("Descripció"),
                            rx.table.column_header_cell("Acció"),
                        )
                    ),
                    rx.table.body(
                        rx.table.row(rx.table.cell(rx.text("id", font_family="monospace")), rx.table.cell("ID del casteller."), rx.table.cell("Només per editar/esborrar")),
                        rx.table.row(rx.table.cell("name"), rx.table.cell("Nom i cognom"), rx.table.cell(rx.box(rx.text("Obligatori", **styles.badge_info)))),
                        rx.table.row(rx.table.cell("nickname"), rx.table.cell("Sobrenom"), rx.table.cell("Opcional")),
                        rx.table.row(rx.table.cell("height"), rx.table.cell("Alçada (cm)"), rx.table.cell(rx.box(rx.text("Obligatori", **styles.badge_info)))),
                        rx.table.row(rx.table.cell("weight"), rx.table.cell("Pes (kg)"), rx.table.cell("Opcional")),
                        rx.table.row(rx.table.cell("talla"), rx.table.cell("XS/S/M/L/XL"), rx.table.cell(rx.box(rx.text("Obligatori", **styles.badge_info)))),
                        rx.table.row(rx.table.cell("action"), rx.table.cell("'save' o 'delete'"), rx.table.cell("Per defecte: save")),
                    ),
                    width="100%",
                ),
                style=styles.card_style,
                width="100%",
            ),
            
            rx.link(rx.button("Tornar al Dashboard", style=styles.btn_secondary), href="/dashboard"),
            spacing="6",
            width="100%",
            padding_bottom="40px",
        ),
        "/upload",
    )