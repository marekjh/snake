import arcade
import arcade.gui
import os
import helper

SCREEN_LENGTH = 600

def main():
    window = arcade.Window(
             width=SCREEN_LENGTH, 
             height=SCREEN_LENGTH,
             title="Snake"
             )
    title_view = TitleView()
    title_view.setup()
    window.show_view(title_view)
    arcade.run()

class SnakeView(arcade.View):
    def __init__(self, properties):
        super().__init__()
        self.ui_manager = arcade.gui.UIManager()
        self.grid_length = properties["grid_length"]
        self.tile_length = SCREEN_LENGTH // self.grid_length
        self.color_scheme = helper.BOARD_COLORS[properties["color_scheme"]]
        self.snake_color = helper.SNAKE_COLORS[properties["snake_color"]]
        
    def setup(self):
        self.ui_manager.purge_ui_elements()
        self.tiles = self.initialize_grid()
        self.snake = self.initialize_snake()

    def on_draw(self):
        arcade.start_render()
        for row in self.tiles:
            row.draw()
        self.snake.draw()
    
    def initialize_snake(self):
        squares = arcade.SpriteList()
        center_row = len(self.tiles) // 2
        center_col = len(self.tiles[center_row]) // 2
        for i in range(center_col - 2, center_col + 2):
            square = arcade.SpriteSolidColor(self.tile_length, self.tile_length, self.snake_color)
            square.center_x = self.tiles[center_row][i].center_x
            square.center_y = self.tiles[center_row][i].center_y
            squares.append(square)
        return squares

    def initialize_grid(self):
        rows = []
        offset = SCREEN_LENGTH / (2 * self.grid_length)
        shade = 0
        for y in range(self.grid_length):
            tiles = arcade.SpriteList()
            for x in range(self.grid_length):
                if x == 0 or x == self.grid_length - 1 or y == 0 or y == self.grid_length - 1:
                    tile_color = helper.TITLE_SCREEN_BACKGROUND_COLOR
                else:
                    tile_color = self.color_scheme[shade]
                tile = arcade.SpriteSolidColor(self.tile_length, self.tile_length, tile_color)
                tile.center_x = offset * (2 * x + 1)
                tile.center_y = offset * (2 * y + 1)
                tiles.append(tile)
                shade = not shade
            rows.append(tiles)
            if self.grid_length % 2 == 0:
                shade = not shade 
        return rows

class TitleView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = arcade.gui.UIManager()
        self.properties = helper.DEFAULT_PROPERTIES
        self.title_image = arcade.load_texture(os.path.join("images", "title.png"))

    def __str__(self):
        return "TitleView"

    def setup(self):
        self.ui_manager.purge_ui_elements()
        self.highlighted = -1
        self.buttons = [
        Button("PLAY", SCREEN_LENGTH / 2, SCREEN_LENGTH / 3, view=self),
        Button("OPTIONS", SCREEN_LENGTH / 2, SCREEN_LENGTH / 6, view=self),
        ]
        helper.initialize_ui(self)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(
        center_x=SCREEN_LENGTH / 2,
        center_y=SCREEN_LENGTH / 2,
        width=SCREEN_LENGTH,
        height=SCREEN_LENGTH,
        texture=self.title_image,
        )

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.S, arcade.key.UP, arcade.key.DOWN):
            helper.highlight_button(self, key)
        elif key in (arcade.key.RETURN, arcade.key.SPACE):
            self.switch_view()
        
    def switch_view(self):
        self.ui_manager.purge_ui_elements()
        if self.highlighted == 0:
            snake_view = SnakeView(self.properties)
            snake_view.setup()
            self.window.show_view(snake_view)
        elif self.highlighted == 1:
            options_view = OptionsView(self.properties)
            options_view.setup()
            self.window.show_view(options_view)

    
class OptionsView(arcade.View):
    def __init__(self, properties):
        super().__init__()
        self.ui_manager = arcade.gui.UIManager()
        self.properties = properties
        
    def __str__(self):
        return "OptionsView"

    def setup(self):
        self.ui_manager.purge_ui_elements()
        test_button = Button("TESTING", SCREEN_LENGTH / 2, SCREEN_LENGTH / 2, view=self)
        self.ui_manager.add_ui_element(test_button)
    
    def on_draw(self):
        arcade.start_render()
    
    def on_key_press(self, key, modifiers):
        helper.highlight_button(self, key)
    
class Button(arcade.gui.UILabel):
    def __init__(self, text, center_x, center_y, view):
        super().__init__(text, center_x, center_y)
        self.view = view
    
    def on_click(self):
        if str(self.view) == "TitleView":
            self.view.switch_view()
        elif str(self.view) == "OptionsView":
            pass
    
    def on_hover(self):
        self.view.highlighted = self.view.buttons.index(self)
        for button in self.view.buttons:
            if button.hovered:
                button.hovered = False
        self.hovered = True
        
if __name__ == "__main__":
    main()