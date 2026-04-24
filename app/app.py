#app/app.py

import reflex as rx
from app import styles

app = rx.App(
    style=styles.base_style,
    theme=rx.theme(
        appearance="inherit", # Important per a que el switch funcioni
        has_background=False,  # Diu a Reflex que pinti el fons de la pàgina
    ),
    stylesheets=["styles.css"],
)

from app.pages.login import login_page
from app.pages.dashboard import dashboard_page
from app.pages.upload import upload_page
from app.pages.manual_entry import manual_entry_page
from app.pages.results import results_page
from app.pages.settings import settings_page
from app.state import AppState

app.add_page(login_page, route="/", title="CastellOpt — Login")
app.add_page(dashboard_page, route="/dashboard", title="CastellOpt — Dashboard")
app.add_page(upload_page, route="/upload", title="CastellOpt — Càrrega CSV", on_load=[AppState.clear_entry_success])
app.add_page(manual_entry_page, route="/manual", title="CastellOpt — Entrada Manual", on_load=[AppState.clear_entry_success])
app.add_page(results_page, route="/results", title="CastellOpt — Resultats")
app.add_page(settings_page, route="/settings", title="CastellOpt — Preferències")
