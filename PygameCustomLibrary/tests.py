import main
import pygame

WIDTH, HEIGHT = 600, 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('test')


def updateWindow():
    pygame.display.update()


def main():
    test = True

    while test:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                test = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    test = False

        updateWindow()


if __name__ == "__main__":
    main()
