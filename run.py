import arcade
import arcade.gui
import os
import random
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
        self.food_color = helper.FOOD_COLORS[properties["food_color"]]
        self.v = properties["snake_speed"]

        with open("highscore.txt", "r") as f:
            self.high_score = int(f.read())
    
    def __str__(self):
        return "SnakeView"

    def setup(self):
        self.ui_manager.purge_ui_elements()
        self.timer = 0
        self.score = 0
        self.direction = "r"
        (self.tiles, self.border) = self.initialize_board()
        self.snake = self.initialize_snake()
        self.food = arcade.SpriteSolidColor(self.tile_length, self.tile_length, self.food_color)     
        self.move_food()
    
    def on_draw(self):
        arcade.start_render()
        for row in self.tiles:
            row.draw()
        self.border.draw()
        self.snake.draw()
        self.food.draw()
        self.draw_score_text()
         
    def on_update(self, delta_time):
        self.timer += delta_time
        if self.timer > self.v:
            self.timer = 0
            self.move_snake()
        if self.snake[0].collides_with_sprite(self.food):
            self.move_food()
            self.elongate_snake()
            self.score += 1
            if self.score > self.high_score:
                self.high_score = self.score
                with open("highscore.txt", "w") as f:
                    f.write(str(self.high_score))
        if self.snake[0].collides_with_list(self.border) or self.snake[0].collides_with_list(self.snake):
            self.setup()
        
    def on_key_press(self, key, modifiers):
        keys = arcade.key
        if key in (keys.W, keys.UP):
            if self.direction == "d":
                return
            self.direction = "u"
        elif key in (keys.A, keys.LEFT):
            if self.direction == "r":
                return
            self.direction = "l"
        elif key in (keys.S, keys.DOWN):
            if self.direction == "u":
                return
            self.direction = "d"
        elif key in (keys.D, keys.RIGHT):
            if self.direction == "l":
                return
            self.direction = "r"

    def move_snake(self):
        head = self.snake[0]
        for i in range(len(self.snake) - 1, 0, -1):
            self.snake[i].center_x = self.snake[i - 1].center_x
            self.snake[i].center_y = self.snake[i - 1].center_y
        if self.direction == "u":
            head.center_y += self.tile_length
        elif self.direction == "l":
            head.center_x -= self.tile_length
        elif self.direction == "d":
            head.center_y -= self.tile_length
        else:
            head.center_x += self.tile_length

    def elongate_snake(self):
        new_tail = arcade.SpriteSolidColor(self.tile_length, self.tile_length, self.snake_color)
        tail = self.snake[-1]
        adjacent = self.snake[-2]
        if tail.center_x == adjacent.center_x:
            if adjacent.center_y < tail.center_y:
                new_tail.center_x = tail.center_x
                new_tail.center_y = tail.center_y + self.tile_length
            else:
                new_tail.center_x = tail.center_x 
                new_tail.center_y = tail.center_y - self.tile_length
        else:  
            if adjacent.center_x < tail.center_x:
                new_tail.center_x = tail.center_x + self.tile_length
                new_tail.center_y = tail.center_y
            else:
                new_tail.center_x = tail.center_x - self.tile_length
                new_tail.center_y = tail.center_y
        self.snake.append(new_tail)

    def move_food(self):
        i = random.randrange(len(self.tiles))
        j = random.randrange(len(self.tiles[i]))
        self.food.center_x = self.tiles[i][j].center_x
        self.food.center_y = self.tiles[i][j].center_y

    def draw_score_text(self):
        arcade.draw_text(str(self.score), SCREEN_LENGTH / 2, SCREEN_LENGTH - self.tile_length, **helper.SCORE_TEXT)
        arcade.draw_text(f"HIGH SCORE {self.high_score}", SCREEN_LENGTH / 4, 0, **helper.SCORE_TEXT)

    def initialize_snake(self):
        squares = arcade.SpriteList()
        center_row = len(self.tiles) // 2
        center_col = len(self.tiles[center_row]) // 2
        for i in range(center_col - 2, center_col + 2):
            square = arcade.SpriteSolidColor(self.tile_length, self.tile_length, self.snake_color)
            square.center_x = self.tiles[center_row][i].center_x
            square.center_y = self.tiles[center_row][i].center_y
            squares.append(square)
        squares.reverse()
        return squares

    def initialize_board(self):
        rows = []
        border = arcade.SpriteList()
        offset = self.tile_length / 2
        shade = 0
        for y in range(self.grid_length):
            tiles = arcade.SpriteList()
            for x in range(self.grid_length):
                if x == 0 or x == self.grid_length - 1 or y == 0 or y == self.grid_length - 1:
                    tile = arcade.SpriteSolidColor(self.tile_length, self.tile_length, helper.TITLE_SCREEN_BACKGROUND_COLOR)
                    sprite_list = border
                else:
                    tile = arcade.SpriteSolidColor(self.tile_length, self.tile_length, self.color_scheme[shade])
                    sprite_list = tiles
                tile.center_x = offset * (2 * x + 1)
                tile.center_y = offset * (2 * y + 1)
                sprite_list.append(tile)
                shade = not shade
            if len(tiles) > 0:
                rows.append(tiles)
            if self.grid_length % 2 == 0:
                shade = not shade 
        
        return (rows, border)

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
        helper.initialize_ui(self, self.buttons, helper.BUTTON_STYLE)

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
        if self.highlighted == -1:
            return

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
        self.properties = properties
        
    def __str__(self):
        return "OptionsView"

    def setup(self):
        pass

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("To Do", SCREEN_LENGTH / 3, SCREEN_LENGTH / 2, arcade.color.WHITE, 
                         font_size=28, align="center", font_name=os.path.join("fonts", "pressstart2p.ttf"))
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            title_view = TitleView()
            title_view.setup()
            self.window.show_view(title_view)
    
class Button(arcade.gui.UILabel):
    def __init__(self, text, center_x, center_y, view):
        super().__init__(text, center_x, center_y)
        self.view = view
    
    def on_click(self):
        if type(self.view) == TitleView:
            self.view.switch_view()
        elif type(self.view) == OptionsView:
            pass
        elif type(self.view) == SnakeView:
            return
    
    def on_hover(self):
        self.view.highlighted = self.view.buttons.index(self)
        for button in self.view.buttons:
            if button.hovered:
                button.hovered = False
        self.hovered = True
        
if __name__ == "__main__":
    main()