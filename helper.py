import arcade

TITLE_SCREEN_BACKGROUND_COLOR = (33, 33, 33)

DEFAULT_PROPERTIES = {
"grid_length": 20,
"color_scheme": "blue",
"snake_color": "green",
"food_color": "red",
"snake_speed": 0.11
}

BOARD_COLORS = {
"blue": (arcade.color.AZURE, arcade.color.BALL_BLUE),
"brown": (arcade.color.LIGHT_BROWN, arcade.color.DARK_BROWN),
"purple": (arcade.color.LIGHT_PASTEL_PURPLE, arcade.color.DARK_PASTEL_PURPLE),
}

SNAKE_COLORS = {
    "green": arcade.color.PASTEL_GREEN
}

FOOD_COLORS = {
    "red": arcade.color.PASTEL_RED
}

BUTTON_STYLE = {
"font_name": "pressstart2p",
"font_size" : 28,
"font_color": (153, 153, 153),
"font_color_hover": (77, 208, 225),
"font_color_press" : (77, 208, 225)
}

SCORE_TEXT = {
    "color": (153, 153, 153),
    "font_size": 18,
    "align": "center",
    "font_name": "pressstart2p"
}

def initialize_ui(view, elements, style):
    for element in elements:
        element.set_style_attrs(**style)
        view.ui_manager.add_ui_element(element)


def highlight_button(view, key):
    view.buttons[view.highlighted].hovered = False
    if key in (arcade.key.W, arcade.key.UP):
        view.highlighted -= 1
    elif key in (arcade.key.S, arcade.key.DOWN):
        view.highlighted += 1     
    view.highlighted %= len(view.buttons)
    view.buttons[view.highlighted].hovered = True
