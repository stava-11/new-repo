import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Starting Template"

ENEMY_SCALING_PLAYER = 0.5
ENEMY_SCALING_COIN = 0.2
ENEMY_COUNT = 50

SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_ENEMY = 0.5
SPRITE_SCALING_PROJECTILE = 0.7
BULLET_SPEED = 5

PLAYER_VELOCITY = 2


"""
NOTES:
'A' fires one projectile
'D' fire the other projectile
Left and Right arrows control player motions
Collisions are handled to get rid of projectile and enemy when the correct hit occurs otherwise the projectile is removed
"""


class Enemy(arcade.Sprite):
    """
    This class represents the coins on our screen. It is a child class of
    the arcade library's "Sprite" class.
    """

    def reset_pos(self):

        # Reset the coin to a random spot above the screen
        self.center_y = random.randrange(SCREEN_HEIGHT + 20,
                                         SCREEN_HEIGHT + 100)
        self.center_x = random.randrange(SCREEN_WIDTH)

    def update(self):

        # Move the coin
        self.center_y -= 1

        # See if the coin has fallen off the bottom of the screen.
        # If so, reset it.
        if self.top < 0:
            self.reset_pos()
            
            
class Player():
    def __init__(self):
        self.player_sprite_list = None
        # Set up the player info
        self.player_sprite = None
        self.player_sprite_list = arcade.SpriteList()
        # Set up the player
        # Character image from kenney.nl
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 400
        self.player_sprite.center_y = 50
        self.player_sprite_list.append(self.player_sprite)
    
    def move_left(self):
        if self.player_sprite.center_x > 0:
            self.player_sprite.center_x -= PLAYER_VELOCITY
        
        
    def move_right(self):
        if self.player_sprite.center_x < SCREEN_WIDTH:
            self.player_sprite.center_x += PLAYER_VELOCITY
        
    def draw(self):
        self.player_sprite_list.draw()
    


class MyGame(arcade.Window):
    """
    Main application class.
    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.AMAZON)

        # If you have sprite lists, you should create them here,
        # and set them to None

               # Variables that will hold sprite lists
        self.player = Player()
        self.enemy_sprite_list = None
        self.projectile_sprite_list = None
        self.projectile2_sprite_list = None
        self.enemyship_sprite_list = None
        self.holding_left = False
        self.holding_right = False

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here

        # Sprite lists
        
        self.enemy_sprite_list = arcade.SpriteList()
        self.projectile_sprite_list = arcade.SpriteList()
        self.projectile2_sprite_list = arcade.SpriteList()
        self.enemyship_sprite_list = arcade.SpriteList()


        # Set up enemy
        for i in range(1, ENEMY_COUNT):
            enemy = Enemy(":resources:images/items/coinGold.png", SPRITE_SCALING_ENEMY)
        # Set its position to a random height and off screen right
            enemy.left = random.randint(0, SCREEN_WIDTH)
            enemy.top = random.randint(0, SCREEN_HEIGHT)

            self.enemy_sprite_list.append(enemy)

        # Set up enemyship
        for i in range(1, ENEMY_COUNT):
            enemyship = Enemy(":resources:images/space_shooter/playerShip2_orange.png", SPRITE_SCALING_ENEMY)
        # Set its position to a random height and off screen right
            enemyship.left = random.randint(0, SCREEN_WIDTH)
            enemyship.top = random.randint(0, SCREEN_HEIGHT)

            self.enemyship_sprite_list.append(enemyship)

        # Set up projectile
        self.projectile_sprite = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", SPRITE_SCALING_PROJECTILE)
        self.projectile_sprite_list.append(self.projectile_sprite)

        # Set up projectile2
        self.projectile2_sprite = arcade.Sprite(":resources:images/space_shooter/playerShip1_green.png", SPRITE_SCALING_PROJECTILE)
        self.projectile2_sprite_list.append(self.projectile2_sprite)
        
        # All sprite list
        self.all_sprites = arcade.SpriteList()

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Call draw() on all your sprite lists below
        self.enemy_sprite_list.draw()
        self.enemyship_sprite_list.draw()
        self.player.draw()
        self.projectile_sprite_list.draw()
        self.projectile2_sprite_list.draw()


    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        if self.holding_left == True:
            self.player.move_left()
        if self.holding_right == True:
            self.player.move_right()
        self.player.draw()
        self.enemy_sprite_list.update()
        self.enemyship_sprite_list.update()
        self.projectile_sprite_list.update()
        self.projectile2_sprite_list.update()
        
        # Loop through each colliding sprite, remove it, and add to the score.
        for enemy in self.enemy_sprite_list: 
            for projectile in self.projectile_sprite_list:
                if arcade.check_for_collision(enemy, projectile):
                    self.enemy_sprite_list.remove(enemy)
                    self.projectile_sprite_list.remove(projectile)
            for projectile in self.projectile2_sprite_list:
                if arcade.check_for_collision(enemy, projectile):
                    self.projectile2_sprite_list.remove(projectile)
                
                    
        for enemy in self.enemyship_sprite_list: 
            for projectile in self.projectile2_sprite_list:
                if arcade.check_for_collision(enemy, projectile):
                    self.enemyship_sprite_list.remove(enemy)
                    self.projectile2_sprite_list.remove(projectile)
            for projectile in self.projectile_sprite_list:
                if arcade.check_for_collision(enemy, projectile):
                    self.projectile_sprite_list.remove(projectile)

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.
        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        # self.projectile_sprite.center_y = self.projectile_sprite.center_y + 5
        if key == arcade.key.A:
                # Create a bullet
            self.projectile_sprite = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", SPRITE_SCALING_PROJECTILE)

            # The image points to the right, and we want it to point up. So
            # rotate it.
            self.projectile_sprite.angle = 90

            # Give the bullet a speed
            self.projectile_sprite.change_y = BULLET_SPEED

            # Position the bullet
            self.projectile_sprite.center_x = self.player.player_sprite.center_x
            self.projectile_sprite.bottom = self.player.player_sprite.top

            # Add the bullet to the appropriate lists
            self.projectile_sprite_list.append(self.projectile_sprite)
            
        if key == arcade.key.D:
                # Create a bullet
            self.projectile2_sprite = arcade.Sprite(":resources:images/space_shooter/playerShip1_green.png", SPRITE_SCALING_PROJECTILE)

            # The image points to the right, and we want it to point up. So
            # rotate it.
            self.projectile2_sprite.angle = 90

            # Give the bullet a speed
            self.projectile2_sprite.change_y = BULLET_SPEED

            # Position the bullet
            self.projectile2_sprite.center_x = self.player.player_sprite.center_x
            self.projectile2_sprite.bottom = self.player.player_sprite.top

            # Add the bullet to the appropriate lists
            self.projectile2_sprite_list.append(self.projectile2_sprite)
        
        if key == arcade.key.LEFT:
            self.holding_left = True

        if key == arcade.key.RIGHT:
            self.holding_right = True

 

    def check_keys(self):
        """
        Checks to see if the user is holding down an
        arrow key, and if so, takes appropriate action.
        """
        if self.holding_left:
            self.ship.turn_left()

        if self.holding_right:
            self.ship.turn_right()
            
        
        

    def on_key_release(self, key, key_modifiers):
        """
        Called when a key is released. Sets the state of
        the arrow key as being not held anymore.
        :param key: The key that was pressed
        :param key_modifiers: Things like shift, ctrl, etc
        """
        if key == arcade.key.LEFT:
            self.holding_left = False

        if key == arcade.key.RIGHT:
            self.holding_right = False
    
   
        

def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()