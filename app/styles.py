import reflex as rx

PURPLE_DARK   = "#3C3489"
PURPLE_MID    = "#534AB7"
PURPLE_LIGHT  = "#EEEDFE"
PURPLE_BORDER = "#CECBF6"

TEAL_LIGHT  = "#E1F5EE"
TEAL_DARK   = "#085041"
CORAL_LIGHT = "#FAECE7"
CORAL_DARK  = "#712B13"
BLUE_LIGHT  = "#E6F1FB"
BLUE_DARK   = "#0C447C"

TEXT_PRIMARY   = "var(--color-text-primary)"
TEXT_SECONDARY = "var(--color-text-secondary)"
BG_PRIMARY     = "var(--color-background-primary)"
BG_SECONDARY   = "var(--color-background-secondary)"
BG_TERTIARY    = "var(--color-background-tertiary)"
BORDER         = "var(--color-border-tertiary)"
BORDER_MID     = "var(--color-border-secondary)"

base_style: dict = {
    "font_family": "var(--font-sans)",
    "background_color": BG_TERTIARY,
}

sidebar_style: dict = {
    "width": "200px",
    "min_width": "200px",
    "background_color": BG_SECONDARY,
    "border_right": f"0.5px solid {BORDER}",
    "height": "100vh",
    "display": "flex",
    "flex_direction": "column",
    "padding_top": "0",
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

nav_item_active: dict = {
    **nav_item_base,
    "color": PURPLE_DARK,
    "border_left": f"2px solid {PURPLE_DARK}",
    "background_color": PURPLE_LIGHT,
    "font_weight": "500",
}

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
    "background_color": "#EAF3DE",
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
    "color": PURPLE_DARK,
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
