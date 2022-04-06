import pygame, sys
import math
import random

import additional_functions as af

class Button():

    def __init__(self, surface, text, location):

        self.surface = surface
        self.font = pygame.font.Font('pixel_font.ttf', 12)
        self.raw_text = text
        self.text = self.font.render(text, True, 'white')
        self.text_rect = self.text.get_rect()
        self.rect = pygame.Rect(location[0], location[1], self.text_rect[2],
        self.text_rect[3]) # uniform size
        self.hovering = False

        self.location = location

    def display(self):
        self.surface.blit(self.text, self.location)

class Sorter():

    def __init__(self, n):

        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Sorting Algorithms")

        self.clock = pygame.time.Clock()

        # Screen Properties
        self.screen_width = 1400
        self.width = 1200
        self.height = 800
        self.screen = pygame.display.set_mode((self.screen_width,
        self.height))
        self.gap_size = 2
        icon = pygame.image.load('icon.png')
        pygame.display.set_icon(icon)

        self.finished = False
        # self.color_speed = math.ceil(int((self.width / n) / 2))
        self.color_speed = 10
        self.n = n

        self.array = self.generate_array()

        self.colors = []
        self.color_index = 0
        self.color_count = 0

        self.blip = pygame.mixer.Sound('blip.wav')
        self.blip.set_volume(0.1)

        self.bubble_button = Button(self.screen, "bubble sort",
        [self.width + 10, 10])
        self.insertion_button = Button(self.screen, "insertion sort", [self.width + 10, 30])
        self.reset_button = Button(self.screen, "reset", [self.width + 10, self.height - 25])

        self.algorithms = {
            'bubble sort': False,
            'insertion sort': False,
        }

        self.count = 0

        self.buttons = [self.bubble_button,
                        self.insertion_button,
                        self.reset_button]

        self.hovering = False

    def generate_array(self):
        array = []
        for i in range(self.n):
            array.append(random.randint(1, self.height - 100))
        return array

    def display_array(self, gap_size, array, colors):

        space = int(self.width / self.n)
        block_width = int((self.width-(self.n*gap_size))/self.n)

        # for i in array, print with gaps
        for i in range(self.n):
            properties = (i*space, self.height-array[i], block_width,
            array[i])
            pygame.draw.rect(self.screen, colors[i], properties)

    def color_array(self):
        if self.finished and self.color_count < self.n * self.color_speed:
            if self.color_count % self.color_speed == 0:
                self.colors[int(self.color_count / self.color_speed) ] = 'green'
                pygame.mixer.Sound.play(self.blip)
            self.color_count += 1

    def check_hover(self, mouse_pos, buttons):
        for button in buttons:
            if button.rect.collidepoint(mouse_pos):
                if not button.hovering:
                    button.location[0] += 10
                    button.hovering = True
            else:
                if button.hovering:
                    button.location[0] -= 10
                    button.hovering = False


    def run(self):

        # Non-loop variables
        # array = self.generate_array()

        for i in range(self.n):
            self.colors.append("white")

        i = 0
        j = 0

        key = self.array[i]

        color_count = 0


        # MAIN LOOP ---------------------------------------------------
        while True:

            self.screen.fill("black")

            self.display_array(self.gap_size, self.array, self.colors)

            pygame.draw.rect(self.screen, 'white', (self.width, 0, 2,
            self.height))

            # EVENT HANDLER
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        sys.exit()
                    if event.key == pygame.K_r:
                        self.reset()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.buttons[0].rect.collidepoint(mouse_pos) and not self.finished:
                            self.algorithms['bubble sort'] = True
                        elif self.finished:
                            self.reset()
                            self.algorithms['bubble sort'] = True # Automate running this with an optional class argument.
                        if self.buttons[1].rect.collidepoint(mouse_pos) and not self.finished:
                            self.algorithms['insertion sort'] = True
                        elif self.finished:
                            self.reset()
                        if self.buttons[2].rect.collidepoint(mouse_pos):
                            self.reset()


            mouse_pos = pygame.mouse.get_pos()

            if self.algorithms['bubble sort']:
                self.colors[j] = 'white'
                i, j= self.bubble_sort(i, j, self.array)
                self.colors[j] = 'green'
            if self.algorithms['insertion sort']:
                self.colors[j+1] = 'white'
                try:
                    i, j = self.insertion_sort(i, j, self.array, key)
                    self.colors[j+1] = 'green'
                except:
                    self.finished = True
                    self.algorithms['insertion sort'] = False

            # Aesthetics
            self.color_array()
            af.display_text(self.screen, f"FPS: {int(self.clock.get_fps())}",
            (10, 10), 12)

            bubble_rect = self.bubble_button.display()
            insertion_rect = self.insertion_button.display()
            reset_rect = self.reset_button.display()

            # Sidebar Buttons
            insertion_rect = self.insertion_button.display()
            self.check_hover(mouse_pos, self.buttons)

            # Essentials
            self.clock.tick(0) # Control Frame Rate
            pygame.display.update()

    # MAIN SORTING ALGORITHMS
    def bubble_sort(self, i, j, array):
        if i < self.n:
            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]
                pygame.mixer.Sound.play(self.blip)
            if i < self.n:
                j += 1
                if j >= self.n-i-1:
                    j = 0
                    i += 1
        else:
            self.finished = True
        return i, j

    def insertion_sort(self, i, j, array, key):
        if self.algorithms['insertion sort']:
            arr = array
            for i in range(1, len(arr)):
                key = arr[i]
                j = i-1
                while j >= 0 and key < arr[j]:
                        arr[j + 1] = arr[j]
                        pygame.mixer.Sound.play(self.blip)
                        j -= 1
                        arr[j + 1] = key
                        return i, j

    def reset(self):
        sorter = Sorter(self.n)
        sorter.run()

if __name__ == "__main__":
    sorter = Sorter(50)
    sorter.run()
