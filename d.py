import pyautogui

a = int(input("Enter a number :"))
for i in range (0,5):
    screenshot = pyautogui.screenshot()
    screenshot.save('screenshot'+str(i)+'.png')
    print('success')
