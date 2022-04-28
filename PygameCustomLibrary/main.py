import pygame
from typing import Union
from math import sin, cos, atan, sqrt, degrees, radians
pygame.font.init()


# --- Mechanic classes
class Vector:
    def __init__(self, xStart: int = 0, yStart: int = 0, x: float = 0, y: float = 0):
        self.xStart = xStart
        self.yStart = yStart
        self.x = x
        self.y = y
        try:
            self.angle = atan(self.y / self.x)
        except ZeroDivisionError:
            self.angle = 0
        self.len = sqrt(self.x**2 + self.y**2)

    def calc_angle(self):
        self.angle = degrees(atan(self.y / self.x))

        return self.angle

    def set_angle(self, newAngle: float = 0.0):
        self.angle = newAngle
        self.x = self.len * cos(radians(self.angle))
        self.y = self.len * sin(radians(self.angle))

    def __len__(self):
        self.len = sqrt(self.x**2 + self.y**2)

        return self.len

    def set_length(self, newLength: float = 0.0):
        self.len = newLength
        self.x = self.len * cos(radians(self.angle))
        self.y = self.len * sin(radians(self.angle))

    def __add__(self, other):
        totX = self.xStart + self.x + other.x
        totY = self.yStart + self.y + other.y
        newVector = Vector(self.xStart, self.yStart, totX, totY)

        return newVector

    def __sub__(self, other):
        totX = self.xStart + self.x - other.x
        totY = self.yStart + self.y - other.y
        newVector = Vector(self.xStart, self.yStart, totX, totY)

        return newVector

    def __mul__(self, other):
        if type(other) == Vector:
            x = self.x * other.x
            y = self.y * other.y

            return x, y

        else:
            totX = self.x * other
            totY = self.y * other
            newVector = Vector(self.xStart, self.yStart, totX, totY)

            return newVector

    def mirror(self, mirrorLine: str = 'h', lineAngle: int = 0):
        possibleMirrorLines = ['h', 'v', 'd']
        if mirrorLine not in possibleMirrorLines:
            mirrorLine = 'h'

        if mirrorLine == 'h':
            lineAngle = 0
        elif mirrorLine == 'v':
            lineAngle = 90

        tempAngle = self.angle + lineAngle
        newAngle = tempAngle - (tempAngle - 180) * 2
        self.angle = newAngle - lineAngle

        if mirrorLine == 'h':
            self.x = -self.x
        elif mirrorLine == 'v':
            self.y = -self.y
        else:
            self.x = self.len * cos(radians(self.angle))
            self.y = self.len * sin(radians(self.angle))

    def turn(self, turnAngle: float = 0.0):
        newAngle = self.angle + turnAngle
        self.set_angle(newAngle)

    def __repr__(self):
        return f'{self.x}, {self.y}'


class Direction:
    LEFT = 'l'
    RIGHT = 'r'
    TOP = 't'
    BOTTOM = 'b'
    CENTER = 'c'
    I_LEFT = 'il'
    I_RIGHT = 'ir'
    I_TOP = 'it'
    I_BOTTOM = 'ib'


class Tag:
    tagList = []

    def __init__(self):
        Tag.tagList.append(self)


# --- Video classes
class Frame:
    frame = 0

    @classmethod
    def increase_frame(cls, increment: int = 1):
        cls.frame += increment


class Sprite:
    assetsFolderPath = ''

    def __init__(self, source: Union[str, pygame.Surface], x: int = 0, y: int = 0, sheetPath: str = '',
                 assetPath: bool = False):
        if type(source) == str:
            if assetPath:
                self.path = source
            else:
                if Sprite.assetsFolderPath[-1] != '\\':
                    Sprite.assetsFolderPath += '\\'
                self.path = Sprite.assetsFolderPath + source
            self.sprite = pygame.image.load(self.path)
        else:
            self.path = sheetPath
            self.sprite = source
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()
        self.x = x
        self.y = y

    def render(self, display, scale: tuple[int, int] = None, scaleFactor: float = 1.0):
        if scale is not None:
            self.sprite = pygame.transform.scale(self.sprite, (scale[0], scale[1]))

            self.width = self.sprite.get_width()
            self.height = self.sprite.get_height()
        elif scaleFactor != 1:
            newWidth = round(self.sprite.get_width() * scaleFactor)
            newHeight = round(self.sprite.get_height() * scaleFactor)
            self.sprite = pygame.transform.scale(self.sprite, (newWidth, newHeight))

            self.width = self.sprite.get_width()
            self.height = self.sprite.get_height()

        display.blit(self.sprite, (self.x, self.y))

    @staticmethod
    def split_sheet(path: str, imagesOnSheet: int = 1, assetPath: bool = False):
        if not assetPath:
            if Sprite.assetsFolderPath[-1] != '\\':
                Sprite.assetsFolderPath += '\\'
            path = Sprite.assetsFolderPath + path
        sheet = pygame.image.load(path).convert_alpha()
        splitSheetList = []
        sheetWidth = sheet.get_width()
        sheetHeight = sheet.get_height()

        singleSpriteWidth = round(sheetWidth / imagesOnSheet)

        for sprite in range(imagesOnSheet):
            sheetPart = pygame.Surface((singleSpriteWidth, sheetHeight)).convert_alpha()
            sheetPart.fill((255, 255, 255, 0))
            sheetPart.blit(sheet, (-sprite * singleSpriteWidth, 0))
            splitSheetList.append(Sprite(sheetPart, sheetPath=path))

        return splitSheetList


# TODO: split Animation class --> Animation.Image & Animation.Move
class Animation:
    current_animations = []
    draw_animations = []

    def __init__(self, spriteSheet: list = None, startFrame: Union[int, Frame] = 0, frameStep: int = 1,
                 sheetIndex: int = 0, spriteX: int = 0, spriteY: int = 0, spriteScale: tuple[int, int] = None,
                 playOnCreation: bool = True, inAnimationList: bool = True):
        self.spriteSheet = spriteSheet
        self.sheetLen = len(spriteSheet)
        self.frameStep = frameStep
        self.sheetIndex = sheetIndex
        self.spriteX = spriteX
        self.spriteY = spriteY
        self.spriteScale = spriteScale
        self.frameInCycle = 0

        if type(startFrame) == Frame:
            self.startFrame = startFrame.frame
        else:
            self.startFrame = startFrame

        if spriteScale is not None:
            self.width = spriteScale[0]
            self.height = spriteScale[1]
        else:
            self.width = self.spriteSheet[0].width
            self.height = self.spriteSheet[0].height

        Animation.current_animations.append(self)
        if inAnimationList:
            Animation.draw_animations.append(self)

        if not playOnCreation:
            self.stop_animation()

    def render(self, display, x: int = None, y: int = None, scale: tuple = None):
        sprite = self.spriteSheet[self.sheetIndex]
        if x is None:
            sprite.x = self.spriteX
        else:
            sprite.x = x
        if y is None:
            sprite.y = self.spriteY
        else:
            sprite.y = y
        if scale is None:
            spriteScale = self.spriteScale
        else:
            spriteScale = scale

        sprite.render(display, spriteScale)

    @classmethod
    def render_cls_list(cls, display):
        for animation in cls.draw_animations:
            animation.render(display)

    def update_animation(self, currentFrame: Union[int, Frame] = 0):
        if type(currentFrame) == Frame:
            currentFrame = currentFrame.frame

        dFrame = currentFrame - self.startFrame
        self.frameInCycle = dFrame % (self.sheetLen * self.frameStep)
        self.sheetIndex = self.frameInCycle // self.frameStep

    @classmethod
    def update_cls_list(cls, currentFrame: Union[int, Frame] = 0):
        if type(currentFrame) == Frame:
            currentFrame = currentFrame.frame

        for animation in cls.current_animations:
            animation.update_animation(currentFrame)

    def stop_animation(self, currentFrame: Union[int, Frame] = 0):
        if type(currentFrame) == Frame:
            currentFrame = currentFrame.frame

        Animation.current_animations.remove(self)

        dFrame = currentFrame - self.startFrame
        self.frameInCycle = dFrame % (self.sheetLen * self.frameStep)

    def play_animation(self, currentFrame: Union[int, Frame] = 0):
        if type(currentFrame) == Frame:
            currentFrame = currentFrame.frame

        Animation.current_animations.append(self)

        self.startFrame = currentFrame - self.frameInCycle


# --- object classes
class Text:
    def __init__(self, txt: str = '', txtColor: tuple[int, int, int] = (0, 0, 0), x: int = 0, y: int = 0,
                 font: str = 'helvetica', fontSize: int = None, txtBold: bool = False, txtItalic: bool = False):
        self.txt = txt
        self.txtColor = txtColor
        self.x = x
        self.y = y
        self.font = font
        self.fontSize = fontSize
        self.txtBold = txtBold
        self.txtItalic = txtItalic

        textBoxFont = pygame.font.SysFont(font, self.fontSize, txtBold, txtItalic)
        self.textBoxText = textBoxFont.render(txt, True, txtColor)

    def update_txt(self):
        textBoxFont = pygame.font.SysFont(self.font, self.fontSize, self.txtBold, self.txtItalic)
        self.textBoxText = textBoxFont.render(self.txt, True, self.txtColor)

    def render(self, display):
        txtXPos = self.x - self.textBoxText.get_width() / 2
        txtYPos = self.y - self.textBoxText.get_height() / 2

        display.blit(self.textBoxText, (txtXPos, txtYPos))


class Shape:
    SHAPE_TYPES = ['polygon', 'circle', 'rectangle', 'line']

    def __init__(self, shape: str = 'polygon', color: tuple[int, int, int] = (0, 0, 0), corners: tuple = (),
                 width: int = 0, radius: int = 0, centerPoint: tuple[int, int] = (0, 0), hitbox: bool = False):
        if shape in Shape.SHAPE_TYPES and not ((shape == 'rectangle' or shape == 'line') and len(corners) != 2):
            self.shape = shape
        else:
            self.shape = 'polygon'
        self.color = color
        self.corners = corners
        self.width = width
        self.radius = radius
        self.x = centerPoint[0]
        self.y = centerPoint[1]
        if hitbox and shape != 'circle':
            minX, maxX, minY, maxY = self.calc_min_max()
            self.hitbox = pygame.Rect(minX, minY, maxX - minX, maxY - minY)
        elif hitbox and shape == 'circle':
            self.hitbox = pygame.Rect(self.x - radius, self.y - radius, 2 * radius, 2 * radius)
        else:
            self.hitbox = None

    def calc_min_max(self):
        cornerList = list(self.corners)[:]
        cornerList.sort(key=lambda x: x[0])
        minX = cornerList[0][0]
        maxX = cornerList[-1][0]

        cornerList.sort(key=lambda x: x[1])
        minY = cornerList[0][1]
        maxY = cornerList[-1][1]

        return minX, maxX, minY, maxY

    def moveHitbox(self):
        if self.shape != 'circle':
            minX, maxX, minY, maxY = self.calc_min_max()
            self.hitbox = pygame.Rect(minX, minY, maxX - minX, maxY - minY)
        elif self.shape == 'circle':
            self.hitbox = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)
        else:
            self.hitbox = None

    def render(self, display):
        if self.shape == 'polygon':
            pygame.draw.polygon(display, self.color, self.corners, self.width)
        elif self.shape == 'circle':
            pygame.draw.circle(display, self.color, (self.x, self.y), self.radius, self.width)
        elif self.shape == 'rectangle':
            minX, maxX, minY, maxY = self.calc_min_max()
            width = maxX - minX
            height = maxY - minY
            pygame.draw.rect(display, self.color, pygame.Rect(minX, minY, width, height), self.width)
        elif self.shape == 'line':
            pygame.draw.line(display, self.color, self.corners[0], self.corners[1], self.width)


class Button:
    BUTTON_TYPES = ('switch', 'push')
    ALIGNMENTS = ('il', 'c', 'ir')

    buttonList = []
    pushButtonList = []

    def __init__(self, rect: Union[tuple[int, int, int, int], pygame.Rect],
                 buttonColor: tuple[int, int, int] = (255, 255, 255), txt: str = '',
                 txtColor: tuple[int, int, int] = (0, 0, 0), alignTxt: str = Direction.CENTER,
                 font: str = 'helvetica', fontSize: int = None, txtBold: bool = False, txtItalic: bool = False,
                 topTxtGap: int = 5, sideTxtGap: int = 5, img: Union[Sprite, Animation] = None,
                 alignImg: str = Direction.CENTER, imgSize: tuple[int, int] = None, topImgGap: int = 5,
                 sideImgGap: int = 5, button3D: bool = False, buttonShadowColor: tuple[int, int, int] = (0, 0, 0),
                 buttonShadowDepth: int = 3, buttonPressed: bool = False, buttonType: str = 'switch',
                 inButtonList: bool = True):

        self.buttonColor = buttonColor
        self.txt = txt
        self.txtColor = txtColor
        self.font = font
        self.fontSize = fontSize
        self.txtBold = txtBold
        self.txtItalic = txtItalic
        self.topTxtGap = topTxtGap
        self.sideTxtGap = sideTxtGap
        self.img = img
        self.imgSize = imgSize
        self.topImgGap = topImgGap
        self.sideImgGap = sideImgGap
        self.button3D = button3D
        self.buttonShadowColor = buttonShadowColor
        self.buttonShadowDepth = buttonShadowDepth
        self.buttonPressed = buttonPressed

        if buttonType not in Button.BUTTON_TYPES:
            self.buttonType = 'switch'
        else:
            self.buttonType = buttonType

        if alignTxt not in Button.ALIGNMENTS:
            self.alignTxt = Direction.CENTER
        else:
            self.alignTxt = alignTxt

        if alignImg not in Button.ALIGNMENTS:
            self.alignImg = Direction.CENTER
        else:
            self.alignImg = alignImg

        if type(rect) == tuple:
            self.buttonRect = pygame.Rect(rect)
        else:
            self.buttonRect = rect

        if txt != '':
            if fontSize is None:
                fontMaxHeight = self.buttonRect.height - 2 * self.topTxtGap
                fontMaxWidth = ((self.buttonRect.width - 2 * self.sideTxtGap) // len(self.txt)) * 2

                if fontMaxWidth <= fontMaxHeight:
                    self.fontSize = fontMaxWidth
                else:
                    self.fontSize = fontMaxHeight
            else:
                self.fontSize = fontSize
        else:
            self.fontSize = 10

        buttonFont = pygame.font.SysFont(font, self.fontSize, txtBold, txtItalic)
        self.buttonText = buttonFont.render(txt, True, txtColor)

        if inButtonList:
            Button.buttonList.append(self)
            if self.buttonType == 'push':
                Button.pushButtonList.append(self)

    def update_button_txt(self):
        buttonFont = pygame.font.SysFont(self.font, self.fontSize, self.txtBold, self.txtItalic)
        self.buttonText = buttonFont.render(self.txt, True, self.txtColor)

    def update_button_rect(self, rect: Union[tuple[int, int, int, int], pygame.Rect]):
        if type(rect) == tuple:
            self.buttonRect = pygame.Rect(rect)
        else:
            self.buttonRect = rect

    def render_button(self, display):
        if self.button3D and not self.buttonPressed:
            depth = self.buttonShadowDepth
            button = pygame.Rect(self.buttonRect.x - depth, self.buttonRect.y - depth,
                                 self.buttonRect.width, self.buttonRect.height)

            shadowPoints = [(self.buttonRect.x + self.buttonRect.width, self.buttonRect.y),
                            (self.buttonRect.x + self.buttonRect.width, self.buttonRect.y + self.buttonRect.height),
                            (self.buttonRect.x, self.buttonRect.y + self.buttonRect.height),
                            (self.buttonRect.x - depth, self.buttonRect.y + self.buttonRect.height - depth),
                            (self.buttonRect.x + self.buttonRect.width - depth, self.buttonRect.y - depth)]

            pygame.draw.polygon(display, self.buttonShadowColor, shadowPoints)
        else:
            button = self.buttonRect

        pygame.draw.rect(display, self.buttonColor, button)

    def render_txt(self, display):
        if self.button3D and not self.buttonPressed:
            xyCorrection = 3
        else:
            xyCorrection = 0

        if self.alignTxt == Direction.I_RIGHT:
            txtXPos = self.buttonRect.x + self.buttonRect.width - self.sideTxtGap - self.buttonText.get_width()\
                      - xyCorrection
        elif self.alignTxt == Direction.I_LEFT:
            txtXPos = self.buttonRect.x + self.sideTxtGap - xyCorrection
        else:
            txtXPos = self.buttonRect.x + (self.buttonRect.width - self.buttonText.get_width()) // 2 - xyCorrection

        txtYPos = self.buttonRect.y + (self.buttonRect.height - self.buttonText.get_height()) // 2 - xyCorrection

        display.blit(self.buttonText, (txtXPos, txtYPos))

    def render_img(self, display):
        imgMaxHeight = self.buttonRect.height - 2 * self.topImgGap
        imgMaxWidth = self.buttonRect.width - 2 * self.sideImgGap
        maxXFactor = imgMaxWidth / self.img.width
        maxYFactor = imgMaxHeight / self.img.height

        if maxXFactor <= maxYFactor:
            self.img.width = self.img.width * maxXFactor
            self.img.height = self.img.height * maxYFactor
        else:
            self.img.width = self.img.width * maxYFactor
            self.img.height = self.img.height * maxYFactor

        if self.button3D and not self.buttonPressed:
            xyCorrection = 3
        else:
            xyCorrection = 0

        if self.alignImg == Direction.I_RIGHT:
            self.img.x = self.buttonRect.x + self.buttonRect.width - self.sideImgGap - self.img.width - xyCorrection
        elif self.alignImg == Direction.I_LEFT:
            self.img.x = self.buttonRect.x + self.sideImgGap - xyCorrection
        else:
            self.img.x = self.buttonRect.x + (self.buttonRect.width - self.img.width) // 2 - xyCorrection

        self.img.y = self.buttonRect.y + (self.buttonRect.height - self.img.height) // 2 - xyCorrection

        if type(self.img) == Sprite:
            self.img.render(display, scale=(self.img.width, self.img.height))
        elif type(self.img) == Animation:
            self.img.render(display, x=self.img.x, y=self.img.y,
                            scale=(self.img.width, self.img.height))

    def render(self, display):
        self.render_button(display)
        if self.img is not None:
            self.render_img(display)
        self.render_txt(display)

    @classmethod
    def render_cls_list(cls, display):
        for button in cls.buttonList:
            button.render(display)

    @classmethod
    def push_button_release(cls):
        for button in cls.pushButtonList:
            button.buttonPressed = False

    def check_mouse_collision(self, scene=None, updateButtonState: bool = True):
        if scene is not None:
            if not scene.check_object_in_scene(self):
                return False
        mX, mY = pygame.mouse.get_pos()
        mouseHitbox = pygame.Rect(mX, mY, 2, 2)
        if self.buttonRect.colliderect(mouseHitbox):
            if updateButtonState:
                self.buttonPressed = not self.buttonPressed
            return True
        else:
            return False

    def swap_button_state(self):
        self.buttonPressed = not self.buttonPressed

    def unpress_button(self):
        self.buttonPressed = False


class Bar:
    ALIGNMENTS = ('l', 'il', 'c', 'r', 'ir', 't', 'it', 'b', 'ib')

    removeFromBar = []
    addToBar = []

    def __init__(self, rect: Union[tuple[int, int, int, int], pygame.Rect], totalVolume: float = 1.0,
                 currentVolume: float = 0.0, barColor: tuple[int, int, int] = (0, 0, 0),
                 barBG: tuple[int, int, int, ...] = (0, 0, 0, 255), barLevelMeter: bool = False,
                 barLevelMeterWidth: int = None, barLevelMeterHeight: int = None,
                 barLevelMeterColor: tuple[int, int, int] = (0, 0, 0), barSurroundWidth: int = 0,
                 barSurroundColor: tuple[int, int, int] = (0, 0, 0), fillFromSide: str = Direction.RIGHT,
                 animationSpeed: float = 1.0, txt: str = '', txtColor: tuple[int, int, int] = (0, 0, 0),
                 font: str = 'helvetica', fontSize: int = None, txtBold: bool = False, txtItalic: bool = False,
                 topTxtGap: int = None, sideTxtGap: int = None, alignTxt: str = Direction.TOP,
                 alignTxtToBar: bool = False, updateTxtWithRender: bool = False):

        self.totalVolume = totalVolume
        self.currentVolume = self.realBarVolume = currentVolume
        self.barColor = barColor
        self.barBG = barBG
        self.barLevelMeterColor = barLevelMeterColor
        self.barSurroundWidth = barSurroundWidth
        self.barSurroundColor = barSurroundColor
        self.animationSpeed = animationSpeed
        self.txt = txt
        self.txtColor = txtColor
        self.font = font
        self.txtBold = txtBold
        self.txtItalic = txtItalic
        self.alignTxtToBar = alignTxtToBar
        self.updateTextWithRender = updateTxtWithRender

        if topTxtGap is None:
            self.topTxtGap = 3
        else:
            self.topTxtGap = topTxtGap

        if sideTxtGap is None:
            self.sideTxtGap = 3
        else:
            self.sideTxtGap = sideTxtGap

        if type(rect) == tuple:
            self.barRect = pygame.Rect(rect)
        else:
            self.barRect = rect

        if txt != '':
            if fontSize is None:
                fontMaxHeight = self.barRect.height - 2 * self.topTxtGap
                fontMaxWidth = ((self.barRect.width - 2 * self.sideTxtGap) // len(self.txt)) * 2

                if fontMaxWidth <= fontMaxHeight:
                    self.fontSize = fontMaxWidth
                else:
                    self.fontSize = fontMaxHeight
            else:
                self.fontSize = fontSize
        else:
            self.fontSize = 10

        if fillFromSide == Direction.RIGHT or fillFromSide == Direction.BOTTOM:
            self.fillFromSide = fillFromSide
        else:
            if self.barRect.width >= self.barRect.height:
                self.fillFromSide = Direction.RIGHT
            else:
                self.fillFromSide = Direction.BOTTOM

        if barLevelMeter:
            if barLevelMeterWidth is None:
                if self.fillFromSide == Direction.BOTTOM:
                    self.barLevelMeterWidth = self.barRect.width
                else:
                    self.barLevelMeterWidth = 2
            else:
                self.barLevelMeterWidth = barLevelMeterWidth

            if barLevelMeterHeight is None:
                if self.fillFromSide == Direction.RIGHT:
                    self.barLevelMeterHeight = self.barRect.height
                else:
                    self.barLevelMeterHeight = 2
            else:
                self.barLevelMeterHeight = barLevelMeterHeight
        else:
            self.barLevelMeterWidth = 0
            self.barLevelMeterHeight = 0

        self.barSurroundRect = pygame.Rect(self.barRect.x - self.barSurroundWidth,
                                           self.barRect.y - self.barSurroundWidth,
                                           self.barRect.width + 2 * self.barSurroundWidth,
                                           self.barRect.height + 2 * self.barSurroundWidth)

        if self.fillFromSide == Direction.BOTTOM:
            levelMeterExtend = (self.barLevelMeterWidth - self.barRect.width) / 2
            self.barLevelMeter = pygame.Rect(self.barRect.x - levelMeterExtend,
                                             self.barRect.y - self.barLevelMeterHeight,
                                             self.barLevelMeterWidth, self.barLevelMeterHeight)
        else:
            levelMeterExtend = (self.barLevelMeterHeight - self.barRect.height) / 2
            self.barLevelMeter = pygame.Rect(self.barRect.x + self.barRect.width,
                                             self.barRect.y - levelMeterExtend,
                                             self.barLevelMeterWidth, self.barLevelMeterHeight)

        if alignTxt not in Bar.ALIGNMENTS:
            self.alignTxt = Direction.TOP
        else:
            self.alignTxt = alignTxt

        self.barFont = pygame.font.SysFont(self.font, self.fontSize, self.txtBold, self.txtItalic)
        self.barText = self.barFont.render(self.txt, True, self.txtColor)

    def update_bar_txt(self):
        self.barFont = pygame.font.SysFont(self.font, self.fontSize, self.txtBold, self.txtItalic)
        self.barText = self.barFont.render(self.txt, True, self.txtColor)

    def set_meter_percent(self, percentage: float = 0.0):
        self.currentVolume = self.realBarVolume = self.totalVolume * percentage / 100

    def get_meter_percent(self, value=None, realVolume: bool = False, decimals: int = 1) -> float:
        if value is None:
            if not realVolume:
                value = self.currentVolume
            else:
                value = self.realBarVolume
        percent = round(value / self.totalVolume * 100, decimals)
        if percent < 0:
            percent = 0.0
        return percent

    def get_value_from_percent(self, percent) -> float or int:
        value = self.totalVolume * percent / 100
        return value

    def remove(self, value: float = 1.0, percentage: bool = False, slowRemove: bool = True, speed: float = 1.0):
        self.animationSpeed = speed
        if percentage:
            value = self.get_value_from_percent(value)
        if self.realBarVolume - value < 0:
            self.realBarVolume = 0
        else:
            self.realBarVolume -= value

        if slowRemove:
            Bar.removeFromBar.append(self)
        else:
            self.currentVolume -= value

    def add(self, value: float = 1.0, percentage: bool = False, slowAdd: bool = True, speed: float = 1.0):
        self.animationSpeed = speed
        if percentage:
            value = self.get_value_from_percent(value)
        if self.realBarVolume + value > self.totalVolume:
            self.realBarVolume = self.totalVolume
        else:
            self.realBarVolume += value

        if slowAdd:
            Bar.addToBar.append(self)
        else:
            self.currentVolume += value

    def render_bar_txt(self, display):
        if self.updateTextWithRender:
            self.update_bar_txt()

        if self.alignTxtToBar:
            percent = self.get_meter_percent()
            if self.fillFromSide == Direction.BOTTOM:
                barLength = self.barRect.height * percent / 100
                bar = pygame.Rect(self.barRect.x, self.barRect.y + self.barRect.height - barLength,
                                  self.barRect.width, barLength)

            else:
                barLength = self.barRect.width * percent / 100
                bar = pygame.Rect(self.barRect.x, self.barRect.y, barLength, self.barRect.height)
        else:
            bar = self.barRect

        if self.alignTxt == Direction.LEFT:
            txtXPos = bar.x - self.sideTxtGap - self.barText.get_width()
            txtYPos = bar.y + (bar.height - self.barText.get_height()) // 2

        elif self.alignTxt == Direction.I_LEFT:
            txtXPos = bar.x + self.sideTxtGap
            txtYPos = bar.y + (bar.height - self.barText.get_height()) // 2

        elif self.alignTxt == Direction.CENTER:
            txtXPos = bar.x + (bar.width - self.barText.get_width()) // 2
            txtYPos = bar.y + (bar.height - self.barText.get_height()) // 2

        elif self.alignTxt == Direction.RIGHT:
            txtXPos = bar.x + bar.width + self.sideTxtGap
            txtYPos = bar.y + (bar.height - self.barText.get_height()) // 2

        elif self.alignTxt == Direction.I_RIGHT:
            txtXPos = bar.x + bar.width - self.sideTxtGap - self.barText.get_width()
            txtYPos = bar.y + (bar.height - self.barText.get_height()) // 2

        elif self.alignTxt == Direction.TOP:
            txtXPos = bar.x + (bar.width - self.barText.get_width()) // 2
            txtYPos = bar.y - self.sideTxtGap - self.barText.get_height()

        elif self.alignTxt == Direction.I_TOP:
            txtXPos = bar.x + (bar.width - self.barText.get_width()) // 2
            txtYPos = bar.y + self.sideTxtGap

        elif self.alignTxt == Direction.BOTTOM:
            txtXPos = bar.x + (bar.width - self.barText.get_width()) // 2
            txtYPos = bar.y + bar.height + self.sideTxtGap

        else:
            txtXPos = bar.x + (bar.width - self.barText.get_width()) // 2
            txtYPos = bar.y + bar.height - self.sideTxtGap - self.barText.get_height()

        if self.alignTxtToBar:
            if txtXPos < bar.x + self.sideTxtGap and self.alignTxt != Direction.LEFT:
                txtXPos = bar.x + self.sideTxtGap

            elif txtXPos < bar.x - self.sideTxtGap - self.barText.get_width() and self.alignTxt == Direction.LEFT:
                txtXPos = bar.x - self.sideTxtGap - self.barText.get_width()

            elif txtXPos > bar.x + bar.width and self.alignTxt != Direction.RIGHT:
                txtXPos = bar.x + bar.width

            elif txtXPos > bar.x + bar.width + self.barText.get_width() and self.alignTxt == Direction.RIGHT:
                txtXPos = bar.x + bar.width - self.sideTxtGap - self.barText.get_width()
        else:
            if txtXPos < self.sideTxtGap:
                txtXPos = self.sideTxtGap
            elif txtXPos > display.get_width():
                txtXPos = display.get_width() - self.sideTxtGap - self.barText.get_width()

        if self.alignTxtToBar:
            if txtYPos > bar.y + bar.height - self.topTxtGap - self.barText.get_height() and \
                    (self.alignTxt == Direction.I_TOP or self.alignTxt == Direction.BOTTOM):
                txtYPos = bar.y + bar.height - self.topTxtGap - self.barText.get_height()
        else:
            if txtYPos < self.topTxtGap:
                txtYPos = self.topTxtGap
            elif txtYPos > display.get_height():
                txtYPos = display.get_height() - self.topTxtGap - self.barText.get_height()

        display.blit(self.barText, (txtXPos, txtYPos))

    def render_level_meter(self, display):
        percent = self.get_meter_percent()
        if self.fillFromSide == Direction.BOTTOM:
            barLength = self.barRect.height * percent / 100

            levelMeterExtend = (self.barLevelMeterWidth - self.barRect.width) / 2
            self.barLevelMeter = pygame.Rect(self.barRect.x - levelMeterExtend,
                                             self.barRect.y + self.barRect.height - barLength -
                                             self.barLevelMeterHeight,
                                             self.barLevelMeterWidth, self.barLevelMeterHeight)
        else:
            barLength = self.barRect.width * percent / 100

            levelMeterExtend = (self.barLevelMeterHeight - self.barRect.height) / 2
            self.barLevelMeter = pygame.Rect(self.barRect.x + barLength,
                                             self.barRect.y - levelMeterExtend,
                                             self.barLevelMeterWidth, self.barLevelMeterHeight)

        pygame.draw.rect(display, self.barLevelMeterColor, self.barLevelMeter)

    def render_bar(self, display):
        percent = self.get_meter_percent()
        if self.fillFromSide == Direction.BOTTOM:
            barLength = self.barRect.height * percent / 100
            bar = pygame.Rect(self.barRect.x, self.barRect.y + self.barRect.height - barLength,
                              self.barRect.width, barLength)

        else:
            barLength = self.barRect.width * percent / 100
            bar = pygame.Rect(self.barRect.x, self.barRect.y, barLength, self.barRect.height)

        bg = pygame.Surface((self.barRect.width, self.barRect.height)).convert_alpha()
        bg.fill(self.barBG)
        display.blit(bg, (self.barRect.x, self.barRect.y))
        pygame.draw.rect(display, self.barColor, bar)

    def render(self, display):
        self.render_bar(display)
        self.render_level_meter(display)
        self.render_bar_txt(display)

    def update_bar_animation(self):
        if self.realBarVolume < self.currentVolume:
            self.currentVolume -= self.animationSpeed
            if self.currentVolume <= self.realBarVolume:
                Bar.removeFromBar.remove(self)
        elif self.realBarVolume > self.currentVolume:
            self.currentVolume += self.animationSpeed
            if self.currentVolume >= self.realBarVolume:
                Bar.addToBar.remove(self)
        else:
            if self in Bar.removeFromBar:
                Bar.removeFromBar.remove(self)
            if self in Bar.addToBar:
                Bar.addToBar.remove(self)

    @classmethod
    def update_cls_list(cls):
        for bar in cls.removeFromBar + cls.addToBar:
            bar.update_bar_animation()


# --- Scene classes
# FINISH BOARD class
class Board:
    class Tile:
        def __init__(self, x: int = 0, y: int = 0, sprite: Sprite = None, addToBoard=None, sortBoard: bool = True,
                     tags: list = None):
            self.x = x
            self.y = y
            self.sprite = sprite
            self.board = addToBoard
            self.tags = tags

            if addToBoard is not None:
                added = False
                for index, tile in enumerate(addToBoard.board):
                    if tile.x == self.x and tile.y == self.y:
                        addToBoard.board[index] = self
                        added = True
                if not added:
                    addToBoard.board.append(self)
                    if sortBoard:
                        addToBoard.sort()

        def check_for_tag(self, tag: Tag = None):
            if tag in self.tags:
                return True
            else:
                return False

        def render(self, display, xPos: int = 0, yPos: int = 0, sprite: Sprite = None):
            if sprite is not None:
                display.blit(sprite, (xPos, yPos))

            elif self.sprite is not None:
                display.blit(self.sprite, (xPos, yPos))

        def __repr__(self):
            return f"Tile pos = {self.x}, {self.y} - Board = {self.board}"

    def __init__(self, width: int = 1, length: int = 1, tileSprites: list = None, spritePattern: list = None,
                 tileTags: list = None, generateTiles: bool = True):
        self.length = length
        self.width = width
        self.tileSprites = tileSprites
        self.spritePattern = spritePattern
        self.board = []

        if generateTiles and tileSprites:
            for pos in range(width * length):
                x = pos % width
                y = pos // width
                if spritePattern is None:
                    sprite = tileSprites[pos % len(tileSprites)]
                else:
                    patternIndex = pos % len(spritePattern)
                    sprite = tileSprites[spritePattern[patternIndex]]
                self.Tile(x, y, sprite, self, tags=tileTags)

    def sort(self):
        numBoardWidth = len(str(self.width))
        try:
            self.board.sort(key=lambda a: int(str(a.y) + str(a.x).zfill(numBoardWidth)))
        except AttributeError:
            pass

    def getTileSize(self, boardRect: tuple[int, int, int, int] = (0, 0, 100, 100)):
        boardLength = boardRect[2]
        boardWidth = boardRect[3]
        maxTileX = 0
        maxTileY = 0
        for tile in self.board:
            if tile.x > maxTileX:
                maxTileX = tile.x
            if tile.y > maxTileY:
                maxTileY = tile.y

        tileSizeH = boardWidth // (maxTileX + 1)
        tileSizeV = boardLength // (maxTileY + 1)

        return tileSizeH, tileSizeV

    def render(self, display, boardRect: tuple[int, int, int, int] = (0, 0, 100, 100)):
        if self.board:
            tileSizeH, tileSizeV = self.getTileSize(boardRect)

            for tile in self.board:
                if tile.sprite is not None:
                    tileXPos = tile.x * tileSizeH
                    tileYPos = tile.y * tileSizeV
                    tile.render(display, tileXPos, tileYPos)

    @classmethod
    def mult_render(cls, display, boardList: list = None):
        if boardList is not None:
            maxLength = 1
            maxWidth = 1
            for board in boardList:
                if board.length > maxLength:
                    maxLength = board.length
                if board.width > maxWidth:
                    maxWidth = board.width
            totalBoard = cls(maxLength, maxWidth)
            for board in boardList:
                totalBoard.board += [tile for tile in board.board]
            totalBoard.sort()
            totalBoard.render(display)

    def __repr__(self):
        return str(self.board)


class Scene:
    selectedScene = None
    sceneList = []

    def __init__(self, objectInSceneList: list = None, bgColor: tuple[int, int, int] = (0, 0, 0)):
        self.objectInSceneList = objectInSceneList
        self.bgColor = bgColor

    def render_scene(self, display):
        display.fill(self.bgColor)
        for obj in self.objectInSceneList:
            obj.render(display)

    def check_object_in_scene(self, obj):
        if obj in self.objectInSceneList:
            return True
        else:
            return False

    @classmethod
    def add_to_scene_objects(cls, additions: Union[list, tuple] = None):
        if additions is not None:
            for obj in additions:
                cls.sceneList.append(obj)


# TODO: update help function
def help_commands(problem=None):
    helpString = """
    Help Menu
    -------------------------------------------------------------------
    Classes:
    Vector, Tag, Frame, Sprite, Animation, Text, Shape, Button, Bar, Board, Board.Tile, Scene
    --------------------------------------------------------------------
    Special Lines:
    Animation.update_cls_list()     --> update all animation frames
    Bar.update_cls_list()           --> update all animated bars
    Scene.selectedScene = ...       --> define first scene
    """
    if problem == Animation:
        print('continuing animation frames - Animation.update_cls_list()')
    elif problem == Bar:
        print('continuing bar slowAdd / slowRemove - Bar.updat_cls.list()')
    elif problem == Scene:
        print('define first scene - Scene.selectedScene = ...')
    else:
        print(helpString)
