import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import pygame
import random
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy

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
        self.score +=1

    def jump(self):
        self.gravitation = -7

    def think(self, pipe):
        input_data = [self.height/600, self.gravitation/100, pipe.width/600, pipe.higherOne/600, pipe.lowerOne/600]
        input_array = numpy.array([input_data])
        # predictions = self.brain.predict(input_array, verbose=0)

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


def birdsThinking(Birds, pipe):
    for bird in Birds:
        bird.think(pipe)

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
            # Wartości wag są losowane z odchyleniem od wag rodzica
            weights = [weight + numpy.random.normal(scale=deviation_factor) for weight in layer.get_weights()]
            child_model.add(Dense(units, input_shape=input_shape, activation=activation, weights=weights))
    child_model.compile(loss=parent_model.loss, optimizer=parent_model.optimizer, metrics=parent_model.metrics)
    return child_model

def birdsUpdate(Birds):
    for bird in Birds:
        bird.updateGravitation()
        bird.updateHeight()
        bird.updateScore()


def pipesUpdate(Pipes):
    if Pipes[0].width < 100:
        Pipes.pop(0)
    for pipe in Pipes:
        pipe.update()


def collision_with_pipe(pipe, Birds, lastGenBirds):
    if 150 < pipe.width < 160:
        newBirds = []
        for bird in Birds:
            if bird.height > pipe.lowerOne or bird.height < pipe.higherOne:
                lastGenBirds.append((Birds[Birds.index(bird)], bird.score))
                Birds.pop(Birds.index(bird))


def collision_with_boundaries(Birds, lastGenBirds):
    for bird in Birds:
        if bird.height > 600 or bird.height < 0:
            lastGenBirds.append((Birds[Birds.index(bird)], bird.score))
            Birds.pop(Birds.index(bird))


def generate_pipes(pipes):
    pipe_height = random.randint(150, 400)
    pipes.append(Pipe(lowerOne = pipe_height + 100, higherOne =pipe_height - 100, width=600))


def display_birds(birds):
    for bird in birds:
        pygame.draw.rect(display, bird.color, pygame.Rect(150, bird.height, 10, 10))


def display_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(display, window_color, pygame.Rect(pipe.width, 0, 15, pipe.higherOne))
        pygame.draw.rect(display, window_color, pygame.Rect(pipe.width, pipe.lowerOne, 15, 600 - pipe.lowerOne))


def display_score(score1):
    largeText = pygame.font.Font('freesansbold.ttf', 15)
    textSurf = largeText.render(f'Score: {score1}', True, window_color)
    display.blit(textSurf, (10, 10))

    largeText = pygame.font.Font('freesansbold.ttf', 15)
    textSurf = largeText.render(f'Highest Score: {highestScore}', True, window_color)
    display.blit(textSurf, (10, 30))





def play_game(Birds, Pipes, score, lastGenBirds):
    crashed = False
    timer = 0

    while crashed is not True:
        if timer == 0:
            generate_pipes(Pipes)
            timer = 200

        if timer%10==0:
            birdsThinking(Birds, Pipes[0])


        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                for bird in Birds:
                    bird.gravitation = -7


        # collision_with_pipe(Pipes[0], Birds)
        collision_with_boundaries(Birds, lastGenBirds)
        collision_with_pipe(Pipes[0], Birds, lastGenBirds)

        #display birds, pipes, score
        display.fill(black)
        display_birds(Birds)
        display_pipes(Pipes)
        display_score(score)

        #update everything
        pipesUpdate(Pipes)
        birdsUpdate(Birds)
        timer -= 1
        score += 1
        # clock.tick(60)

        #display display
        pygame.display.set_caption("FlappyBird" + "  " + "SCORE: " + str(score))
        pygame.display.update()

        if not Birds:
            print(lastGenBirds)
            break

    return score

import numpy as np


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




if __name__ == "__main__":
    attempt = 1
    colors = [(255, 89, 94),
              (255, 202, 58),
              (138, 201, 38),
              (25, 130, 196),
              (106, 76, 147),
              (255, 146, 76),
              (82, 166, 117),
              (232, 252, 207),
              (248, 173, 157)]
    ###### initialize required parameters ########
    display_width = 600
    display_height = 600
    green = (0, 255, 0)
    red = (255, 0, 0)
    black = (0, 0, 0)
    window_color = (200, 200, 200)
    clock = pygame.time.Clock()
    random.seed(69)
    lastGenBirds = []
    maxscore = 0
    maxTuple = ()
    highestScore = 0
    while True:
            random.seed(69)
            Birds = []
            Pipes = []
            score = 0


            if not lastGenBirds:
                for i in range(100):
                    Birds.append(Bird(brain=createModel(),
                                      height=200+i,
                                      gravitation=0,
                                      color=colors[i%9]))
            else:
                print("NEW GEN")



                for tup in lastGenBirds:
                    if maxscore < tup[1]:
                        maxscore = tup[1]
                        maxTuple = tup
                        highestScore = tup[1]
                maxBrain = maxTuple[0].brain
                lastGenBirds.clear()
                for i in range(100):
                    Birds.append(Bird(brain=createChildModel(maxBrain, 0.1),
                                      height=200 + i,
                                      gravitation=0,
                                      color=colors[i%9]))
            pygame.init()  # initialize pygame modules

            #### display game window #####
            display = pygame.display.set_mode((display_width, display_height))
            display.fill(window_color)
            pygame.display.update()

            final_score = play_game(Birds, Pipes, score, lastGenBirds)
            print(f"Attempt: {attempt}, FINAL SCORE: {final_score}")
            attempt+=1

            #JAKAS FUNKCJA CO BEDZIE USPRAWNIALA NASZE TESTOWANE PTASZORY

    # pygame.quit()


