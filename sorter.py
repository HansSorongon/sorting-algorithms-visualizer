import pygame, sys
import math
import random

import additional_functions as af

class Button():

    def __init__(self, surface, text, location):

        self.surface = surface
        self.size = (50, 25)
        self.font = pygame.font.Font('pixel_font.ttf', 12)
        self.text = self.font.render(text, True, 'white')
        text_rect = self.text.get_rect()
        self.rect = pygame.Rect(location[0], location[1], text_rect[2],
        text_rect[3]) # uniform size

        self.location = location

    def display(self):
        self.surface.blit(self.text, self.location)
        return self.rect

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

        self.finished = False
        # self.color_speed = math.ceil(int((self.width / n) / 2))
        self.color_speed = 10
        self.n = n

        self.colors = []
        self.color_index = 0
        self.color_count = 0

        self.blip = pygame.mixer.Sound('blip.wav')
        self.blip.set_volume(0.1)

        self.bubble_button = Button(self.screen, "bubble sort",
        [self.width + 10, 10])

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

    def check_hover(self, mouse_pos, hovering):
        bubble_rect = self.bubble_button.display()
        if bubble_rect.collidepoint(mouse_pos):
            if not hovering:
                self.bubble_button.location[0] += 10
                hovering = True # You are now currently hovering.
        else:
            if hovering:
                self.bubble_button.location[0] -= 10
                hovering = False
        return hovering, bubble_rect

    def run(self):

        array = self.generate_array()

        for i in range(self.n):
            self.colors.append("white")

        i = 0
        j = 0

        color_count = 0

        # Algorithm Dictionary
        algorithms = {
            'bubble sort': False,
        }
        algo_keys = list(algorithms)

        hovering = False
        # MAIN LOOP ---------------------------------------------------
        while True:

            self.screen.fill("black")

            self.display_array(self.gap_size, array, self.colors)

            pygame.draw.rect(self.screen, 'white', (self.width, 0, 2,
            self.height))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        sys.exit()
                    if event.key == pygame.K_2:
                        array = self.insertion_sort(array)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if bubble_rect.collidepoint(mouse_pos):
                            algorithms['bubble sort'] = True

            mouse_pos = pygame.mouse.get_pos()

            if algorithms['bubble sort']:
                self.colors[j] = 'white'
                i, j= self.bubble_sort(i, j, array)
                self.colors[j] = 'green'

            # Aesthetics
            self.color_array()
            af.display_text(self.screen, f"FPS: {int(self.clock.get_fps())}",
            (10, 10), 12)

            # Sidebar Buttons
            hovering, bubble_rect = self.check_hover(mouse_pos, hovering)

            # Essentials
            self.clock.tick(0)
            pygame.display.update()

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
        return i, j # i, j are used to display each specific iteration

    def insertion_sort(self, array):
        arr = array
        for i in range(1, len(arr)):
            key = arr[i]

            j = i-1
            while j >= 0 and key < arr[j] :
                    arr[j + 1] = arr[j]
                    j -= 1
                    arr[j + 1] = key
        return arr

if __name__ == "__main__":
    sorter = Sorter(50)
    sorter.run()
