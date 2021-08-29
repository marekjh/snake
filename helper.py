import arcade

TITLE_SCREEN_BACKGROUND_COLOR = (33, 33, 33)

DEFAULT_PROPERTIES = {
"grid_length": 20,
"color_scheme": "blue"
}

COLORS = {
"blue": (arcade.color.AZURE, arcade.color.BALL_BLUE),
"brown": (arcade.color.LIGHT_BROWN, arcade.color.DARK_BROWN),
"purple": (arcade.color.LIGHT_PASTEL_PURPLE, arcade.color.DARK_PASTEL_PURPLE),
}

BUTTON_STYLE = {
"font_name": "pressstart2p",
"font_size" : 28,
"font_color": (153, 153, 153),
"font_color_hover": (77, 208, 225),
"font_color_press" : (77, 208, 225)
}

def initialize_ui(view):
    for button in view.buttons:
        button.set_style_attrs(**BUTTON_STYLE)
        view.ui_manager.add_ui_element(button)


def highlight_button(view, key):
    view.buttons[view.highlighted].hovered = False
    if key in (arcade.key.W, arcade.key.UP):
        view.highlighted -= 1
    elif key in (arcade.key.S, arcade.key.DOWN):
        view.highlighted += 1     
    view.highlighted %= len(view.buttons)
    view.buttons[view.highlighted].hovered = True
