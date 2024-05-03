#!/usr/bin/python
# Paperclip_Play - 5th Pi Birthday Bash activity  By Mike Cook - Febuary 2017
# Infinate note hold version
import pygame, time, os
import wiringpi as io

pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
pygame.display.set_caption("Paperclip player")
screen = pygame.display.set_mode([300,40],0,32)
pygame.mixer.quit()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.event.set_allowed(None)
pygame.event.set_allowed([pygame.MOUSEBUTTONDOWN,pygame.KEYDOWN,pygame.QUIT])
font = pygame.font.Font(None, 36) 
pinList = [21,26,20,19,16,13,6,12,5] # GPIO pins

def main():
   initGPIO()
   print"Stylophone - By Mike Cook"
   drawWords("Play the paperclip",36,6)
   while True:
      checkForEvent()
      for pin in range (0,len(pinList)):
        if io.digitalRead(pinList[pin]) == 0:
           pygame.mixer.music.load("Marimba/"+str(pin)+".wav")
           pygame.mixer.music.set_volume(1.0)
           pygame.mixer.music.play(-1,0.0)
           time.sleep(0.030)
           while io.digitalRead(pinList[pin]) == 0:
               pass
           pygame.mixer.music.fadeout(100)
           time.sleep(0.030) # debounce time
           
def initGPIO():
   try :
      io.wiringPiSetupGpio()
   except :
      print"start IDLE with 'gksudo idle' from command line"
      os._exit(1)
   for pin in range (0,len(pinList)):
      io.pinMode(pinList[pin],0) # make pin into an input
      io.pullUpDnControl(pinList[pin],2) # enable pull up
      
def drawWords(words,x,y) :
        textSurface = pygame.Surface((len(words)*12,36))
        textRect = textSurface.get_rect()
        textRect.left = x ; textRect.top = y
        pygame.draw.rect(screen,(0,0,0), (x,y,len(words)*12,26), 0)
        textSurface = font.render(words, True, (255,255,255), (0,0,0))
        screen.blit(textSurface, textRect)
        pygame.display.update()
      
def terminate(): # close down the program
    pygame.mixer.quit()
    pygame.quit()
    os._exit(1)
 
def checkForEvent(): # keyboard commands
    event = pygame.event.poll()
    if event.type == pygame.QUIT :
         terminate()
    if event.type == pygame.KEYDOWN :
       if event.key == pygame.K_ESCAPE :
          terminate()
             
# Main program logic:
if __name__ == '__main__':    
    main()
