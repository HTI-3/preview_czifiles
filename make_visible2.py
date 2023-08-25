import glob
import numpy as np
import czifile
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import os

try:
	os.mkdir("png_images")
except:
	print("path already exists")

def normalize(image_input):
	for c in range(image.shape[3]):
		for t in range(image.shape[2]):
			frame = (image[0,0,t,c,:,:,:,0]).astype(int) #can still be a z stack
			max_val = np.max(frame)
			image_input[0,0,t,c,:,:,:,0] = ((1/max_val) * frame * 65535).astype(np.uint16)
	return image_input

def normalize_8bit(image_input):
	for c in range(image.shape[3]):
		for t in range(image.shape[2]):
			frame = (image[0,0,t,c,:,:,:,0]).astype(int) #can still be a z stack
			max_val = np.max(frame)
			image_input[0,0,t,c,:,:,:,0] = ((1/max_val) * frame * 254).astype(np.uint8)
	return image_input

#image = czifile.CziFile("Image 8.czi").asarray()
#print (image.shape) # shape: [?,?,c,t,z,x,y,?]

#image = normalize(image)
#plt.imshow(image[0,0,:,0,10,:,:,0].transpose((1,2,0)),interpolation='nearest')
#plt.show()

for file in glob.glob("*.czi"):
	print(file)
	image = czifile.CziFile(file).asarray()
	if (image.shape[3] != 1) or (image.shape[4]) != 1:
		image = normalize_8bit(image)
	else:
		image = normalize(image)


	for c in range(image.shape[2]):

		if (image.shape[3] != 1) or (image.shape[4]) != 1:
			font = ImageFont.truetype("helvetica.ttf", 20) # has to include whole path!
			gif = []
			for t in range(image.shape[3]):
				for z in range(image.shape[4]):
					img = Image.fromarray(image[0,0,c,t,z,:,:,0])
					draw = ImageDraw.Draw(img)
					text = "c: " + str(c) + " t: " + str(t) + " z: " + str(z)
					draw.text((20, 20), text, font=font)
					gif.append(img)

			name = os.path.basename(file)
			frame_one = gif[0]
			frame_one.save("png_images/" + name +"_c" +str(c)+ ".gif", format="GIF", append_images=gif, save_all=True, loop=1, duration=100)
		else:
			name = os.path.basename(file)
			img = Image.fromarray(image[0,0,c,0,0,:,:,0])
			img.save("png_images/" + name +"_c" +str(c)+ ".png")
