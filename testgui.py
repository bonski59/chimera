import pygame
import os
import subprocess
import ctypes
pygame.init()

screen = pygame.display.set_mode([500, 500])

color_light = (170, 170, 170)

color_dark = (100, 100, 100)

smallfont = pygame.font.SysFont('Corbel', 35)
text1 = smallfont.render('Test GSM', True, (0,0,0))
text2 = smallfont.render('Send GSM text', True, (0,0,0))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 100 <= mouse[0] <= 300 and 100 <= mouse[1] <= 200:
                print("Test GSM")
                path = "C:\\Users\\falcon\\Documents\\OpenSSH\\ssh.exe pi@192.168.1.85 /bin/sh -c /home/pi/phonescripts/testgsm.sh"
                #conout = os.system(path).readlines()
                #ctypes.windll.user32.MessageBoxW(0, conout, "Output", 1)
                cmd = ['C:\\Users\\falcon\\Documents\\OpenSSH\\ssh.exe', 'pi@192.168.1.85', '/bin/sh', '-c', '/home/pi/phonescripts/testgsm.sh']
                conout = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
                #print(conout.decode("utf-8"))
                ctypes.windll.user32.MessageBoxW(0, conout.decode("utf-8"), "Output", 1)
                #ssh = paramiko.SSHClient()
                #ssh.connect("192.168.1.5", username="pi", password="!@#$QWER1234qwer")
                #os.chdir("C:\\Users\\falcon\\Documents\\OpenSSH\\")
                #subprocess.Popen("C:\\Windows\\System32\\OpenSSH\\ssh.exe pi@192.168.1.85 /bin/sh -c /home/pi/phonescripts/testgsm.sh")
            if 100 <= mouse[0] <= 300 and 250 <= mouse[1] <= 350:
                print("Send GSM text")
                cmd = ['C:\\Users\\falcon\\Documents\\OpenSSH\\ssh.exe', 'pi@192.168.1.85', '/bin/sh', '-c', '/home/pi/phonescripts/gsmmess.sh']
                conout = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
                # print(conout.decode("utf-8"))
                ctypes.windll.user32.MessageBoxW(0, conout.decode("utf-8"), "Output", 1)
    screen.fill((255, 255, 255))
    
    mouse = pygame.mouse.get_pos()
    
    #button 1 draw
    if 100 <= mouse[0] <= 300 and 100 <= mouse[1] <= 200:
        pygame.draw.rect(screen,color_light,[100,100,200,100])
    else:
        pygame.draw.rect(screen,color_dark,[100,100,200,100])
        
        
    #button 2 draw
    if 100 <= mouse[0] <= 300 and 250 <= mouse[1] <= 350:
        pygame.draw.rect(screen,color_light,[100,250,200,100])
    else:
        pygame.draw.rect(screen,color_dark,[100,250,200,100])
        
    screen.blit(text1, (140, 135))
    screen.blit(text2, (110, 285))
    pygame.display.flip()

pygame.quit()