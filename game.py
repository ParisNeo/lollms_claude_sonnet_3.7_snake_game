import pygame
import sys
import random
from pathlib import Path
import math
from enum import Enum

# Initialize pygame
pygame.init()

# Game constants with RIDICULOUS names because why not?
SCREEN_CHUNKY_MONKEY_WIDTH = 800
SCREEN_ABSOLUTELY_BONKERS_HEIGHT = 600
GRID_TEENY_WEENY_SIZE = 20
SNAKE_SPEEDY_WEEDY = 10
FONT_ABSOLUTELY_FABULOUS = pygame.font.SysFont('Comic Sans MS', 24)  # The most professional font ever!
TITLE_FONT_CHONKY_BOI = pygame.font.SysFont('Comic Sans MS', 48)

# Colors with names that would make a crayon manufacturer weep
BLACK_HOLE_SUN = (0, 0, 0)
WHITE_AS_MY_PROGRAMMING_SKILLS = (255, 255, 255)
RED_LIKE_MY_DEBUG_ERRORS = (255, 0, 0)
GREEN_LIKE_MONEY_I_DONT_HAVE = (0, 255, 0)
BLUE_LIKE_MY_MOOD_WHEN_CODING = (0, 0, 255)
YELLOW_BANANA_PHONE = (255, 255, 0)
PURPLE_NURPLE = (128, 0, 128)
TEAL_NO_BIG_DEAL = (0, 128, 128)
ORANGE_YOU_GLAD_I_DIDNT_SAY_BANANA = (255, 165, 0)

# Game states that are way too dramatic
class GameState(Enum):
    MAIN_MENU_OF_DESTINY = 0
    PLAYING_FOR_YOUR_LIFE = 1
    GAME_OVER_DUDE_SO_SAD = 2
    HELP_ME_OBI_WAN = 3
    SETTINGS_FOR_PICKY_PEOPLE = 4
    CREDITS_TO_THE_AWESOME = 5
    PAUSED_FOR_DRAMATIC_EFFECT = 6

# Initialize screen
screen = pygame.display.set_mode((SCREEN_CHUNKY_MONKEY_WIDTH, SCREEN_ABSOLUTELY_BONKERS_HEIGHT))
pygame.display.set_caption("SUPER SLITHERY SNAKE SIMULATOR 5000")

# Clock to control game speed (and your destiny)
clock = pygame.time.Clock()

# Game variables with excessive enthusiasm
current_state = GameState.MAIN_MENU_OF_DESTINY
snake_color = GREEN_LIKE_MONEY_I_DONT_HAVE
food_color = RED_LIKE_MY_DEBUG_ERRORS
background_color = BLACK_HOLE_SUN
difficulty_level = "TOTALLY AVERAGE"
selected_menu_item = 0
snake_party_hats = False  # Easter egg setting - gives snake segments party hats!

class SnakeSegment:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wiggle_offset = 0  # For that extra WIGGLE

class SnakeGame:
    def __init__(self):
        self.reset_game()
        
    def reset_game(self):
        self.snake = [SnakeSegment(SCREEN_CHUNKY_MONKEY_WIDTH // 2, SCREEN_ABSOLUTELY_BONKERS_HEIGHT // 2)]
        self.direction = (GRID_TEENY_WEENY_SIZE, 0)
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        self.bonus_food = None
        self.bonus_food_timer = 0
        self.snake_length_goal = 5  # For level progression
        self.current_level = 1
        self.powerup = None
        self.powerup_effect = None
        self.powerup_timer = 0
        
    def generate_food(self):
        while True:
            x = random.randrange(0, SCREEN_CHUNKY_MONKEY_WIDTH, GRID_TEENY_WEENY_SIZE)
            y = random.randrange(0, SCREEN_ABSOLUTELY_BONKERS_HEIGHT, GRID_TEENY_WEENY_SIZE)
            
            # Check if food would spawn on snake
            if not any(segment.x == x and segment.y == y for segment in self.snake):
                return (x, y)
    
    def update(self):
        if self.game_over:
            return
            
        # Move snake
        head = self.snake[0]
        new_head = SnakeSegment(head.x + self.direction[0], head.y + self.direction[1])
        
        # Check for wall collision (with hilarious death message)
        if (new_head.x < 0 or new_head.x >= SCREEN_CHUNKY_MONKEY_WIDTH or 
            new_head.y < 0 or new_head.y >= SCREEN_ABSOLUTELY_BONKERS_HEIGHT):
            self.game_over = True
            return
            
        # Check for self collision (with equally hilarious death message)
        if any(segment.x == new_head.x and segment.y == new_head.y for segment in self.snake):
            self.game_over = True
            return
            
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check for food collision
        if new_head.x == self.food[0] and new_head.y == self.food[1]:
            self.score += 10
            self.food = self.generate_food()
            
            # Add random wiggle to each segment for EXTRA FUN
            for segment in self.snake:
                segment.wiggle_offset = random.randint(-3, 3)
                
            # Check for level progression
            if len(self.snake) >= self.snake_length_goal:
                self.current_level += 1
                self.snake_length_goal += 5
                
            # Randomly generate powerup (1 in 5 chance)
            if random.random() < 0.2 and not self.powerup:
                self.generate_powerup()
                
            # Sometimes spawn bonus food (1 in 3 chance)
            if random.random() < 0.3 and not self.bonus_food:
                self.generate_bonus_food()
        else:
            # Remove tail if no food eaten
            self.snake.pop()
            
        # Check for bonus food collision
        if self.bonus_food and new_head.x == self.bonus_food[0] and new_head.y == self.bonus_food[1]:
            self.score += 25  # SUPER BONUS POINTS!
            self.bonus_food = None
            
        # Update bonus food timer
        if self.bonus_food:
            self.bonus_food_timer += 1
            if self.bonus_food_timer > 100:  # Bonus food disappears after ~10 seconds
                self.bonus_food = None
                self.bonus_food_timer = 0
                
        # Check for powerup collision
        if self.powerup and new_head.x == self.powerup[0] and new_head.y == self.powerup[1]:
            self.activate_powerup()
            self.powerup = None
            
        # Update powerup timer
        if self.powerup_effect:
            self.powerup_timer += 1
            if self.powerup_timer > 200:  # Powerup lasts ~20 seconds
                self.powerup_effect = None
                self.powerup_timer = 0
    
    def generate_bonus_food(self):
        self.bonus_food = self.generate_food()
        self.bonus_food_timer = 0
        
    def generate_powerup(self):
        self.powerup = self.generate_food()
        
    def activate_powerup(self):
        powerup_types = ["SPEED_BOOST", "SLOW_MOTION", "RAINBOW_SNAKE", "INVINCIBILITY"]
        self.powerup_effect = random.choice(powerup_types)
        self.powerup_timer = 0
        
    def draw(self, screen):
        # Draw background
        screen.fill(background_color)
        
        # Draw snake with wiggles and maybe party hats (because WHY NOT?)
        for i, segment in enumerate(self.snake):
            wiggle = 0
            if i > 0:  # Only wiggle body segments
                wiggle = segment.wiggle_offset
                
            color = snake_color
            
            # Rainbow snake powerup effect
            if self.powerup_effect == "RAINBOW_SNAKE":
                hue = (pygame.time.get_ticks() // 50 + i * 10) % 360
                r, g, b = self.hsv_to_rgb(hue, 1, 1)
                color = (r, g, b)
                
            snake_rect = pygame.Rect(segment.x + wiggle, segment.y + wiggle, 
                                     GRID_TEENY_WEENY_SIZE, GRID_TEENY_WEENY_SIZE)
            pygame.draw.rect(screen, color, snake_rect)
            
            # Draw silly eyes on head
            if i == 0:
                eye_size = GRID_TEENY_WEENY_SIZE // 4
                eye1_x = segment.x + GRID_TEENY_WEENY_SIZE // 4
                eye2_x = segment.x + GRID_TEENY_WEENY_SIZE - GRID_TEENY_WEENY_SIZE // 4 - eye_size
                eye_y = segment.y + GRID_TEENY_WEENY_SIZE // 4
                
                pygame.draw.ellipse(screen, WHITE_AS_MY_PROGRAMMING_SKILLS, 
                                    (eye1_x, eye_y, eye_size, eye_size))
                pygame.draw.ellipse(screen, WHITE_AS_MY_PROGRAMMING_SKILLS,
                                    (eye2_x, eye_y, eye_size, eye_size))
                
            # Draw party hats if enabled (ESSENTIAL FEATURE)
            if snake_party_hats and i % 3 == 0:
                hat_points = [
                    (segment.x + GRID_TEENY_WEENY_SIZE // 2, segment.y - 10),
                    (segment.x + 2, segment.y),
                    (segment.x + GRID_TEENY_WEENY_SIZE - 2, segment.y)
                ]
                pygame.draw.polygon(screen, YELLOW_BANANA_PHONE, hat_points)
        
        # Draw food
        food_rect = pygame.Rect(self.food[0], self.food[1], GRID_TEENY_WEENY_SIZE, GRID_TEENY_WEENY_SIZE)
        pygame.draw.rect(screen, food_color, food_rect)
        
        # Draw pulsating bonus food
        if self.bonus_food:
            pulse = abs(math.sin(pygame.time.get_ticks() / 200)) * 5  # Pulsating effect
            bonus_rect = pygame.Rect(
                self.bonus_food[0] - pulse, 
                self.bonus_food[1] - pulse, 
                GRID_TEENY_WEENY_SIZE + pulse * 2, 
                GRID_TEENY_WEENY_SIZE + pulse * 2
            )
            pygame.draw.rect(screen, ORANGE_YOU_GLAD_I_DIDNT_SAY_BANANA, bonus_rect)
            
        # Draw powerup
        if self.powerup:
            powerup_rect = pygame.Rect(
                self.powerup[0], self.powerup[1],
                GRID_TEENY_WEENY_SIZE, GRID_TEENY_WEENY_SIZE
            )
            pygame.draw.rect(screen, PURPLE_NURPLE, powerup_rect)
            
            # Draw a ? in the middle of powerup
            question_text = FONT_ABSOLUTELY_FABULOUS.render("?", True, WHITE_AS_MY_PROGRAMMING_SKILLS)
            question_rect = question_text.get_rect(center=(
                self.powerup[0] + GRID_TEENY_WEENY_SIZE // 2,
                self.powerup[1] + GRID_TEENY_WEENY_SIZE // 2
            ))
            screen.blit(question_text, question_rect)
        
        # Draw HUD (with EXTRA enthusiasm)
        score_text = FONT_ABSOLUTELY_FABULOUS.render(f"Score: {self.score} (WOW!)", True, WHITE_AS_MY_PROGRAMMING_SKILLS)
        screen.blit(score_text, (10, 10))
        
        level_text = FONT_ABSOLUTELY_FABULOUS.render(f"Level: {self.current_level} (AMAZING!)", True, WHITE_AS_MY_PROGRAMMING_SKILLS)
        screen.blit(level_text, (10, 40))
        
        # Display active powerup with EXCITEMENT
        if self.powerup_effect:
            powerup_text = FONT_ABSOLUTELY_FABULOUS.render(
                f"POWERUP: {self.powerup_effect}!!!", True, YELLOW_BANANA_PHONE)
            screen.blit(powerup_text, (SCREEN_CHUNKY_MONKEY_WIDTH // 2 - 100, 10))
    
    # Helper function for rainbow snake
    def hsv_to_rgb(self, h, s, v):
        h = h / 360
        i = math.floor(h * 6)
        f = h * 6 - i
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        
        r, g, b = 0, 0, 0
        if i % 6 == 0: r, g, b = v, t, p
        elif i % 6 == 1: r, g, b = q, v, p
        elif i % 6 == 2: r, g, b = p, v, t
        elif i % 6 == 3: r, g, b = p, q, v
        elif i % 6 == 4: r, g, b = t, p, v
        elif i % 6 == 5: r, g, b = v, p, q
        
        return int(r * 255), int(g * 255), int(b * 255)

# Create game instance
game = SnakeGame()

# Helper functions for menu rendering with PIZZAZZ
def draw_main_menu():
    screen.fill(BLACK_HOLE_SUN)
    
    # Animated title with bouncing effect
    bounce_offset = math.sin(pygame.time.get_ticks() / 300) * 10
    title_text = TITLE_FONT_CHONKY_BOI.render("SUPER SLITHERY", True, GREEN_LIKE_MONEY_I_DONT_HAVE)    
    title_text2 = TITLE_FONT_CHONKY_BOI.render("SNAKE SIMULATOR 5000", True, GREEN_LIKE_MONEY_I_DONT_HAVE)
    screen.blit(title_text, (SCREEN_CHUNKY_MONKEY_WIDTH // 2 - title_text.get_width() // 2, 
                             100 + bounce_offset))
    screen.blit(title_text2, (SCREEN_CHUNKY_MONKEY_WIDTH // 2 - title_text2.get_width() // 2, 
                              160 + bounce_offset))
    
    # Draw a ridiculous snake icon
    snake_icon_x = SCREEN_CHUNKY_MONKEY_WIDTH // 2
    snake_icon_y = 50 + bounce_offset
    
    # Draw snake body segments in a silly pattern
    for i in range(5):
        offset = math.sin(pygame.time.get_ticks() / 200 + i) * 15
        pygame.draw.circle(screen, GREEN_LIKE_MONEY_I_DONT_HAVE, 
                          (snake_icon_x + offset, snake_icon_y), 15)
    
    # Snake googly eyes (ESSENTIAL)
    pygame.draw.circle(screen, WHITE_AS_MY_PROGRAMMING_SKILLS, 
                      (snake_icon_x + 25, snake_icon_y - 10), 8)
    pygame.draw.circle(screen, BLACK_HOLE_SUN, 
                      (snake_icon_x + 25 + math.sin(pygame.time.get_ticks() / 500) * 3, 
                       snake_icon_y - 10 + math.cos(pygame.time.get_ticks() / 500) * 3), 4)
    
    # Menu items with OVER-THE-TOP selection indicators
    menu_items = ["Start Game", "Settings", "Help", "Credits", "Quit"]
    
    for i, item in enumerate(menu_items):
        color = WHITE_AS_MY_PROGRAMMING_SKILLS
        prefix = "   "
        
        if i == selected_menu_item:
            color = YELLOW_BANANA_PHONE
            wiggle = math.sin(pygame.time.get_ticks() / 100) * 5
            prefix = ">> "  # Super professional selection indicator
        else:
            wiggle = 0
            
        item_text = FONT_ABSOLUTELY_FABULOUS.render(f"{prefix}{item}", True, color)
        screen.blit(item_text, (SCREEN_CHUNKY_MONKEY_WIDTH // 2 - 100 + wiggle, 
                                250 + i * 50))

def draw_help_screen():
    screen.fill(BLACK_HOLE_SUN)
    
    title_text = TITLE_FONT_CHONKY_BOI.render("HELP?! YOU NEED HELP?!", True, BLUE_LIKE_MY_MOOD_WHEN_CODING)
    screen.blit(title_text, (SCREEN_CHUNKY_MONKEY_WIDTH // 2 - title_text.get_width() // 2, 50))
    
    # Draw help instructions with RIDICULOUSLY detailed explanations
    instructions = [
        "- Arrow keys to move the snake (yes, REALLY!)",
        "- Eat red food to grow (mind = blown)",
        "- Don't hit walls (they're like SUPER solid)",
        "- Don't eat yourself (that's just gross)",
        "- Orange bonus food = MEGA POINTS (disappears fast!)",
        "- Purple powerups do CRAZY things (try them!)",
        "- Press P to pause (for bathroom breaks)",
        "- Press ESC to return to main menu (duh!)",
        "",
        "SECRET: Press 'H' during gameplay for party hats!",
    ]
    
    for i, line in enumerate(instructions):
        # Make even lines wiggle for NO REASON AT ALL
        wiggle = math.sin(pygame.time.get_ticks() / 300) * 5 if i % 2 == 0 else 0
        line_text = FONT_ABSOLUTELY_FABULOUS.render(line, True, WHITE_AS_MY_PROGRAMMING_SKILLS)
        screen.blit(line_text, (100 + wiggle, 150 + i * 40))
    
    # Animated back button because static buttons are BORING
    back_text = FONT_ABSOLUTELY_FABULOUS.render("Back to Menu (click here, genius)", True, 
                                            YELLOW_BANANA_PHONE)
    back_rect = back_text.get_rect(center=(SCREEN_CHUNKY_MONKEY_WIDTH // 2, 
                                         SCREEN_ABSOLUTELY_BONKERS_HEIGHT - 50))
    
    # Add a pulsating effect because WHY NOT
    pulse = abs(math.sin(pygame.time.get_ticks() / 300)) * 10
    pygame.draw.rect(screen, TEAL_NO_BIG_DEAL, 
                    (back_rect.x - pulse/2, back_rect.y - pulse/2, 
                     back_rect.width + pulse, back_rect.height + pulse), 
                    border_radius=10)
    
    screen.blit(back_text, back_rect)

def draw_settings_screen():
    screen.fill(BLACK_HOLE_SUN)
    
    title_text = TITLE_FONT_CHONKY_BOI.render("FANCYPANTS SETTINGS", True, PURPLE_NURPLE)
    screen.blit(title_text, (SCREEN_CHUNKY_MONKEY_WIDTH // 2 - title_text.get_width() // 2, 50))
    
    # Settings with OUTRAGEOUS descriptions
    settings = [
        "Snake Color:",
        "Food Color:",
        "Background Color:",
        "Difficulty:",
        "Party Mode:"
    ]
    
    # Available options with equally OUTRAGEOUS names
    color_options = [
        ["Green (Boring)", "Blue (Cool)", "Yellow (Banana!)", "Rainbow (PARTY!)"],
        ["Red (Classic)", "Purple (Fancy)", "Teal (Hipster)", "Orange (LOUD)"],
        ["Black (Emo)", "Navy (Sophisticated)", "Gray (Meh)", "Dark Purple (Mysterious)"],
        ["Easy Peasy", "TOTALLY AVERAGE", "Hard (Ouch!)", "NIGHTMARE MODE (RIP)"],
        ["OFF (Boooring)", "ON (WOOOOOO!)"]
    ]
    
    # Current selected options (indexes)
    current_options = [
        ["Green (Boring)", "Blue (Cool)", "Yellow (Banana!)", "Rainbow (PARTY!)"].index(
            "Green (Boring)" if snake_color == GREEN_LIKE_MONEY_I_DONT_HAVE else
            "Blue (Cool)" if snake_color == BLUE_LIKE_MY_MOOD_WHEN_CODING else
            "Yellow (Banana!)" if snake_color == YELLOW_BANANA_PHONE else "Rainbow (PARTY!)"),
        
        ["Red (Classic)", "Purple (Fancy)", "Teal (Hipster)", "Orange (LOUD)"].index(
            "Red (Classic)" if food_color == RED_LIKE_MY_DEBUG_ERRORS else
            "Purple (Fancy)" if food_color == PURPLE_NURPLE else
            "Teal (Hipster)" if food_color == TEAL_NO_BIG_DEAL else "Orange (LOUD)"),
        
        ["Black (Emo)", "Navy (Sophisticated)", "Gray (Meh)", "Dark Purple (Mysterious)"].index(
            "Black (Emo)" if background_color == BLACK_HOLE_SUN else
            "Navy (Sophisticated)" if background_color == (0, 0, 50) else
            "Gray (Meh)" if background_color == (50, 50, 50) else "Dark Purple (Mysterious)"),
        
        ["Easy Peasy", "TOTALLY AVERAGE", "Hard (Ouch!)", "NIGHTMARE MODE (RIP)"].index(
            difficulty_level),
        
        1 if snake_party_hats else 0
    ]
    
    # Draw settings with WILD selection animations
    for i, setting in enumerate(settings):
        setting_text = FONT_ABSOLUTELY_FABULOUS.render(setting, True, WHITE_AS_MY_PROGRAMMING_SKILLS)
        screen.blit(setting_text, (100, 150 + i * 70))
        
        # Draw options for this setting
        for j, option in enumerate(color_options[i]):
            color = WHITE_AS_MY_PROGRAMMING_SKILLS
            prefix = "[ ]"
            
            if j == current_options[i]:
                color = YELLOW_BANANA_PHONE
                wiggle = math.sin(pygame.time.get_ticks() / 100) * 3
                prefix = "[X]"  # Professional checkbox UI
            else:
                wiggle = 0
                
            option_text = FONT_ABSOLUTELY_FABULOUS.render(f"{prefix} {option}", True, color)
            screen.blit(option_text, (250 + j * 180 + wiggle, 150 + i * 70))
    
    # Back button with UNNECESSARY animation
    back_text = FONT_ABSOLUTELY_FABULOUS.render("Save & Go Back", True, YELLOW_BANANA_PHONE)
    back_rect = back_text.get_rect(center=(SCREEN_CHUNKY_MONKEY_WIDTH // 2, 
                                         SCREEN_ABSOLUTELY_BONKERS_HEIGHT - 50))
    
    # Spinning effect because normal buttons are for SQUARES
    spin_offset_x = math.sin(pygame.time.get_ticks() / 500) * 5
    spin_offset_y = math.cos(pygame.time.get_ticks() / 500) * 5
    
    pygame.draw.rect(screen, TEAL_NO_BIG_DEAL, 
                    (back_rect.x - 10 + spin_offset_x, 
                     back_rect.y - 10 + spin_offset_y, 
                     back_rect.width + 20, 
                     back_rect.height + 20), 
                    border_radius=10)
    
    screen.blit(back_text, back_rect)

def draw_credits_screen():
    screen.fill(BLACK_HOLE_SUN)
    
    title_text = TITLE_FONT_CHONKY_BOI.render("CREDITS (THE AWESOME PEOPLE)", True, ORANGE_YOU_GLAD_I_DIDNT_SAY_BANANA)
    screen.blit(title_text, (SCREEN_CHUNKY_MONKEY_WIDTH // 2 - title_text.get_width() // 2, 50))
    
    # Credits with OVER-THE-TOP praise
    credits = [
        "Developed by the DYNAMIC DUO:",
        "",
        "ParisNeo - The LEGENDARY Code Architect",
        "      (Master of Python and Keeper of Bugs)",
        "",
        "LoLLMs - The ASTOUNDING AI Assistant",
        "      (Writes code and silly comments with equal skill)",
        "",
        "No snakes were harmed in the making of this game.",
        "(But several keyboards were brutally abused)",
        "",
        "SUPER SLITHERY SNAKE SIMULATOR 5000",
        "Copyright © Whenever - All Rights Reserved",
        "Patent Pending (Not Really)"
    ]
    
    for i, line in enumerate(credits):
        # Add random colors to important lines because CONSISTENCY IS BORING
        if "ParisNeo" in line or "LoLLMs" in line:
            color = YELLOW_BANANA_PHONE
            wave = math.sin(pygame.time.get_ticks() / 200 + i) * 10
        elif "SUPER SLITHERY" in line:
            color = GREEN_LIKE_MONEY_I_DONT_HAVE
            wave = math.sin(pygame.time.get_ticks() / 300) * 5
        else:
            color = WHITE_AS_MY_PROGRAMMING_SKILLS
            wave = 0
            
        line_text = FONT_ABSOLUTELY_FABULOUS.render(line, True, color)
        screen.blit(line_text, (100 + wave, 150 + i * 30))
    
    # Back button with ridiculous animation
    back_text = FONT_ABSOLUTELY_FABULOUS.render("Back to Menu", True, YELLOW_BANANA_PHONE)
    back_rect = back_text.get_rect(center=(SCREEN_CHUNKY_MONKEY_WIDTH // 2, 
                                         SCREEN_ABSOLUTELY_BONKERS_HEIGHT - 50))
    
    # Rainbow pulsing effect for the back button
    hue = (pygame.time.get_ticks() // 20) % 360
    r, g, b = game.hsv_to_rgb(hue, 1, 1)
    
    pygame.draw.rect(screen, (r, g, b), 
                    (back_rect.x - 10, back_rect.y - 10, 
                     back_rect.width + 20, back_rect.height + 20), 
                    border_radius=10)
    
    screen.blit(back_text, back_rect)

def draw_game_over_screen():
    # Semi-transparent overlay
    overlay = pygame.Surface((SCREEN_CHUNKY_MONKEY_WIDTH, SCREEN_ABSOLUTELY_BONKERS_HEIGHT))
    overlay.set_alpha(150)
    overlay.fill(BLACK_HOLE_SUN)
    screen.blit(overlay, (0, 0))
    
    # Game Over text with DRAMATIC shaking effect
    shake_x = random.randint(-5, 5)
    shake_y = random.randint(-5, 5)
    
    gameover_text = TITLE_FONT_CHONKY_BOI.render("GAME OVER", True, RED_LIKE_MY_DEBUG_ERRORS)
    screen.blit(gameover_text, (SCREEN_CHUNKY_MONKEY_WIDTH // 2 - gameover_text.get_width() // 2 + shake_x, 
                              SCREEN_ABSOLUTELY_BONKERS_HEIGHT // 3 + shake_y))
    
    # Show final score with EXCESSIVE praise
    score_texts = [
        f"Your Score: {game.score}",
        get_score_comment(game.score),
        "",
        "Press SPACE to restart",
        "Press ESC for main menu"
    ]
    
    for i, text in enumerate(score_texts):
        if i == 1:  # Make the comment extra flashy
            color_value = abs(math.sin(pygame.time.get_ticks() / 300)) * 255
            text_color = (color_value, color_value, 0)  # Flashing gold
        else:
            text_color = WHITE_AS_MY_PROGRAMMING_SKILLS
            
        rendered_text = FONT_ABSOLUTELY_FABULOUS.render(text, True, text_color)
        screen.blit(rendered_text, (SCREEN_CHUNKY_MONKEY_WIDTH // 2 - rendered_text.get_width() // 2, 
                                  SCREEN_ABSOLUTELY_BONKERS_HEIGHT // 2 + i * 40))

def get_score_comment(score):
    if score == 0:
        return "WOW... JUST... WOW. (Not the good kind)"
    elif score < 50:
        return "ARE YOU EVEN TRYING?? (Seriously?)"
    elif score < 100:
        return "NOT BAD FOR A HUMAN! (Low bar, really)"
    elif score < 200:
        return "PRETTY GOOD! (Mom would be proud)"
    elif score < 300:
        return "SNAKE MASTER! (Business cards incoming)"
    elif score < 500:
        return "SLITHERING SUPERSTAR!! (Call the newspapers)"
    else:
        return "GOD OF SNAKES!!!! (All hail the new reptile royalty!)"

def draw_pause_screen():
    # Semi-transparent overlay
    overlay = pygame.Surface((SCREEN_CHUNKY_MONKEY_WIDTH, SCREEN_ABSOLUTELY_BONKERS_HEIGHT))
    overlay.set_alpha(150)
    overlay.fill(BLACK_HOLE_SUN)
    screen.blit(overlay, (0, 0))

    # DRAMATIC pause text
    pause_text = TITLE_FONT_CHONKY_BOI.render("GAME PAUSED", True, YELLOW_BANANA_PHONE)
    
    # Make the pause text BOUNCE because static text is boring
    bounce_offset = math.sin(pygame.time.get_ticks() / 300) * 10
    
    screen.blit(pause_text, (SCREEN_CHUNKY_MONKEY_WIDTH // 2 - pause_text.get_width() // 2, 
                          SCREEN_ABSOLUTELY_BONKERS_HEIGHT // 3 + bounce_offset))

    # Pause menu options
    pause_options = [
        "Press P to Resume (and face your destiny)",
        "Press R to Restart (admit defeat)",
        "Press ESC for Main Menu (chicken out)"
    ]

    for i, option in enumerate(pause_options):
        # Make each option pulse at different rates because WHY NOT
        pulse_value = abs(math.sin(pygame.time.get_ticks() / (300 + i * 100))) * 255
        option_color = (255, pulse_value, pulse_value) if i == 0 else (pulse_value, pulse_value, 255)
        
        option_text = FONT_ABSOLUTELY_FABULOUS.render(option, True, option_color)
        screen.blit(option_text, (SCREEN_CHUNKY_MONKEY_WIDTH // 2 - option_text.get_width() // 2, 
                              SCREEN_ABSOLUTELY_BONKERS_HEIGHT // 2 + i * 50))

# Apply changes based on settings
def apply_settings(selected_snake, selected_food, selected_bg, selected_diff, selected_party):
    global snake_color, food_color, background_color, difficulty_level, snake_party_hats

    # Snake colors
    if selected_snake == 0:
        snake_color = GREEN_LIKE_MONEY_I_DONT_HAVE
    elif selected_snake == 1:
        snake_color = BLUE_LIKE_MY_MOOD_WHEN_CODING
    elif selected_snake == 2:
        snake_color = YELLOW_BANANA_PHONE
    elif selected_snake == 3:
        # Rainbow mode handled in drawing
        food_color = RED_LIKE_MY_DEBUG_ERRORS

    # Food colors
    if selected_food == 0:
        food_color = RED_LIKE_MY_DEBUG_ERRORS
    elif selected_food == 1:
        food_color = PURPLE_NURPLE
    elif selected_food == 2:
        food_color = TEAL_NO_BIG_DEAL
    elif selected_food == 3:
        food_color = ORANGE_YOU_GLAD_I_DIDNT_SAY_BANANA

    # Background colors
    if selected_bg == 0:
        background_color = BLACK_HOLE_SUN
    elif selected_bg == 1:
        background_color = (0, 0, 50)  # Navy
    elif selected_bg == 2:
        background_color = (50, 50, 50)  # Gray
    elif selected_bg == 3:
        background_color = (30, 0, 30)  # Dark Purple

    # Difficulty levels affect game speed
    difficulty_options = ["Easy Peasy", "TOTALLY AVERAGE", "Hard (Ouch!)", "NIGHTMARE MODE (RIP)"]
    difficulty_level = difficulty_options[selected_diff]
    
    # Party mode
    snake_party_hats = selected_party == 1

# Main game loop (where the MAGIC happens)
running = True
while running:
    # Check events with EXCITING comments
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if current_state == GameState.MAIN_MENU_OF_DESTINY:
                if event.key == pygame.K_UP:
                    selected_menu_item = (selected_menu_item - 1) % 5
                elif event.key == pygame.K_DOWN:
                    selected_menu_item = (selected_menu_item + 1) % 5
                elif event.key == pygame.K_RETURN:
                    if selected_menu_item == 0:  # Start Game
                        current_state = GameState.PLAYING_FOR_YOUR_LIFE
                        game.reset_game()
                    elif selected_menu_item == 1:  # Settings
                        current_state = GameState.SETTINGS_FOR_PICKY_PEOPLE
                    elif selected_menu_item == 2:  # Help
                        current_state = GameState.HELP_ME_OBI_WAN
                    elif selected_menu_item == 3:  # Credits
                        current_state = GameState.CREDITS_TO_THE_AWESOME
                    elif selected_menu_item == 4:  # Quit
                        running = False

            elif current_state == GameState.PLAYING_FOR_YOUR_LIFE:
                if event.key == pygame.K_UP and game.direction != (0, GRID_TEENY_WEENY_SIZE):
                    game.direction = (0, -GRID_TEENY_WEENY_SIZE)
                elif event.key == pygame.K_DOWN and game.direction != (0, -GRID_TEENY_WEENY_SIZE):
                    game.direction = (0, GRID_TEENY_WEENY_SIZE)
                elif event.key == pygame.K_LEFT and game.direction != (GRID_TEENY_WEENY_SIZE, 0):
                    game.direction = (-GRID_TEENY_WEENY_SIZE, 0)
                elif event.key == pygame.K_RIGHT and game.direction != (-GRID_TEENY_WEENY_SIZE, 0):
                    game.direction = (GRID_TEENY_WEENY_SIZE, 0)
                elif event.key == pygame.K_p:  # Pause
                    current_state = GameState.PAUSED_FOR_DRAMATIC_EFFECT
                elif event.key == pygame.K_ESCAPE:  # Return to main menu
                    current_state = GameState.MAIN_MENU_OF_DESTINY
                elif event.key == pygame.K_h:  # SECRET PARTY HAT MODE!!!!
                    snake_party_hats = not snake_party_hats

            elif current_state == GameState.GAME_OVER_DUDE_SO_SAD:
                if event.key == pygame.K_SPACE:  # Restart game
                    current_state = GameState.PLAYING_FOR_YOUR_LIFE
                    game.reset_game()
                elif event.key == pygame.K_ESCAPE:  # Return to main menu
                    current_state = GameState.MAIN_MENU_OF_DESTINY

            elif current_state == GameState.HELP_ME_OBI_WAN:
                if event.key == pygame.K_ESCAPE:  # Return to main menu
                    current_state = GameState.MAIN_MENU_OF_DESTINY

            elif current_state == GameState.SETTINGS_FOR_PICKY_PEOPLE:
                if event.key == pygame.K_ESCAPE:  # Return to main menu
                    # Apply settings before returning
                    current_options = [min(3, max(0, opt)) for opt in current_options]
                    apply_settings(*current_options)
                    current_state = GameState.MAIN_MENU_OF_DESTINY
                elif event.key == pygame.K_RIGHT:
                    # Change setting
                    if selected_menu_item < 4:  # For all except party mode
                        current_options[selected_menu_item] = min(3, current_options[selected_menu_item] + 1)
                    else:  # Party mode is just on/off
                        current_options[selected_menu_item] = 1 - current_options[selected_menu_item]
                elif event.key == pygame.K_LEFT:
                    # Change setting
                    if selected_menu_item < 4:  # For all except party mode
                        current_options[selected_menu_item] = max(0, current_options[selected_menu_item] - 1)
                    else:  # Party mode is just on/off
                        current_options[selected_menu_item] = 1 - current_options[selected_menu_item]
                elif event.key == pygame.K_UP:
                    selected_menu_item = max(0, selected_menu_item - 1)
                elif event.key == pygame.K_DOWN:
                    selected_menu_item = min(4, selected_menu_item + 1)
                elif event.key == pygame.K_RETURN:
                    # Apply settings and return to main menu
                    apply_settings(*current_options)
                    current_state = GameState.MAIN_MENU_OF_DESTINY

            elif current_state == GameState.CREDITS_TO_THE_AWESOME:
                if event.key == pygame.K_ESCAPE:  # Return to main menu
                    current_state = GameState.MAIN_MENU_OF_DESTINY

            elif current_state == GameState.PAUSED_FOR_DRAMATIC_EFFECT:
                if event.key == pygame.K_p:  # Resume game
                    current_state = GameState.PLAYING_FOR_YOUR_LIFE
                elif event.key == pygame.K_r:  # Restart game
                    current_state = GameState.PLAYING_FOR_YOUR_LIFE
                    game.reset_game()
                elif event.key == pygame.K_ESCAPE:  # Return to main menu
                    current_state = GameState.MAIN_MENU_OF_DESTINY

        # Check for mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if current_state == GameState.HELP_ME_OBI_WAN:
                # Check if back button clicked
                back_rect = pygame.Rect(SCREEN_CHUNKY_MONKEY_WIDTH // 2 - 150, 
                                      SCREEN_ABSOLUTELY_BONKERS_HEIGHT - 70, 300, 40)
                if back_rect.collidepoint(mouse_pos):
                    current_state = GameState.MAIN_MENU_OF_DESTINY

            elif current_state == GameState.SETTINGS_FOR_PICKY_PEOPLE:
                # Check if back button clicked
                back_rect = pygame.Rect(SCREEN_CHUNKY_MONKEY_WIDTH // 2 - 100, 
                                      SCREEN_ABSOLUTELY_BONKERS_HEIGHT - 70, 200, 40)
                if back_rect.collidepoint(mouse_pos):
                    apply_settings(*current_options)
                    current_state = GameState.MAIN_MENU_OF_DESTINY

                # Check if any settings clicked
                for i in range(5):  # 5 settings
                    for j in range(len(color_options[i])):
                        option_rect = pygame.Rect(250 + j * 180, 150 + i * 70 - 10, 170, 30)
                        if option_rect.collidepoint(mouse_pos):
                            current_options[i] = j

            elif current_state == GameState.CREDITS_TO_THE_AWESOME:
                # Check if back button clicked
                back_rect = pygame.Rect(SCREEN_CHUNKY_MONKEY_WIDTH // 2 - 100, 
                                      SCREEN_ABSOLUTELY_BONKERS_HEIGHT - 70, 200, 40)
                if back_rect.collidepoint(mouse_pos):
                    current_state = GameState.MAIN_MENU_OF_DESTINY

    # Update game state with ENTHUSIASM
    if current_state == GameState.PLAYING_FOR_YOUR_LIFE:
        # Set game speed based on difficulty
        if difficulty_level == "Easy Peasy":
            game_speed = 5
        elif difficulty_level == "TOTALLY AVERAGE":
            game_speed = 10
        elif difficulty_level == "Hard (Ouch!)":
            game_speed = 15
        elif difficulty_level == "NIGHTMARE MODE (RIP)":
            game_speed = 20

        # Apply powerup effects
        if game.powerup_effect == "SPEED_BOOST":
            game_speed += 5
        elif game.powerup_effect == "SLOW_MOTION":
            game_speed = max(2, game_speed - 5)

        # Update game state
        game.update()

        # Check for game over
        if game.game_over:
            current_state = GameState.GAME_OVER_DUDE_SO_SAD

    # Render appropriate screen with GUSTO
    if current_state == GameState.MAIN_MENU_OF_DESTINY:
        draw_main_menu()
    elif current_state == GameState.PLAYING_FOR_YOUR_LIFE:
        game.draw(screen)
    elif current_state == GameState.GAME_OVER_DUDE_SO_SAD:
        game.draw(screen)
        draw_game_over_screen()
    elif current_state == GameState.HELP_ME_OBI_WAN:
        draw_help_screen()
    elif current_state == GameState.SETTINGS_FOR_PICKY_PEOPLE:
        draw_settings_screen()
    elif current_state == GameState.CREDITS_TO_THE_AWESOME:
        draw_credits_screen()
    elif current_state == GameState.PAUSED_FOR_DRAMATIC_EFFECT:
        game.draw(screen)
        draw_pause_screen()

    # Update the display with FLOURISH
    pygame.display.flip()

    # Control game speed
    if current_state == GameState.PLAYING_FOR_YOUR_LIFE:
        clock.tick(game_speed)
    else:
        clock.tick(30)  # Menu screens run at reasonable FPS

# Clean up
pygame.quit()
sys.exit()
