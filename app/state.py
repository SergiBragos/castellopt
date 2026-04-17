# state.py
import reflex as rx
import sqlmodel
import hashlib
from typing import Optional # Importem per al tipus de la colla

# ── BDDs ──────────────────────────────────────────────────────────────────────

class User(rx.Model, table=True):
    username: str = sqlmodel.Field(unique=True, index=True)
    password: str
    colla: int
    email: str

class Casteller(rx.Model, table=True):
    name: str
    nickname: str
    colla: int
    height: int
    weight: int
    talla: str
    comentaris: str

# ── Helpers ───────────────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# ── App State ─────────────────────────────────────────────────────────────────

class AppState(rx.State):
    username: str = ""
    is_logged_in: bool = False
    colla: int | None = None  # Usem el pipe | per permetre el None inicial
    email: str = ""

    login_username: str = ""
    login_password: str = ""
    login_error: str = ""

    casteller_name: str = ""
    casteller_nickname: str = ""
    casteller_height: str = "" 
    casteller_weight: str = "" 
    casteller_id_edicio: int | None = None
    casteller_shirt: str = ""
    casteller_notes: str = ""
    entry_success: str = ""

    # Setters manuals (Necessaris per evitar DeprecationWarnings)
    def set_name(self, value: str): self.casteller_name = value
    def set_nickname(self, value: str): self.casteller_nickname = value
    def set_height(self, value: str): self.casteller_height = value
    def set_weight(self, value: str): self.casteller_weight = value
    def set_shirt(self, value: str): self.casteller_shirt = value # Afegit
    def set_notes(self, value: str): self.casteller_notes = value # Afegit

    prioritize_safety: bool = True
    allow_swaps: bool = True
    use_experience: bool = False
    display_name: str = ""
    settings_saved: str = ""

    results_tab: str = "visual"

    def do_login(self):
        username = self.login_username.strip()
        password = self.login_password.strip()

        if not username or not password:
            self.login_error = "Si et plau, escriu el teu usuari i contrasenya."
            return

        with rx.session() as session:
            user = session.exec(
                sqlmodel.select(User).where(User.username == username)
            ).first()

        if user is None:
            self.login_error = "L'usuari no existeix."
            return

        # TODO: Implementar hash_password aquí quan tinguis usuaris reals
        if user.password != password:
            self.login_error = "Contrasenya incorrecta."
            return

        self.username = username
        self.display_name = username
        self.is_logged_in = True
        self.login_error = ""
        self.email = user.email
        self.colla = int(user.colla)
        return rx.redirect("/dashboard")

    def do_logout(self):
        self.is_logged_in = False
        self.username = ""
        self.login_username = ""
        self.login_password = ""
        return rx.redirect("/")

    def set_results_tab(self, tab: str):
        self.results_tab = tab

    def save_casteller(self):
        if not self.casteller_name.strip():
            self.entry_success = "error: El nom és obligatori."
            return
        
        try:
            # Validació de números abans d'entrar a la sessió
            # El .strip() i l'OR '0' evita errors si l'input està buit
            h = int(self.casteller_height.strip() or "0")
            w = int(self.casteller_weight.strip() or "0")

            with rx.session() as session:
                if self.casteller_id_edicio:
                    casteller = session.get(Casteller, self.casteller_id_edicio)
                    if casteller:
                        casteller.name = str(self.casteller_name)
                        casteller.nickname = str(self.casteller_nickname)
                        casteller.colla = int(self.colla)
                        casteller.height = h
                        casteller.weight = w
                        casteller.talla = str(self.casteller_shirt)
                        casteller.comentaris = str(self.casteller_notes)
                else:
                    nou_casteller = Casteller(
                        name=str(self.casteller_name),
                        nickname=str(self.casteller_nickname),
                        colla=int(self.colla),
                        height=h,
                        weight=w,
                        talla=str(self.casteller_shirt),
                        comentaris=str(self.casteller_notes),
                    )
                    session.add(nou_casteller)
                
                session.commit()
                self.casteller_id_edicio = None 
            
            self.clear_form() # Usem la funció per netejar el formulari
            self.entry_success = f"Reeixida! Casteller desat correctament!"

        except ValueError:
            self.entry_success = "error: L'alçada i el pes han de ser números."
        except Exception as e:
            self.entry_success = f"error: {str(e)}"

    def goto_edit_casteller(self, casteller: Casteller):
        """Prepara l'estat per editar i redirigeix al formulari."""
        self.casteller_id_edicio = int(casteller.id)
        self.casteller_name = casteller.name
        self.casteller_nickname = casteller.nickname
        
        # CORRECCIÓ CRÍTICA: Convertim a str() perquè l'estat espera STR, no INT.
        self.casteller_height = str(casteller.height)
        self.casteller_weight = str(casteller.weight)
        
        self.casteller_shirt = casteller.talla
        self.casteller_notes = casteller.comentaris
        self.entry_success = "" # Netegem missatges previs
        
        return rx.redirect("/manual")

    def clear_form(self):
        self.casteller_name = ""
        self.casteller_nickname = ""
        self.casteller_height = ""
        self.casteller_weight = ""
        self.casteller_shirt = ""
        self.casteller_notes = ""
        self.casteller_id_edicio = None
        self.entry_success = ""

    def save_settings(self):
        self.settings_saved = "Preferències actualitzades correctament!"

    def toggle_safety(self):
        self.prioritize_safety = not self.prioritize_safety

    def toggle_swaps(self):
        self.allow_swaps = not self.allow_swaps

    def toggle_experience(self):
        self.use_experience = not self.use_experience

    @rx.var
    def user_initials(self) -> str:
        if not self.username:
            return "?"
        parts = self.username.strip().split()
        if len(parts) >= 2:
            return (parts[0][0] + parts[1][0]).upper()
        return self.username[:2].upper()

    @rx.var
    def entry_is_error(self) -> bool:
        return self.entry_success.startswith("error:")

    @rx.var
    def entry_message(self) -> str:
        if ":" in self.entry_success:
            return self.entry_success.split(":", 1)[1]
        return self.entry_success
    
    @rx.var
    def num_castellers(self) -> int:
        with rx.session() as session:
            # Busquem tots els castellers que tenen la mateixa colla que l'usuari
            result = session.exec(
                sqlmodel.select(Casteller).where(Casteller.colla == self.colla)
            ).all()
            return len(result)

    @rx.var
    def castellers_colla(self) -> list[Casteller]:
        with rx.session() as session:
            # Recuperem tots els castellers de la colla actual
            return session.exec(
                sqlmodel.select(Casteller).where(Casteller.colla == self.colla)
            ).all()