import pygame
import numpy as np
import time
import random


def collision_with_pipe(pipes_positions, bird):
    pipe = pipes_positions[0]
    if (pipe[2] - bird[0]) > 10 or (pipe[2] - bird[0]) < 0:
        return False
    if pipe[0]-10 < bird[1] or pipe[1] > bird[1]:
        return True



def collision_with_boundaries(bird_position):
    if bird_position[1] >= 600 or bird_position[1] < 0:
        return True
    else:
        return False


def generate_pipes(pipes_positions):
    pipe_height = random.randint(100, 500)
    pipes_positions.append((pipe_height + 50, pipe_height - 50, display_width))



def display_bird(bird_position):
    pygame.draw.rect(display, red, pygame.Rect(bird_position[0], bird_position[1], 10, 10))


def display_pipes(pipes_positions):
    for pipe in pipes_positions:
        if pipe[2] < 0:
            pipes_positions.pop(0)
        pygame.draw.rect(display, black, pygame.Rect(pipe[2], 0, 10, pipe[1]))
        pygame.draw.rect(display, black, pygame.Rect(pipe[2], pipe[0], 10, 600 - pipe[0]))

def display_score(score):
    largeText = pygame.font.Font('freesansbold.ttf',15)
    TextSurf = largeText.render(f'Score: {score}', True, black)
    display.blit(TextSurf, (10, 10))


def play_game(gravitation, bird_position, pipes_positions, score):
    timer = 0
    crashed = False
    serialized_data = None;

    while crashed is not True:
        if timer == 0:
            generate_pipes(pipes_positions)
            timer = 120

        for pipe in pipes_positions:
            if pipe[2] < bird_position[0]:
                continue
            data = [attempt, bird_position[0], pipe[2], pipe[1], pipe[0]]
            serialized_data = ",".join(map(str, data)).encode()
        #podejscie, wysokosc ptaka, pozycja dziury, wysokosc gorna dziury, wysokosc dolna dziury

        s.sendall(serialized_data)
        # Odbiór odpowiedzi od plikNeuron
        odpowiedz = s.recv(1024).decode()
        # print("Odpowiedź od plikNeuron:", odpowiedz)

        # Symulacja wykonania skoku lub nieskoku na podstawie odpowiedzi
        if odpowiedz == 'True':
            # print("Wykonaj skok!")
            gravitation = -8

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.KEYUP:
                gravitation = -8
                # TU NAPISAC CO SIE DZIEJE GDY PODSKOCZE



        for i in range(len(pipes_positions)):
            tuple_value = pipes_positions[i]
            new_tuple = (tuple_value[0], tuple_value[1], tuple_value[2] - 2)
            pipes_positions[i] = new_tuple

        crashed = collision_with_boundaries(bird_position) or collision_with_pipe(pipes_positions, bird_position)

        display.fill(window_color)
        display_bird(bird_position)
        display_pipes(pipes_positions)
        display_score(score)

        pygame.display.set_caption("FlappyBird" + "  " + "SCORE: " + str(score))
        pygame.display.update()

        bird_position[1] += gravitation
        gravitation += 0.5
        timer -= 1
        score += 1
        clock.tick(240)

    return score


import socket

if __name__ == "__main__":
    HOST = '127.0.0.1'  # Adres localhost
    PORT = 65432  # Port do komunikacji

    attempt = 1
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))  # Nawiązanie połączenia
        print("Connected")
        # Symulacja gry



        while True:
            ###### initialize required parameters ########
            display_width = 600
            display_height = 600
            green = (0, 255, 0)
            red = (255, 0, 0)
            black = (0, 0, 0)
            window_color = (200, 200, 200)
            clock = pygame.time.Clock()


            gravitation = 0
            flappy_bird_position = [150, 300]
            pipes_positions = []
            score = 0

            random.seed(69)


            pygame.init()  # initialize pygame modules

            #### display game window #####

            display = pygame.display.set_mode((display_width, display_height))
            display.fill(window_color)
            pygame.display.update()

            final_score = play_game(gravitation, flappy_bird_position, pipes_positions, score)
            print(f"Attempt: {attempt}, FINAL SCORE: {final_score}")
            attempt+=1
            pygame.quit()


