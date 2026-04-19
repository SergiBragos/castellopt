# app/styles.py
import reflex as rx

# --- COLORS FIXES O CORPORATIUS ---

PURPLE_DARK   = "#3C3489"
PURPLE_MID    = "#534AB7"
PURPLE_LIGHT  = "var(--color-purple-light)" # La definirem al CSS
PURPLE_BORDER = "#B5B2D8"

TEAL_LIGHT  = "#E1F5EE"
TEAL_DARK   = "#085041"
CORAL_LIGHT = "#FAECE7"
CORAL_DARK  = "#712B13"
BLUE_LIGHT  = "#E6F1FB"
BLUE_DARK   = "#0C447C"

# --- VARIABLES DINÀMIQUES (CSS) ---
TEXT_PRIMARY   = "var(--color-text-primary)"
TEXT_SECONDARY = "var(--color-text-secondary)"
BG_PRIMARY     = "var(--color-background-primary)"
BG_SECONDARY   = "var(--color-background-secondary)"
BG_TERTIARY    = "var(--color-background-tertiary)"
BORDER         = "var(--color-border-tertiary)"
BORDER_MID     = "var(--color-border-secondary)"

base_style: dict = {
    "font_family": "var(--font-sans)",
    "background_color": "var(--color-background-tertiary)",
}

# --- ACTUALITZACIÓ D'ESTILS ---

# Sidebar ara usarà el fons secundari dinàmic
sidebar_style: dict = {
    "width": "200px",
    "min_width": "200px",
    "background_color": BG_SECONDARY, 
    "border_right": f"0.5px solid {BORDER}",
    "height": "100vh",
    "display": "flex",
    "flex_direction": "column",
}

nav_item_base: dict = {
    "display": "flex",
    "align_items": "center",
    "gap": "10px",
    "padding": "8px 16px",
    "font_size": "13px",
    "color": TEXT_SECONDARY,
    "cursor": "pointer",
    "border_left": "2px solid transparent",
    "width": "100%",
    "text_decoration": "none",
    "_hover": {
        "background_color": BG_SECONDARY,
        "color": TEXT_PRIMARY,
    },
}

# Nav Item Active ha d'anar amb compte amb el PURPLE_LIGHT en mode fosc
nav_item_active: dict = {
    **nav_item_base,
    "color": PURPLE_MID, # Millor usar MID per contrast
    "border_left": f"2px solid {PURPLE_MID}",
    "background_color": "var(--color-accent-transparent)", # Variable nova
    "font_weight": "500",
}

# Les cards ara brillaran o s'enfosquiran soles
card_style: dict = {
    "background_color": BG_PRIMARY,
    "border": f"0.5px solid {BORDER}",
    "border_radius": "12px",
    "padding": "20px",
    "margin_bottom": "16px",
    "width": "100%",
}

card_title_style: dict = {
    "font_size": "14px",
    "font_weight": "500",
    "margin_bottom": "16px",
    "color": TEXT_PRIMARY,
}

stat_card_style: dict = {
    "background_color": BG_SECONDARY,
    "border_radius": "8px",
    "padding": "16px",
    "flex": "1",
}

btn_primary: dict = {
    "background_color": PURPLE_MID,
    "color": "white",
    "border": "none",
    "border_radius": "8px",
    "padding": "8px 16px",
    "font_size": "13px",
    "font_weight": "500",
    "cursor": "pointer",
    "_hover": {"background_color": PURPLE_DARK},
}

btn_secondary: dict = {
    "background_color": "transparent",
    "color": TEXT_PRIMARY,
    "border": f"0.5px solid {BORDER_MID}",
    "border_radius": "8px",
    "padding": "8px 16px",
    "font_size": "13px",
    "font_weight": "500",
    "cursor": "pointer",
    "_hover": {"background_color": BG_SECONDARY},
}

badge_success: dict = {
    "background_color": "#B0D67D",
    "color": "#27500A",
    "font_size": "11px",
    "padding": "2px 8px",
    "border_radius": "8px",
    "font_weight": "500",
    "display": "inline-block",
}

badge_warning: dict = {
    "background_color": "#FAEEDA",
    "color": "#633806",
    "font_size": "11px",
    "padding": "2px 8px",
    "border_radius": "8px",
    "font_weight": "500",
    "display": "inline-block",
}

badge_info: dict = {
    "background_color": PURPLE_LIGHT,
    "color": "var(--color-purple-primary)",
    "font_size": "11px",
    "padding": "2px 8px",
    "border_radius": "8px",
    "font_weight": "500",
    "display": "inline-block",
}

label_style: dict = {
    "font_size": "12px",
    "color": TEXT_SECONDARY,
    "margin_bottom": "4px",
}

page_title_style: dict = {
    "font_size": "18px",
    "font_weight": "500",
    "color": TEXT_PRIMARY,
    "margin_bottom": "4px",
}

page_sub_style: dict = {
    "font_size": "13px",
    "color": TEXT_SECONDARY,
    "margin_bottom": "24px",
}