from main import *
import pygame

WIN = pygame.display.set_mode((600, 600))
pygame.display.set_caption('test')


testBar = Bar((30, 30, 40, 300), 100, 100, barColor=(255, 0, 0), barBG=(150, 150, 150),
              barLevelMeter=True, txtColor=(0, 255, 0), txtBold=True, alignTxt=Direction.I_TOP,
              fillFromSide=Direction.BOTTOM, alignTxtToBar=True, updateTxtWithRender=True)


def update_window():
    WIN.fill((0, 150, 150))

    testBar.txt = f"{testBar.get_meter_percent()}%"
    testBar.render(WIN)

    Bar.update_cls_list()
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    test = True

    while test:
        clock.tick(60)
        Frame.increase_frame()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                test = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_MINUS:
                    testBar.remove(10, speed=0.5)
                if event.key == pygame.K_EQUALS:
                    testBar.add(10, speed=0.5)

        update_window()


if __name__ == "__main__":
    main()
