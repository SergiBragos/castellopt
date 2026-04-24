#app/state.py
import reflex as rx
import sqlmodel
import hashlib
from typing import Optional # Importem per al tipus de la colla
import pandas as pd
import io

# ── BDDs ──────────────────────────────────────────────────────────────────────

class User(rx.Model, table=True):
    username: str = sqlmodel.Field(unique=True, index=True)
    password: str
    colla: int
    email: str

class Casteller(rx.Model, table=True):
    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    name: str
    nickname: str
    colla: int
    height: int
    weight: int
    talla: str
    comentaris: str

class Castell(rx.Model, table=True):
    nom: str = sqlmodel.Field(unique=True)
    posicions: int | None = None
    max_rengles: int | None = None
    max_reserves: int | None = None
    pisos: int | None = None
    num_castellers: int | None = None
    equacions: int | None = None
    tipus_tronc: str = ""
    max_iters: int | None = None
    min_iters: int | None = None
    rengles_pes: int | None = None
    x_folre: int | None = None
    x_manilles: int | None = None
    x_pinya: int | None = None
    x_tronc: int | None = None
    y_folre: int | None = None
    y_manilles: int | None = None
    y_pinya: int | None = None
    y_tronc: int | None = None
    dist_cordo: int | None = None
    angle_inioffset: int | None = None
    long_tit: float | None = None
    rang_mapa_r1: int | None = None
    offset_mapa_r1: int | None = None
    offset_titol_r1: int | None = None
    rang_mapa_r2: int | None = None
    offset_mapa_r2: int | None = None
    offset_titol_r2: int | None = None
    rang_mapa_r3: int | None = None
    offset_mapa_r3: int | None = None
    offset_titol_r3: int | None = None
    grafic_vmax: int | None = None
    grafic_nivvert: int | None = None
    grafic_nivhor: int | None = None
    cordo_cm: float | None = None

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
    upload_processing: bool = False #Variable per saber si estem enmig d'una càrrega de CSV

    # --- Setters manuals per evitar DeprecationWarnings ---
    
    # Formularis de Castellers
    def set_casteller_name(self, value: str): self.casteller_name = value
    def set_casteller_nickname(self, value: str): self.casteller_nickname = value
    def set_casteller_height(self, value: str): self.casteller_height = value
    def set_casteller_weight(self, value: str): self.casteller_weight = value
    def set_casteller_shirt(self, value: str): self.casteller_shirt = value
    def set_casteller_notes(self, value: str): self.casteller_notes = value
    def set_upload_processing(self, value: bool): self.upload_processing = value

    # Login
    def set_login_username(self, value: str): self.login_username = value
    def set_login_password(self, value: str): self.login_password = value
    def set_login_error(self, value: str): self.login_error = value

    # Settings i Preferències
    def set_display_name(self, value: str): self.display_name = value
    def set_email(self, value: str): self.email = value
    def set_selected_castell(self, value: str): self.selected_castell = value
    def set_iteracions_triades(self, value: str): self.iteracions_triades = value
    def set_results_tab(self, value: str): self.results_tab = value

    prioritize_safety: bool = True
    allow_swaps: bool = True
    use_experience: bool = False
    display_name: str = ""
    settings_saved: str = ""
    selected_castell: str = ""  # El nom del castell triat al menú
    dades_castell_actiu: Optional[Castell] = None
    iteracions_triades: str = ""
    def set_iteracions_triades(self, value: str): self.iteracions_triades = value

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

    def clear_entry_success(self):
        self.entry_success=""

    def save_settings(self):
        self.settings_saved = "Aquest botó de moment no fa res!"

    def toggle_safety(self):
        self.prioritize_safety = not self.prioritize_safety

    def toggle_swaps(self):
        self.allow_swaps = not self.allow_swaps

    def toggle_experience(self):
        self.use_experience = not self.use_experience

    def set_selected_castell(self, val: str):
        #La funció que canvia el valor de la variable selected_castell segons el que cliquis a la pestanya de results.
        self.selected_castell = val
        with rx.session() as session:
            # Busquem el castell a la DB per omplir les dades automàticament
            self.dades_castell_actiu = session.exec(
                sqlmodel.select(Castell).where(Castell.nom == val)
            ).first()
    
    #Funcions de la càrrega dels castellers en CSV.

    async def handle_csv_upload(self, files: list[rx.UploadFile]):
        self.upload_processing = True
        self.entry_success = "Processant..."
        
        try:
            for file in files:
                upload_data = await file.read()
                # Useu keep_default_na=False o fillna per evitar els problemes de l'int(NaN)
                df = pd.read_csv(io.BytesIO(upload_data)).fillna("")
                df.columns = df.columns.str.strip().str.lower()
                
                with rx.session() as session:
                    for _, row in df.iterrows():
                        row_id = row.get('id')
                        existing = None
                        
                        # Validem que l'ID sigui realment un número abans de buscar
                        if row_id != "" and pd.notna(row_id):
                            try:
                                search_id = int(float(row_id)) # float primer per si ve com "1.0"
                                existing = session.exec(
                                    sqlmodel.select(Casteller).where(Casteller.id == search_id)
                                ).first()
                            except ValueError:
                                continue # Si l'ID no és numèric, ignorem aquesta fila

                        action = str(row.get('action', 'save')).lower().strip()
                        
                        if action == 'delete' and existing:
                            session.delete(existing)
                        else:
                            # Funció auxiliar interna per netejar enters i evitar crashes
                            def to_int(val, default):
                                try:
                                    return int(float(val)) if val != "" else default
                                except:
                                    return default

                            if existing:
                                # EDITAR
                                existing.name = str(row.get('name', existing.name))
                                existing.nickname = str(row.get('nickname', existing.nickname))
                                existing.height = to_int(row.get('height'), existing.height)
                                existing.weight = to_int(row.get('weight'), existing.weight)
                                existing.talla = str(row.get('talla', existing.talla))
                                existing.comentaris = str(row.get('comentaris', existing.comentaris))
                            else:
                                # CREAR NOU
                                nou = Casteller(
                                    name=str(row.get('name', '-')),
                                    nickname=str(row.get('nickname', '')),
                                    colla=int(self.colla),
                                    height=to_int(row.get('height'), 0),
                                    weight=to_int(row.get('weight'), 0),
                                    talla=str(row.get('talla', '')),
                                    comentaris=str(row.get('comentaris', ''))
                                )
                                session.add(nou)
                    
                    session.commit()
            
            self.entry_success = "Base de dades actualitzada correctament."

        except Exception as e:
            # Si hi ha qualsevol error greu, el capturem aquí
            print(f"ERROR CRÍTIC CÀRREGA: {e}")
            self.entry_success = f"error: Error en el processament: {str(e)}"
        
        finally:
            # Això s'executa SEMPRE, encara que el codi hagi petat
            self.upload_processing = False

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
        
    @rx.var
    def llista_noms_castells(self) -> list[str]:
        "Obtén la llista de noms per al menú desplegable."
        with rx.session() as session:
            result = session.exec(sqlmodel.select(Castell.nom)).all()
            #print(f"DEBUG --> result: {result}")
            return result if result else []
        
    @rx.var
    def llista_pisos_rang(self) -> list[int]:
        # Si el castell té 7 pisos, volem [7, 6, 5, 4, 3, 2, 1] per pintar la taula de dalt a baix
        if self.dades_castell_actiu and self.dades_castell_actiu.pisos:
            return list(range(self.dades_castell_actiu.pisos, 0, -1))
        return []

    @rx.var
    def llista_rengles_rang(self) -> list[int]:
        # Si té 3 rengles, volem [1, 2, 3]
        if self.dades_castell_actiu and self.dades_castell_actiu.max_rengles:
            return list(range(1, self.dades_castell_actiu.max_rengles + 1))
        return []