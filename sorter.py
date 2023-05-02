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
        self.color_speed = 5
        self.n = n

        self.array = self.generate_array()

        self.colors = []
        self.color_index = 0
        self.color_count = 0

        self.blip = pygame.mixer.Sound('blip.wav')
        self.blip.set_volume(0.1)

        self.bubble_button = Button(self.screen, "bubble sort",
        [self.width + 10, 10])
        self.insertion_button = Button(self.screen, "insertion sort",
                                       [self.width + 10, 35])
        self.selection_button = Button(self.screen, "selection sort",
                                       [self.width + 10, 60])
        self.merge_button = Button(self.screen, "merge sort", [self.width + 10,
                                                               85])
        self.bogosort_button = Button(self.screen, "bogosort", [self.width +
                                                                10, 110])
        self.quicksort_button = Button(self.screen, "quicksort", [self.width +
                                                                  10, 135])
        self.cocktail_sort_button = Button(self.screen, "cocktail sort",
                                           [self.width + 10, 160])


        self.three_hundred = Button(self.screen, "300 Elements", [self.width + 10,
                                                         self.height - 50])
        self.reset_button = Button(self.screen, "reset", [self.width + 10, self.height - 25])

        self.algorithms = {
            'bubble sort': False,
            'insertion sort': False,
            'selection sort': False,
            'merge sort': False,
            'bogosort': False,
            'quicksort': False,
            'cocktail sort': False
        }

        self.count = 0

        self.buttons = [
                        self.bubble_button,
                        self.insertion_button,
                        self.selection_button,
                        self.merge_button,
                        self.bogosort_button,
                        self.quicksort_button,
                        self.cocktail_sort_button,

                        self.three_hundred,
                        self.reset_button
                       ]

        self.hovering = False

    def generate_array(self):
        array = []
        # for i in range(self.n):
        #     array.append(random.randint(1, self.height - 100))

        # some constant the average of each bar
        constant = (self.height - 100) // self.n

        for i in range(self.n):
            array.append(i * constant)

        random.shuffle(array)

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

        self.colors = ["white" for i in range(self.n)]

        # variable declarations for color indices
        i = 0
        j = 0
        min_idx = 0

        key = self.array[i]
        # it = self.new_bubble_sort(self.array)
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
                    if event.key == pygame.K_s:
                        self.algorithms['cocktail sort'] = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for button in self.buttons:
                            if button.rect.collidepoint(mouse_pos):

                                self.algorithms[button.raw_text] = True

                                if button.raw_text == "bubble sort":
                                    it = self.bubble_sort(self.array)
                                if button.raw_text == "insertion sort":
                                    it = self.insertion_sort(self.array)
                                if button.raw_text == "selection sort":
                                    it = self.selection_sort(self.array)
                                if button.raw_text == "merge sort":
                                    it = self.merge_sort(self.array)
                                if button.raw_text == "bogosort":
                                    it = self.bogosort(self.array)
                                if button.raw_text == "quicksort":
                                    it = self.quicksort(self.array, 0, len(self.array) - 1)
                                if button.raw_text == "cocktail sort":
                                    it = self.cocktail_sort(self.array)

                                if button.raw_text == "300 Elements":
                                    self.n = 300
                                    self.reset()
                                if button.raw_text == "reset":
                                    self.reset()

            mouse_pos = pygame.mouse.get_pos()

            # Algorithm Iterations
            if self.algorithms['bubble sort']:
                self.colors[j+1] = 'white'
                self.colors[i] = 'white'
                try:
                    i, j = next(it)
                    pygame.mixer.Sound.play(self.blip)
                    self.colors[j+1] = 'green'
                    self.colors[i] = 'red'
                except StopIteration:
                    self.finished = True
                    self.algorithms['bubble sort'] = False
            if self.algorithms['insertion sort']:
                self.colors[j] = 'white'
                self.colors[i] = 'white'
                try:
                    i, j = next(it)
                    self.colors[i] = 'red'
                    self.colors[j] = 'green'
                except StopIteration:
                    self.finished = True
                    self.algorithms['insertion sort'] = False
            if self.algorithms['selection sort']:
                self.colors[i] = 'white'
                self.colors[min_idx] = 'white'
                try:
                    self.clock.tick(20)
                    i, min_idx = next(it)
                    self.colors[i] = 'red'
                    self.colors[min_idx] = 'green'
                except StopIteration:
                    self.clock.tick(60)
                    self.finished = True
                    self.algorithms['selection sort'] = False
            if self.algorithms['merge sort']:
                self.colors[i] = 'white'
                self.colors[j - 1] = 'white'
                try:
                    self.clock.tick(80)
                    i, j = next(it)
                    self.colors[i] = 'red'
                    self.colors[j - 1] = 'green'
                except StopIteration:
                    self.clock.tick(60)
                    self.finished = True
                    self.algorithms['merge sort'] = False
            if self.algorithms['bogosort']:
                try:
                    self.clock.tick(80)
                    a = next(it)
                except StopIteration:
                    self.clock.tick(60)
                    self.finished = True
                    self.algorithms['bogosort'] = False
            if self.algorithms['quicksort']:
                self.colors[i] = 'white'
                try:
                    self.clock.tick(40)
                    i = next(it)
                    self.colors[i] = 'red'
                except StopIteration:
                    self.clock.tick(60)
                    self.finished = True
                    self.algorithms['quicksort'] = False
            if self.algorithms['cocktail sort']:
                self.colors[i + 1] = 'white'
                try:
                    self.clock.tick(500)
                    i = next(it)
                    self.colors[i + 1] = 'red'
                except StopIteration:
                    self.clock.tick(60)
                    self.finished = True
                    self.algorithms['cocktail sort'] = False


            # Aesthetics
            self.color_array()
            # af.display_text(self.screen, f"FPS: {int(self.clock.get_fps())}",
            # (10, 10), 12)

            bubble_rect = self.bubble_button.display()
            insertion_rect = self.insertion_button.display()
            selection_rect = self.selection_button.display()
            merge_rect = self.merge_button.display()
            bogosort_rect = self.bogosort_button.display()
            quicksort_rect = self.quicksort_button.display()
            cocktail_rect = self.cocktail_sort_button.display()

            three_hundred_rect = self.three_hundred.display()
            reset_rect = self.reset_button.display()

            # Sidebar Buttons
            insertion_rect = self.insertion_button.display()
            self.check_hover(mouse_pos, self.buttons)

            # Essentials
            self.clock.tick(0)
            pygame.display.update()

    # MAIN SORTING ALGORITHMS
    def bubble_sort(self, array):
        n = self.n
        for i in range(n-1):
            for j in range(n-i-1):
                if array[j] > array[j + 1]:
                    array[j], array[j + 1] = array[j + 1], array[j]
                    yield i, j

    def insertion_sort(self, array):
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
                        yield i, j

    def selection_sort(self, array):

        for i in range(self.n):
            min_idx = i
            for j in range(i+1, len(array)):
                if array[min_idx] > array[j]:
                    min_idx = j
                    pygame.mixer.Sound.play(self.blip)
            array[i], array[min_idx] = array[min_idx], array[i]
            yield i, min_idx

    def merge_sort(self, array):

        # it's recursive so we define inside
        def merge_recursion(start, end):
            if end - start > 1:
                middle = (start + end) // 2

                yield from merge_recursion(start, middle)
                yield from merge_recursion(middle, end)
                left = array[start:middle]
                right = array[middle:end]

                a = 0
                b = 0
                c = start

                while a < len(left) and b < len(right):
                    if left[a] < right[b]:
                        array[c] = left[a]
                        pygame.mixer.Sound.play(self.blip)
                        a += 1
                    else:
                        array[c] = right[b]
                        b += 1
                    c += 1
                while a < len(left):
                    array[c] = left[a]
                    pygame.mixer.Sound.play(self.blip)
                    a += 1
                    c += 1
                while b < len(right):
                    array[c] = right[b]
                    pygame.mixer.Sound.play(self.blip)
                    b += 1
                    c += 1
            yield start, end
        yield from merge_recursion(0, len(array))

    def bogosort(self, array):

        def is_sorted(data):
            return all(a <= b for a, b in zip(data, data[1:]))

        while not is_sorted(array):
            random.shuffle(array)
            pygame.mixer.Sound.play(self.blip)
            yield array

    def quicksort(self, array, start, end):

        def quicksort_recursion(arr, start, end):

            if (end <= start):
                return

            pivot = arr[end]
            i = start - 1

            for j in range(start, end):
                if (arr[j] < pivot):
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]

            i += 1
            arr[i], arr[end] = arr[end], arr[i]

            yield i # pivot
            pygame.mixer.Sound.play(self.blip)

            yield from quicksort_recursion(arr, start, i - 1)
            yield from quicksort_recursion(arr, i + 1, end)
        yield from quicksort_recursion(array, 0, len(array) - 1)

    def cocktail_sort(self, array):
        n = len(array)
        swapped = True
        start = 0
        end = n - 1

        while (swapped == True):
            swapped = False

            for i in range(start, end):
                if (array[i] > array[i + 1]):
                    array[i], array[i + 1] = array[i + 1], array[i]
                    swapped = True
                    pygame.mixer.Sound.play(self.blip)
                    yield i

            if (swapped == False):
                break
            swapped = False

            end = end - 1

            for i in range(end - 1, start - 1, -1):
                if (array[i] > array[i + 1]):
                    array[i], array[i + 1] = array[i + 1], array[i]
                    swapped = True
                    pygame.mixer.Sound.play(self.blip)
                    yield i
            start = start + 1

    def reset(self):
        sorter = Sorter(self.n)
        sorter.run()

if __name__ == "__main__":
    sorter = Sorter(200)
    sorter.run()
