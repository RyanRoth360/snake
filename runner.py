import pygame
import logic
import random

HEIGHT = 600
WIDTH = 600
BG = pygame.Color(103, 186, 101)
BLACK = pygame.Color(0, 0, 0)
RED = pygame.Color(209, 60, 6)
GREY = pygame.Color(100, 100, 100)
DARK_RED = pygame.Color(148, 44, 3)
BLUE = pygame.Color(38, 157, 237)
DARK_BLUE = pygame.Color(6, 76, 122)
YELLOW = pygame.Color(230, 202, 78)
LAV = pygame.Color(159, 88, 191)
GOLD = pygame.Color(161, 125, 8)
GREEN = pygame.Color(2, 94, 53)
SCARLET = pygame.Color(173, 31, 107)
DARK_SCARLET = pygame.Color(92, 7, 53)
FRAME_RATE = 60

# BUGS
# - visula glitch
# - snake gets cut off sometimes
#
#


class Game:

    def __init__(self):
        self.master = True
        self.running = True
        self.sound = True
        self.logic = logic.Logic()
        self.bounds_power_up = False
        self.apple_power_up = False

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        apple = pygame.mixer.Sound('./assests/bite1.wav')
        thud = pygame.mixer.Sound('./assests/thud.wav')
        star = pygame.mixer.Sound('./assests/star.wav')
        power_down = pygame.mixer.Sound('./assests/power_down.wav')
        gold = pygame.mixer.Sound('./assests/gold.wav')
        poisen = pygame.mixer.Sound('./assests/poisen.wav')

        while self.master:
            pygame.font.init()
            pygame.mixer.init()
            clock.tick(FRAME_RATE)
            self._create_display(HEIGHT, WIDTH)
            try:
                # RESETS VARIABLES
                self.logic.board = self.logic.clear_board()
                self.bounds_power_up = False
                self.logic.generate_starting_pos()
                self.logic.generate_piece('A')
                power_spawned = False
                gold_spawned = False
                poisen_spawned = False
                end_sound = False
                directions = []
                count = 1
                score = 0
                condition = ''

                while self.running:
                    # MOVES SNAKE
                    directions.append(self._handle_inputs())
                    self._clean_list(directions)
                    if len(directions) > 0:
                        count += 1
                        if directions[-1] == 'restart':  # RESTARTS GAME
                            break
                        elif directions[-1] == 'sound':  # TURNS SOUND ON/OFF
                            self.sound = not self.sound
                            del directions[-1]
                        if count % 30 == 0:  # CONTROLS SNAKE SPEED
                            condition = self.logic.move(
                                directions[-1], self.bounds_power_up)  # EXECUTES MOVE
                            if condition == 'Delete':  # ACCOUNTS FOR FAST TAPS
                                del directions[-1]
                            elif condition == 'Crossed' or condition == 'OOB':  # ENDS GAME
                                star.stop()
                                if self.sound:
                                    thud.play()
                                pygame.time.wait(500)
                                self.running = False
                                self.bounds_power_up = False

                    # CHECKS APPLE AND POWER UPS
                    if not self.logic.find_piece('A'):
                        self.logic.add_tail(False)  # GROWS SNAKE
                        self.logic.generate_piece('A')  # CREATES APPLE
                        if self.sound:
                            apple.play()
                        score += 1

                    if count % 450 == 0 and score >= 10 and not power_spawned:  # CONTROLS FREQUENCY OF WHEN POWER CAN SPAWN
                        power_spawned = self._randomize_bounds_powerup()
                    elif count % 250 == 0 and not gold_spawned:
                        gold_spawned = self._randomize_apple_powerup()
                        if gold_spawned:
                            gold_end_time = pygame.time.get_ticks()+3500
                            if self.sound:
                                gold.play()
                    elif count % 251 == 0 and not poisen_spawned:
                        poisen_spawned = self._randomize_poisen_powerup()
                        if poisen_spawned:
                            poisen_end_time = pygame.time.get_ticks()+10000

                    if poisen_spawned:
                        if pygame.time.get_ticks() > poisen_end_time:
                            self.logic.erase_piece('P')
                            poisen_spawned = False
                        elif not self.logic.find_piece('P'):
                            self.bounds_power_up = False
                            star.stop()
                            if self.sound:
                                poisen.play()
                            self.running = False

                    if gold_spawned:
                        if pygame.time.get_ticks() > gold_end_time:
                            self.logic.erase_piece('G')
                            gold_spawned = False
                        # POWER HAS BEEN EATEN IN TIME
                        elif not self.logic.find_piece('G'):
                            if self.sound:
                                apple.play()
                            self.logic.add_tail(True)
                            score += 3
                            gold_spawned = False

                    if power_spawned:  # IF A BOUNDS POWER WAS SPAWNED
                        # AND THE POWER IS GONE
                        if not self.logic.find_piece('B'):
                            self.bounds_power_up = True  # ACTIVIATES POWER UP
                            end_time = pygame.time.get_ticks()+10000
                            power_spawned = False
                            power_sound = True
                            end_sound = True

                    # HANDLES POWERUPS
                    if self.bounds_power_up:
                        if power_sound:
                            if self.sound:
                                star.play()
                            power_sound = False
                        if self.bounds_power_up and end_sound and end_time-1500 < pygame.time.get_ticks() < end_time-1480:  # 2 SECONDS LEFT
                            if self.sound:
                                power_down.play()
                            end_sound = False
                        if pygame.time.get_ticks() > end_time:  # DEACTIVATES POWER UP
                            star.stop()
                            self.bounds_power_up = False

                    if not self.sound:  # CONTROLS STAR SOUND
                        star.set_volume(0)
                    else:
                        star.set_volume(3.0)

                    self._redraw(score)

                while True:  # COMES HERE IF GAME ENDS

                    self._write_message()  # Don't know why this isn't working
                    action = self._handle_inputs()
                    if action == 'restart' or action == 'quit':
                        break
                    self._redraw(score)

            finally:

                pygame.quit()

    def _randomize_poisen_powerup(self):
        num = random.randrange(1, 11)  # Adjust range to adjust probablility
        if num == 1:
            self.logic.generate_piece('P')
            return True
        return False

    def _randomize_apple_powerup(self):
        num = random.randrange(1, 11)  # Adjust range to adjust probablility
        if num == 1:
            self.logic.generate_piece('G')
            return True
        return False

    def _randomize_bounds_powerup(self,):
        num = random.randrange(1, 11)  # Adjust range to adjust probablility
        if not self.logic.find_piece('B') and num == 1 and not self.bounds_power_up:
            self.logic.generate_piece('B')
            return True
        return False

    def _sound_text(self):
        surface = pygame.display.get_surface()
        image_on = pygame.image.load('./assests/note_on.png')
        image_on = pygame.transform.scale(
            image_on, (surface.get_width()*0.15, surface.get_height()*0.1450))
        image_off = pygame.image.load('./assests/note_off.png')
        image_off = pygame.transform.scale(
            image_off, (surface.get_width()*0.15, surface.get_height()*0.1450))
        imageX = 0.87*surface.get_width()
        imageY = -20

        if self.sound:
            surface.blit(image_on, (imageX, imageY))
        else:
            surface.blit(image_off, (imageX, imageY))

    def _write_score(self, score):
        surface = pygame.display.get_surface()
        font = pygame.font.Font('freesansbold.ttf', 40)
        textX = 0.025*surface.get_width()
        textY = 0.015*surface.get_height()
        score_text = font.render(str(score), True, BLACK)
        surface.blit(score_text, (textX, textY))

    def _write_message(self):
        surface = pygame.display.get_surface()
        font = pygame.font.SysFont('Comic Sans', 32)
        textX = 0.25*surface.get_width()
        textY = 0.03*surface.get_height()
        score_text = font.render(
            'Press R to restart or Q to quit', True, BLACK)
        surface.blit(score_text, (textX, textY))

    def _clean_list(self, directions: list):
        for item in directions:
            if item == '0':
                directions.remove(item)

        if len(directions) == 1:
            if directions[0] == 'left':
                del directions[0]

        if len(directions) >= 2:
            if directions[-1] == 'right' and directions[-2] == 'left':
                del directions[-1]
            elif directions[-1] == 'left' and directions[-2] == 'right':
                del directions[-1]
            elif directions[-1] == 'up' and directions[-2] == 'down':
                del directions[-1]
            elif directions[-1] == 'down' and directions[-2] == 'up':
                del directions[-1]

    def _create_display(self, height: int, width: int):
        pygame.display.set_mode((height, width), pygame.RESIZABLE)

    def _redraw(self, score):
        surface = pygame.display.get_surface()
        surface.fill(BG)
        self._draw_board()
        self._vert_lines()
        self._horiz_lines()
        self._write_score(score)
        self._sound_text()
        pygame.display.flip()

    def _handle_inputs(self):
        last_key = '0'
        up = pygame.mixer.Sound('./assests/up.wav')
        down = pygame.mixer.Sound('./assests/down.wav')
        right = pygame.mixer.Sound('./assests/right.wav')
        left = pygame.mixer.Sound('./assests/left.wav')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.master = False
                return 'quit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
                    self.master = False
                    return 'quit'
                if event.key == pygame.K_r and self.running == False:  # restart after
                    self.running = True
                if event.key == pygame.K_r and self.running == True:  # restart midgame
                    last_key = 'restart'
                if event.key == pygame.K_s:
                    last_key = 'sound'
                if event.key == pygame.K_LEFT:
                    last_key = 'left'
                    if self.sound:
                        left.play()
                if event.key == pygame.K_RIGHT:
                    last_key = 'right'
                    if self.sound:
                        right.play()
                if event.key == pygame.K_UP:
                    last_key = 'up'
                    if self.sound:
                        up.play()
                if event.key == pygame.K_DOWN:
                    last_key = 'down'
                    if self.sound:
                        down.play()
        return last_key

    def _draw_board(self):
        surface = pygame.display.get_surface()
        board = self.logic.get_board()
        for r in range(15):
            for c in range(15):
                if board[r][c] != ' ':

                    top_left_x, top_left_y = self._get_location(r, c)
                    rec_width = surface.get_width()/15
                    rec_height = (surface.get_height() -
                                  surface.get_height()*0.08)/15+1
                    rect = pygame.Rect((top_left_x, top_left_y),
                                       (rec_width, rec_height))

                    if board[r][c] == 'A':
                        pygame.draw.ellipse(surface, RED, rect)
                        pygame.draw.ellipse(surface, DARK_RED, rect, 4)
                    elif board[r][c] == 'B':
                        pygame.draw.ellipse(surface, BLUE, rect)
                        pygame.draw.ellipse(surface, DARK_BLUE, rect, 4)
                    elif board[r][c] == 'G':
                        pygame.draw.ellipse(surface, YELLOW, rect)
                        pygame.draw.ellipse(surface, GOLD, rect, 4)
                    elif board[r][c] == 'P':
                        pygame.draw.ellipse(surface, SCARLET, rect)
                        pygame.draw.ellipse(surface, DARK_SCARLET, rect, 4)

                    else:
                        if board[r][c] == 'S':
                            pygame.draw.rect(surface, BLACK, rect)
                        elif self.bounds_power_up:
                            color = pygame.Color(random.randrange(50, 255), random.randrange(
                                50, 255), random.randrange(50, 255))
                            pygame.draw.rect(surface, color, rect)
                        else:
                            pygame.draw.rect(surface, LAV, rect)
                        pygame.draw.rect(surface, BLACK, rect, 4)

    def _get_location(self, r, c):
        shift = 0
        if c < 5:
            shift = 0.005
        elif c == 11:
            shift = 0.0053
        else:
            shift = 0.00515
        surface = pygame.display.get_surface()
        x = r*surface.get_width()/15
        y = c*surface.get_height()/15+(0.08-shift*c)*surface.get_height()
        return x, y

    def _vert_lines(self):
        surface = pygame.display.get_surface()

        pix_x = 0
        pix_y = 0.08*surface.get_height()
        end_pix_y = surface.get_height()

        shift = 0
        for line in range(15):
            shift += surface.get_width()/15
            pygame.draw.line(surface, BLACK,
                             (pix_x+shift, pix_y), (pix_x+shift, end_pix_y))

    def _horiz_lines(self):
        surface = pygame.display.get_surface()

        pix_x = 0
        pix_y = 0.08*surface.get_height()
        end_pix_x = surface.get_width()

        shift = 0
        for line in range(15):

            pygame.draw.line(surface, BLACK,
                             (pix_x, pix_y+shift), (end_pix_x, pix_y+shift))
            shift += (surface.get_height()-pix_y)/15


if __name__ == '__main__':
    Game().run()
