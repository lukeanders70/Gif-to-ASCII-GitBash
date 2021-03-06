from PIL import Image, ImageFilter, ImageEnhance
import time
import sys


#list of allowed characters and their associated 'lightness' values. Since this is printed in 
#GitBash with white on black text, characters that are larger and more complex, will appear lighter
#when viewed in the context of a full image. These values were generated by analyzing a screenshot 
#of chars printed on GitBash, along with human tweaking for better results
lightnessList = [(10, ' '), (25, ':'), (42, ';'), (46, '|'), (48, '+'), (51, '='), 
(52, 'i'), (55, '?'),  (57, 'J'), (60, '('), (62, 's'), (65, 'I'), (66, '['), 
(67, '5'), (70, 'X'), (73, 'E'), (77, 'H'), (80, '$'),  (83, '0'), (85, '#'), 
(89, '@'), (98, '&'), (100, '&')]

#take a single rgb image and print it in ASCII to GitBash
def makePic(rgb_im):
	#iterate through x and y
	for y in range(rgb_im.size[1]):
		for x in range(rgb_im.size[0]):

			#git the r, g, b values of the current pixel, add them up to get lightness, convert to a percent.
			a, b, c = rgb_im.getpixel((x,y))
			raw = (a+b+c)/3
			percent = int((raw/255) * 100)

			#find out what indices in lightnessList this pixel's value is between 
			n = 0
			while lightnessList[n][0] < percent:
				n += 1

			#if we're on the last character of a printed line, we have to create a linebreak after printing
			if x == rgb_im.size[0] - 1:

				#easier to hardcode this one in
				if n == 0:
					print (' ')
				#between the two lindecies of linghtnessList that this pixel is between, print the val of the cloaser one
				elif lightnessList[n][0] == percent or (lightnessList[n][0] - percent) < (percent - lightnessList[n-1][0]):
					print(lightnessList[n][1])

				else:
					print (lightnessList[n-1][1])

			#if we aren't at the end of a line, we want to not print a linebreak. The 'end' just means what to end the print
			#statment whih. By default it's a new line char, which we don't want in this case
			else:
				#easier to hardcode this one in
				if n == 0:
					print (' ', end="")

				#between the two lindecies of linghtnessList that this pixel is between, print the val of the cloaser one
				elif lightnessList[n][0] == percent or (lightnessList[n][0] - percent) < (percent - lightnessList[n-1][0]):
					print(lightnessList[n][1], end="")

				else:
					print (lightnessList[n-1][1], end="")

#startup text 
print("************* ASCII Gif for GitBash *************")
print("")
print("Make sure you're window is large enough for your input")
print("use 'ctr +' to zoom in and 'ctr -' to zoom out")
print("")
print("")

#user imput
im_string = input("gif or image to load:")
height_string = input("desired character height of image or gif (width we be calculated):")


im = Image.open(im_string) # open Image
y = int(height_string)
x = im.size[0]*(y / im.size[1]) #get the width of the image based on the inputed character height
x = int(x * 1.65) #GitBash chars are taller than they are wide, so this scaling factor stops distortion of final image 

#if the image is a .gif, we will iterate over the panels indefinitally 
if im.tile[0][0] == "gif":
	while 1:

		rgb_im = im.convert('RGB') #convert the frame to a form that can be divided into rgb values 
		rgb_im = rgb_im.resize((x, y)) #resize by our user input and calculated dimensions

		#convert the picture to ASCII and print it 
		makePic(rgb_im)

		#for every line printed (height), we use this GitBash command to retroacticly delete the line. allowing us to use 
		#the same space to put the next frame (we dont want to scroll down)
		for _ in range(rgb_im.size[1]):
 			sys.stdout.write("\033[F")

 		#either get the next frame or, if the gif is done, return to the start
		try:
			im.seek(im.tell()+1)
		except EOFError:
			im.seek(0)

		#a short timer to make the gifs move at a reasonable speed
		time.sleep(.05)

#run if this is not a .gif (so if it's a .png)
else:
		#some enhancments since time complexity is less of an issue with static images than gifs
		enhancer = ImageEnhance.Contrast(im) # make an object to change contrast
		im = enhancer.enhance( 2.0 ) # amp  up the contrast for better results 

		rgb_im = im.convert('RGB')
		rgb_im = rgb_im.resize((x, y))

		makePic(rgb_im)



