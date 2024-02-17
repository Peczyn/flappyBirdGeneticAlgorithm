# Used Python 3.9 interpreter and libraries like
# OS, Pygame, Random, Tensorflow, Keras and numpy
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"  # only to hide prompts when running
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

import pygame
import random
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np


class Bird:
    def __init__(self, brain, height, gravitation, color):
        self.brain = brain
        self.height = height
        self.gravitation = gravitation
        self.score = 0
        self.color = color

    def updateGravitation(self):
        self.gravitation += 0.3

    def updateHeight(self):
        self.height += self.gravitation

    def updateScore(self):
        self.score += 1

    def jump(self):
        self.gravitation = -7

    def think(self, pipe):
        input_data = [self.height / 600, self.gravitation / 100, pipe.width / 600, pipe.higherOne / 600,
                      pipe.lowerOne / 600]
        input_array = np.array([input_data])
        # predictions = self.brain.predict(input_array, verbose=0)
        # You can use keras predictions, but it's much slower than then one I made

        predictions = predict(input_array, self.brain.get_weights())
        if predictions > 0.5:
            self.jump()


class Pipe:
    def __init__(self, lowerOne, higherOne, width):
        self.lowerOne = lowerOne
        self.higherOne = higherOne
        self.width = width

    def update(self):
        self.width -= 2



def createModel():
    model = Sequential()
    model.add(Dense(10, input_shape=(5,), activation='relu', ))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


def createChildModel(parent_model, deviation_factor=0.1):
    child_model = Sequential()
    for layer in parent_model.layers:
        if isinstance(layer, Dense):
            input_shape = layer.input_shape[1:]
            units = layer.units
            activation = layer.activation
            # Weights are randomly selected with deviation of the parent model
            weights = [weight + np.random.normal(scale=deviation_factor) for weight in layer.get_weights()]
            child_model.add(Dense(units, input_shape=input_shape, activation=activation, weights=weights))
    child_model.compile(loss=parent_model.loss, optimizer=parent_model.optimizer, metrics=parent_model.metrics)
    return child_model


def birdsThinking(birdsThinkers, pipe):
    for bird in birdsThinkers:
        bird.think(pipe)

def predict(X, weights):
    # Początkowe przekształcenie danych wejściowych
    X = X.reshape((X.shape[0], -1))

    # Pierwsza warstwa Dense z 8 węzłami i funkcją aktywacji ReLU
    W1 = weights[0]
    b1 = weights[1]
    X = np.dot(X, W1) + b1
    X[X < 0] = 0  # ReLU

    # Warstwa wyjściowa Dense z jednym węzłem i funkcją aktywacji sigmoidalną
    W2 = weights[2]
    b2 = weights[3]
    X = np.dot(X, W2) + b2
    output = 1 / (1 + np.exp(-X))  # Sigmoid

    return output

def birdsUpdate(birds):
    for bird in birds:
        bird.updateGravitation()
        bird.updateHeight()
        bird.updateScore()


def pipesUpdate(pipes):
    if pipes[0].width < 100:
        pipes.pop(0)
    for pipe in pipes:
        pipe.update()


def collision_with_pipe(pipe, birds, lastGenerationBirds):
    if 150 < pipe.width < 160:
        for bird in birds:
            if bird.height > pipe.lowerOne or bird.height < pipe.higherOne:
                lastGenerationBirds.append((birds[birds.index(bird)], bird.score))
                birds.pop(birds.index(bird))


def collision_with_boundaries(birds, lastGenerationBirds):
    for bird in birds:
        if bird.height > 600 or bird.height < 0:
            lastGenerationBirds.append((birds[birds.index(bird)], bird.score))
            birds.pop(birds.index(bird))


def generate_pipes(pipes):
    pipe_height = random.randint(150, 400)
    pipes.append(Pipe(lowerOne=pipe_height + 100, higherOne=pipe_height - 100, width=600))


def display_birds(birds):
    for bird in birds:
        pygame.draw.rect(display, bird.color, pygame.Rect(150, bird.height, 10, 10))


def display_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(display, white, pygame.Rect(pipe.width, 0, 15, pipe.higherOne))
        pygame.draw.rect(display, white, pygame.Rect(pipe.width, pipe.lowerOne, 15, 600 - pipe.lowerOne))


def display_score(score1, gen):
    largeText = pygame.font.Font('freesansbold.ttf', 15)
    textSurf = largeText.render(f'Score: {score1}', True, white)
    display.blit(textSurf, (10, 10))

    largeText = pygame.font.Font('freesansbold.ttf', 15)
    textSurf = largeText.render(f'Highest Score: {highestScore}', True, white)
    display.blit(textSurf, (10, 30))

    largeText = pygame.font.Font('freesansbold.ttf', 15)
    textSurf = largeText.render(f'Generation: {gen}', True, white)
    display.blit(textSurf, (10, 50))


def play_game(birds, pipes, inGameScore, lastGenerationBirdsArray, generation):
    timer = 0

    while birds.__sizeof__() != 0:
        if timer == 0:
            generate_pipes(pipes)
            timer = 200

        if timer % 3 == 0:
            birdsThinking(birds, pipes[0])

        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                for bird in birds:
                    bird.gravitation = -7

        # collision_with_pipe(Pipes[0], Birds)
        collision_with_boundaries(birds, lastGenerationBirdsArray)
        collision_with_pipe(pipes[0], birds, lastGenerationBirdsArray)

        # display birds, pipes, score
        display.fill((0, 0, 0))
        display_birds(birds)
        display_pipes(pipes)
        display_score(inGameScore, generation)

        # update everything
        pipesUpdate(pipes)
        birdsUpdate(birds)
        timer -= 1
        inGameScore += 1
        clock.tick(30)

        # display display
        pygame.display.set_caption("FlappyBird" + "  " + "SCORE: " + str(inGameScore))
        pygame.display.update()

        if not birds:
            break

    return inGameScore







def generateBirds(numberOfBirds, lastGen, maxscore, maxTuple):
    if not lastGen:
        for i in range(numberOfBirds):
            Birds.append(Bird(brain=createModel(),
                              height=200 + i,
                              gravitation=0,
                              color=(random.randint(0,255),
                                     random.randint(0,255),
                                     random.randint(0,255))
                              )
                         )
    else:
        for tup in lastGen:
            if maxscore < tup[1]:
                maxTuple = tup
                maxscore = tup[1]
        maxBrain = maxTuple[0].brain
        lastGen.clear()

        deviation = 0
        if maxscore < 1000:
            deviation = 0.25
        elif maxscore < 2500:
            deviation = 0.15
        elif maxscore < 5000:
            deviation = 0.1
        else:
            deviation = 0.04

        for i in range(numberOfBirds):
            Birds.append(Bird(brain=createChildModel(maxBrain, deviation),
                              height=200 + i,
                              gravitation=0,
                              color=(random.randint(0, 255),
                                    random.randint(0, 255),
                                    random.randint(0, 255))
                              )
                         )


if __name__ == "__main__":
    gener = 1

    # initialize window and game parameters
    display_width = 600
    display_height = 600
    white = (250, 250, 250)
    clock = pygame.time.Clock()


    highestScore = 0
    maxTuple = ()
    lastGenBirds = []

    while True:
        gener += 1
        random.seed(0)
        Birds = []
        Pipes = []
        score = 0

        generateBirds(30, lastGenBirds, highestScore, maxTuple)

        pygame.init()
        display = pygame.display.set_mode((display_width, display_height))
        display.fill(white)
        pygame.display.update()

        final_score = play_game(Birds, Pipes, highestScore, lastGenBirds, gener)




