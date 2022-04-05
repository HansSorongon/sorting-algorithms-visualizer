import pygame, sys
import math
import random

import additional_functions as af

class Sorter():

    def __init__(self, n):

        pygame.init()
        pygame.mixer.init()

        self.clock = pygame.time.Clock()

        self.width = 1200
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.gap_size = 1

        self.finished = False
        # self.color_speed = math.ceil(int((self.width / n) / 2))
        self.color_speed = 10
        self.n = n

        self.colors = []
        self.color_index = 0
        self.color_count = 0

        self.blip = pygame.mixer.Sound('blip.wav')
        self.blip.set_volume(0.1)

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
            properties = (i*space, self.height-array[i], block_width, array[i])
            pygame.draw.rect(self.screen, colors[i], properties)

    def color_array(self):
        if self.finished and self.color_count < self.n * self.color_speed:
            if self.color_count % self.color_speed == 0:
                self.colors[int(self.color_count / self.color_speed) ] = 'green'
                pygame.mixer.Sound.play(self.blip)
            self.color_count += 1

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

        # MAIN LOOP
        while True:

            self.screen.fill("black")

            self.display_array(self.gap_size, array, self.colors)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        sys.exit()
                    if event.key == pygame.K_1:
                        algorithms['bubble sort'] = True
                    if event.key == pygame.K_2:
                        array = self.insertion_sort(array)

            mx, my = pygame.mouse.get_pos()

            if algorithms['bubble sort']:
                self.colors[j] = 'white'
                i, j= self.bubble_sort(i, j, array)
                self.colors[j] = 'green'

            self.color_array()

            af.display_text(self.screen, f"FPS: {int(self.clock.get_fps())}", (10, 10), 12)


            # print(int(self.clock.get_fps()))
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
        return i, j
        
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
    sorter = Sorter(200)
    sorter.run()
