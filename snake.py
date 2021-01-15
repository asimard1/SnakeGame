"""Snake Game"""

import arcade  # Game engine
import time  # Control game speed
import random  # Place food randomly
import ctypes

# Read screen resolution
user32 = ctypes.windll.user32
FULL_WIDTH = user32.GetSystemMetrics(0)
FULL_HEIGHT = user32.GetSystemMetrics(1)

POSSIBLE_SCALES = [5, 6, 8, 10, 12, 15, 20, 24, 30, 40, 60, 120]
MAX_FOOD = 10

# Read constants from config.ini
reader = open("config.ini", "r")  # Open reader
settings = list(map(lambda x: x.split(" = "), reader.read().split("\n")))

FULLSCREEN = list(filter(lambda x: x[0] == "FULLSCREEN",
                         settings))[0][1] == "True"
DARK_MODE = list(filter(lambda x: x[0] == "DARK_MODE",
                        settings))[0][1] == "True"
TILE_POS = int(list(filter(lambda x: x[0] == "TILE_POS", settings))[0][1])
TILE_SCALE = POSSIBLE_SCALES[TILE_POS]
WIN_WIDTH = FULL_WIDTH - 300
WIN_HEIGHT = FULL_HEIGHT - 100


def update_size(bool):
    if bool:
        # If fullscreen is on
        return [FULL_WIDTH // TILE_SCALE * TILE_SCALE,
                FULL_HEIGHT // TILE_SCALE * TILE_SCALE]
    else:
        # If fullscreen is off
        return [WIN_WIDTH // TILE_SCALE * TILE_SCALE,
                WIN_HEIGHT // TILE_SCALE * TILE_SCALE]


[SCREEN_WIDTH, SCREEN_HEIGHT] = update_size(FULLSCREEN)

GAME_SPEED = SCREEN_HEIGHT / TILE_SCALE / 2

FOOD_NB = int(list(filter(lambda x: x[0] == "FOOD_NB", settings))[0][1])
HIGH_SCORE = int(list(filter(lambda x: x[0] == "HIGH_SCORE", settings))[0][1])

reader.close()  # Close reader

# Constants for the window
SCREEN_TITLE = "Snake Game"  # Title of window


class MenuView(arcade.View):
    def on_show(self):  # First time we show
        # Set background
        arcade.set_background_color(menu_color(self.window.dark_mode))

    def on_draw(self):  # To draw screen (updates at all time)
        arcade.start_render()

        # All text zones
        arcade.draw_text("Snake Game", 0, 2/3*self.window.screen_height,
                         text_color(self.window.dark_mode), 72,
                         width=self.window.screen_width, align="center")
        arcade.draw_text("by Alexandre Simard", 0, 2/3*self.window.screen_height-30,
                         text_color(self.window.dark_mode), 20,
                         width=self.window.screen_width, align="center")
        arcade.draw_text("Your High Score : " + str(self.window.high_score), 0,
                         2/5*self.window.screen_height +
                         70, text_color(self.window.dark_mode),
                         20, width=self.window.screen_width, align="center")
        arcade.draw_text("Press Enter or Space to Start", 0,
                         2/5 *
                         self.window.screen_height, text_color(
                             self.window.dark_mode),
                         40, width=self.window.screen_width, align="center")
        arcade.draw_text("Press X for controls list", 0,
                         2/5*self.window.screen_height - 50,
                         text_color(self.window.dark_mode),
                         20, width=self.window.screen_width, align="center")
        arcade.draw_text("Press Tab for Options", 0,
                         2/5*self.window.screen_height - 100,
                         text_color(self.window.dark_mode),
                         20, width=self.window.screen_width, align="center")
        arcade.draw_text("Press Escape to Exit", 0, 1/10*self.window.screen_height,
                         text_color(self.window.dark_mode),
                         20, width=self.window.screen_width, align="center")
        arcade.draw_text(dark_message(self.window.dark_mode), 5, 5,
                         text_color(self.window.dark_mode), 20)
        arcade.draw_text("Press R to Reset High Score",
                         5, self.window.screen_height - 30,
                         text_color(self.window.dark_mode), 20)

        # Update background color
        arcade.set_background_color(menu_color(self.window.dark_mode))

    def on_key_press(self, key: int, modifiers: int):  # User inputs
        if key in [arcade.key.SPACE, arcade.key.ENTER]:
            # Start Game
            game_view = MyGame()
            self.window.show_view(game_view)
        if key == arcade.key.ESCAPE:
            # Close Game
            arcade.close_window()
        if key == arcade.key.C:
            # Change colors
            self.window.dark_mode = not self.window.dark_mode
        if key == arcade.key.X:
            # Go to controls view
            controls_view = ControlsView()
            self.window.show_view(controls_view)
        if key == arcade.key.R:
            # Reset high score
            self.window.high_score = 0
        if key == arcade.key.TAB:
            options_view = OptionsView()
            self.window.show_view(options_view)


class ControlsView(arcade.View):
    def on_show(self):
        # Same color as menu
        arcade.set_background_color(menu_color(self.window.dark_mode))

    def on_draw(self):  # To draw screen (updates at all time)
        arcade.start_render()

        arcade.draw_text("Controls", 0, 4/5*self.window.screen_height,
                         text_color(self.window.dark_mode), 54,
                         width=self.window.screen_width, align="center")
        arcade.draw_text("Space or Enter : Start Game",
                         0, 8/12*self.window.screen_height,
                         text_color(self.window.dark_mode), 20,
                         width=self.window.screen_width, align="center")
        arcade.draw_text("Space, P or Pause (in game) : Pause",
                         0, 7/12*self.window.screen_height,
                         text_color(self.window.dark_mode), 20,
                         width=self.window.screen_width, align="center")
        arcade.draw_text("WASD or Arrow keys : Change Direction",
                         0, 6/12*self.window.screen_height,
                         text_color(self.window.dark_mode), 20,
                         width=self.window.screen_width, align="center")
        arcade.draw_text("Escape : Close Game", 0, 5/12*self.window.screen_height,
                         text_color(self.window.dark_mode), 20,
                         width=self.window.screen_width, align="center")
        arcade.draw_text("Escape (in game or in pause menu) : Exit to Menu",
                         0, 4/12*self.window.screen_height,
                         text_color(self.window.dark_mode), 20,
                         width=self.window.screen_width, align="center")
        arcade.draw_text("Press Space or Enter to Start Game",
                         0, 2/12*self.window.screen_height,
                         text_color(self.window.dark_mode), 20,
                         width=self.window.screen_width, align="center")
        arcade.draw_text("Press X or Escape to Exit to Menu",
                         0, 1/12*self.window.screen_height,
                         text_color(self.window.dark_mode), 20,
                         width=self.window.screen_width, align="center")

        arcade.set_background_color(menu_color(self.window.dark_mode))

    def on_key_press(self, key: int, modifiers: int):  # User inputs
        if key in [arcade.key.SPACE, arcade.key.ENTER]:
            # Start Game
            game_view = MyGame()
            self.window.show_view(game_view)
        if key == arcade.key.C:
            # Change colors
            self.window.dark_mode = not self.window.dark_mode
        if key in [arcade.key.X, arcade.key.ESCAPE]:
            # Back to menu
            menu_view = MenuView()
            self.window.show_view(menu_view)


class OptionsView(arcade.View):
    def on_show(self):
        # Same color as menu
        arcade.set_background_color(menu_color(self.window.dark_mode))

    def on_draw(self):  # To draw screen (updates at all time)
        arcade.start_render()

        arcade.draw_text("Options", 0, 4/5*self.window.screen_height,
                         text_color(self.window.dark_mode), 54,
                         width=self.window.screen_width, align="center")
        arcade.draw_text("Press F to Toggle Fullscreen",
                         0, 8/12*self.window.screen_height,
                         text_color(self.window.dark_mode), 20,
                         width=self.window.screen_width, align="center")
        arcade.draw_text("Number of Food Pieces : " + str(self.window.food_nb),
                         0, 7/12*self.window.screen_height,
                         text_color(self.window.dark_mode), 20,
                         width=self.window.screen_width, align="center")
        arcade.draw_text("Tile Scale : " + str(self.window.tile_scale),
                         0, 6/12*self.window.screen_height,
                         text_color(self.window.dark_mode), 20,
                         width=self.window.screen_width, align="center")
        arcade.draw_text("Use Left and Right to adjust number of Food Pieces",
                         0, 9/24*self.window.screen_height - 10,
                         text_color(self.window.dark_mode), 20,
                         width=self.window.screen_width, align="center")
        arcade.draw_text("Use Up and Down to adjust Tile Scale",
                         0, 7/24*self.window.screen_height + 10,
                         text_color(self.window.dark_mode), 20,
                         width=self.window.screen_width, align="center")
        arcade.draw_text("Press Space or Enter to Start Game",
                         0, 2/12*self.window.screen_height,
                         text_color(self.window.dark_mode), 20,
                         width=self.window.screen_width, align="center")
        arcade.draw_text("Press Tab or Escape to Exit to Menu",
                         0, 1/12*self.window.screen_height,
                         text_color(self.window.dark_mode), 20,
                         width=self.window.screen_width, align="center")

        arcade.set_background_color(menu_color(self.window.dark_mode))

    def on_key_press(self, key: int, modifiers: int):  # User inputs
        if key in [arcade.key.SPACE, arcade.key.ENTER]:
            # Start Game
            game_view = MyGame()
            self.window.show_view(game_view)
        if key == arcade.key.C:
            # Change colors
            self.window.dark_mode = not self.window.dark_mode
        if key in [arcade.key.TAB, arcade.key.ESCAPE]:
            # Back to menu
            menu_view = MenuView()
            self.window.show_view(menu_view)
        if key == arcade.key.F:
            self.window.full_screen = not self.window.full_screen  # update variable
            self.window.set_fullscreen(
                not self.window.fullscreen)  # update window
            [self.window.screen_width, self.window.screen_height] = update_size(
                self.window.fullscreen)
            if not self.window.fullscreen:
                self.window.set_size(self.window.screen_width,
                                     self.window.screen_height)
        if key in [arcade.key.RIGHT, arcade.key.D] and self.window.food_nb < MAX_FOOD:
            self.window.food_nb += 1
        if key in [arcade.key.LEFT, arcade.key.A] and self.window.food_nb > 1:
            self.window.food_nb -= 1

        if key in [arcade.key.UP, arcade.key.W] and self.window.tile_pos < len(POSSIBLE_SCALES) - 1:
            self.window.tile_pos += 1
            self.window.tile_scale = POSSIBLE_SCALES[self.window.tile_pos]
            self.window.game_speed = self.window.screen_height / self.window.tile_scale / 2
            self.window.set_update_rate(1/self.window.game_speed)
        if key in [arcade.key.DOWN, arcade.key.S] and self.window.tile_pos > 0:
            self.window.tile_pos -= 1
            self.window.tile_scale = POSSIBLE_SCALES[self.window.tile_pos]
            self.window.game_speed = self.window.screen_height / self.window.tile_scale / 2
            self.window.set_update_rate(1/self.window.game_speed)


class MyGame(arcade.View):
    """Main application class"""

    def on_show(self):
        # Set background
        arcade.set_background_color(game_color(self.window.dark_mode))

        self.window.snake = [[(self.window.screen_width /
                               self.window.tile_scale) // 2 * self.window.tile_scale,
                              (self.window.screen_height /
                               self.window.tile_scale) // 2 * self.window.tile_scale]]  # Position of snake

        self.window.food = random_food(
            self.window.snake, self.window.food_nb, self.window)  # Set food position
        self.window.snake_mvt = [0, 0]  # Snake doesn't move at start
        self.window.next_mvt = [0, 0]
        self.window.total_score = 0  # Reset the score
        self.window.pause = False  # Start game unpaused

    def on_draw(self):
        """Render the screen"""

        arcade.start_render()

        for f in self.window.food:
            draw_square(f, food_color(
                self.window.dark_mode), self.window.tile_scale, self.window)  # Draw food

        for block in self.window.snake:
            # Draw every snake block
            draw_square(block, snake_color(
                self.window.dark_mode), self.window.tile_scale, self.window)

        arcade.draw_text("Score : " + str(self.window.total_score), 5, 5,
                         text_color(self.window.dark_mode), 20)  # Score text

        if self.window.pause:  # Pause Menu
            arcade.draw_text("Pause", 0, 1/2*self.window.screen_height,
                             text_color(self.window.dark_mode), 80,
                             width=self.window.screen_width, align="center")  # Pause text
            arcade.draw_text("Press Escape for Menu", 0, 1/5*self.window.screen_height,
                             text_color(self.window.dark_mode),
                             20, width=self.window.screen_width, align="center")
            arcade.draw_text("Press Space, P or Pause to Resume", 0,
                             2/5 * self.window.screen_height,
                             text_color(self.window.dark_mode),
                             30, width=self.window.screen_width, align="center")

        # Update background (for dark mode)
        arcade.set_background_color(game_color(self.window.dark_mode))

    def on_update(self, delta_time):
        """Updates the game"""

        if not self.window.pause:
            # Update all snake
            self.window.snake[1:] = self.window.snake[0:-1]

            if check_death(self.window.snake, self.window):
                # Use function to check death and show death screen
                if self.window.total_score > self.window.high_score:
                    # Update high score if score is higher
                    self.window.high_score = self.window.total_score
                # Game Over Screen
                game_over_view = GameOverView()
                self.window.show_view(game_over_view)

            # If eat food
            if self.window.snake[0] in self.window.food:
                self.window.food = random_food(
                    self.window.snake, self.window.food_nb, self.window)  # New food
                self.window.snake.append(self.window.snake[0])  # Add to snake
                self.window.total_score += 1  # Add to score
                if win(self.window.snake, self.window):
                    win_view = WinView
                    self.window.show_view(win_view)

            self.window.snake[0] = [sum(x) for x in zip(
                self.window.snake[0], self.window.snake_mvt)]  # Move head
            self.window.snake_mvt = self.window.next_mvt  # Update movement with buffer
            self.window.mvt_block = False  # Remove block as we updated movement

    def on_key_press(self, key: int, modifiers: int):
        """Called when a key is pressed"""

        if not self.window.mvt_block and not self.window.pause:
            # Update movement
            self.window.snake_mvt = update_mvt(
                key, self.window.snake_mvt, self.window)

            self.window.next_mvt = self.window.snake_mvt  # So that we continue straight
            self.window.mvt_block = True  # We don't want to change movement too fast

        elif not self.window.pause:
            # Update movement
            self.window.next_mvt = update_mvt(
                key, self.window.snake_mvt, self.window)

            self.window.mvt_block = False  # This is here just in case

        if key == arcade.key.C:
            self.window.dark_mode = not self.window.dark_mode  # Change theme

        if key == arcade.key.ESCAPE:
            if self.window.pause:
                menu_view = MenuView()  # Go back to menu if we are in game
                self.window.show_view(menu_view)
            else:
                self.window.pause = True

        if key in [arcade.key.PAUSE, arcade.key.P, arcade.key.SPACE]:  # Pause/Unpause
            self.window.pause = not self.window.pause


class WinView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(win_color(self.window.dark_mode))

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text("You Won!", 0, 2/3*self.window.screen_height,
                         text_color(self.window.dark_mode), 72,
                         width=self.window.screen_width, align="center")
        arcade.draw_text("Your Score : " + str(self.window.total_score), 0,
                         1/2 *
                         self.window.screen_height, text_color(
                             self.window.dark_mode),
                         30, width=self.window.screen_width, align="center")
        arcade.draw_text("Press Enter or Space to Restart", 0,
                         2/5 *
                         self.window.screen_height, text_color(
                             self.window.dark_mode),
                         30, width=self.window.screen_width, align="center")
        arcade.draw_text("Press Escape for Menu", 0, 1/5*self.window.screen_height,
                         text_color(self.window.dark_mode),
                         20, width=self.window.screen_width, align="center")
        arcade.set_background_color(win_color(self.window.dark_mode))

    def on_key_press(self, key: int, modifiers: int):
        if key in [arcade.key.SPACE, arcade.key.ENTER]:
            # Restart game
            game_view = MyGame()
            self.window.show_view(game_view)
        if key == arcade.key.ESCAPE:
            # Back to menu
            menu_view = MenuView()
            self.window.show_view(menu_view)
        if key == arcade.key.C:
            # Change colors
            self.window.dark_mode = not self.window.dark_mode


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        # Red color
        arcade.set_background_color(gameover_color(self.window.dark_mode))

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text("Game Over", 0, 2/3*self.window.screen_height,
                         text_color(self.window.dark_mode), 72,
                         width=self.window.screen_width, align="center")
        arcade.draw_text("Your Score : " + str(self.window.total_score), 0,
                         1/2 *
                         self.window.screen_height, text_color(
                             self.window.dark_mode),
                         30, width=self.window.screen_width, align="center")
        arcade.draw_text("Press Enter or Space to Restart", 0,
                         2/5 *
                         self.window.screen_height, text_color(
                             self.window.dark_mode),
                         30, width=self.window.screen_width, align="center")
        arcade.draw_text("Press Escape for Menu", 0, 1/5*self.window.screen_height,
                         text_color(self.window.dark_mode),
                         20, width=self.window.screen_width, align="center")
        arcade.set_background_color(gameover_color(self.window.dark_mode))

    def on_key_press(self, key: int, modifiers: int):
        if key in [arcade.key.SPACE, arcade.key.ENTER]:
            # Restart game
            game_view = MyGame()
            self.window.show_view(game_view)
        if key == arcade.key.ESCAPE:
            # Back to menu
            menu_view = MenuView()
            self.window.show_view(menu_view)
        if key == arcade.key.C:
            # Change colors
            self.window.dark_mode = not self.window.dark_mode


def win(tab, window):
    return len(tab) == (window.screen_height /
                        window.tile_scale) * (window.screen_width /
                                              window.tile_scale)


def draw_square(coord, color, width, window):
    """To draw food and snake"""
    # We add TILE_SCALE/2 because the function takes the center point
    arcade.draw_rectangle_filled(
        coord[0] + window.tile_scale/2, coord[1] + window.tile_scale/2,
        width, width, color)


def random_food(tab, n, window):
    """Random food position"""
    if len(tab) != (window.screen_height /
                    window.tile_scale) * (window.screen_width /
                                          window.tile_scale):
        food = tab[0]
        food_tab = []

        # We don't want to put food on the snake
        for _ in range(min([n, (window.screen_width /
                                window.tile_scale) * (window.screen_height /
                                                      window.tile_scale) - len(tab)])):
            while food in tab or food in food_tab:
                foodx = window.screen_width * random.random() // window.tile_scale * \
                    window.tile_scale
                foody = window.screen_height * random.random() // window.tile_scale * \
                    window.tile_scale
                food = [foodx, foody]
            food_tab.append(food)

        return food_tab  # Return food positions
    else:
        return []


def check_death(tab, window):
    """Death condition"""
    # Death condition, snake collides or we get out of bounds
    if (tab[0] in tab[2:] or tab[0][0] < 0 or tab[0][1] < 0
            or tab[0][0] >= window.screen_width or tab[0][1] >= window.screen_height):
        return True


def write_to_file(tab):
    # Write settings tab to file config.ini
    for i in range(len(tab)):
        tab[i] = " = ".join(tab[i])
    new_file = "\n".join(tab)
    f = open("config.ini", "w")
    f.write(new_file)
    f.close()  # Close reader


def update_mvt(key, snake_mvt, window):
    # takes a key, the snake movement and the vector to update
    if key in [arcade.key.UP, arcade.key.W] and snake_mvt[1] >= 0:
        return [0, window.tile_scale]
    if key in [arcade.key.DOWN, arcade.key.S] and snake_mvt[1] <= 0:
        return [0, -window.tile_scale]
    if key in [arcade.key.LEFT, arcade.key.A] and snake_mvt[0] <= 0:
        return [-window.tile_scale, 0]
    if key in [arcade.key.RIGHT, arcade.key.D] and snake_mvt[0] >= 0:
        return [window.tile_scale, 0]
    else:
        return snake_mvt


def main():
    """Main application funtion"""
    # Main window
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT,
                           SCREEN_TITLE, fullscreen=FULLSCREEN,
                           update_rate=1/GAME_SPEED)

    # All global variables for game
    window.total_score = 0
    window.snake = None
    window.food = None
    window.snake_mvt = None
    window.next_mvt = [0, 0]
    window.mvt_block = False
    window.dark_mode = DARK_MODE
    window.pause = False
    window.food_nb = FOOD_NB
    window.high_score = HIGH_SCORE
    window.full_screen = FULLSCREEN
    window.screen_width = SCREEN_WIDTH
    window.screen_height = SCREEN_HEIGHT
    window.food_nb = FOOD_NB
    window.tile_pos = TILE_POS
    window.tile_scale = TILE_SCALE
    window.game_speed = GAME_SPEED

    # Start with menu
    menu_view = MenuView()
    window.show_view(menu_view)
    # This is the loop for the game
    arcade.run()

    # Update settings tab
    fullscreen_pos = settings.index(list(filter(lambda x: x[0] == "FULLSCREEN",
                                                settings))[0])
    settings[fullscreen_pos][1] = str(window.fullscreen)
    darkmode_pos = settings.index(list(filter(lambda x: x[0] == "DARK_MODE",
                                              settings))[0])
    settings[darkmode_pos][1] = str(window.dark_mode)
    tilepos_pos = settings.index(list(filter(lambda x: x[0] == "TILE_POS",
                                             settings))[0])
    settings[tilepos_pos][1] = str(window.tile_pos)
    highscore_pos = settings.index(list(filter(lambda x: x[0] == "HIGH_SCORE",
                                               settings))[0])
    settings[highscore_pos][1] = str(window.high_score)
    foodnb_pos = settings.index(list(filter(lambda x: x[0] == "FOOD_NB",
                                            settings))[0])
    settings[foodnb_pos][1] = str(window.food_nb)

    # Update config.ini file
    write_to_file(settings)


def text_color(bool):
    return arcade.csscolor.LIGHT_GRAY if bool else arcade.csscolor.BLACK


def menu_color(bool):
    return arcade.csscolor.INDIGO if bool else arcade.csscolor.LIGHT_SKY_BLUE


def game_color(bool):
    return arcade.csscolor.BLACK if bool else arcade.csscolor.BEIGE


def food_color(bool):
    return arcade.csscolor.DARK_GOLDENROD if bool else arcade.csscolor.RED


def snake_color(bool):
    return arcade.csscolor.DIM_GRAY if bool else arcade.csscolor.DARK_ORCHID


def gameover_color(bool):
    return arcade.csscolor.MAROON if bool else arcade.csscolor.RED


def win_color(bool):
    return arcade.csscolor.DARK_GREEN if bool else arcade.csscolor.LIGHT_GREEN


def dark_message(bool):
    return "Press C at any time to turn on light mode" if bool else \
        "Press C at any time to turn on dark mode"


if __name__ == "__main__":
    # Runs the main file
    main()
