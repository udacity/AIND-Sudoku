import os, pygame

def load_image(name):
    """A better load of images."""
    fullname = os.path.join("images", name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() == None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error, message:
        print "Oops! Could not load image:", fullname
    return image, image.get_rect()


def load_sound(name):
    """A better load of sound."""
    fullname = os.path.join("sounds", name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print "Oops! Could not load sound:", fullname
    return sound


def load_music(name):
    """A better load of music."""
    fullname = os.path.join("sounds", name)
    try:
        pygame.mixer.music.load(fullname)
        pygame.mixer.music.play(-1, 0.0)
    except pygame.error, message:
        print "Oops! Could not load music:", fullname