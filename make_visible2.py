import glob
import numpy as np
import czifile
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import os
from bs4 import BeautifulSoup

try:
	os.mkdir("png_images")
except:
	print("path already exists")

def normalize(image_input):
	for c in range(image.shape[3]):
		for t in range(image.shape[2]):
			frame = (image[0,0,t,c,:,:,:,0]).astype(int) #can still be a z stack
			max_val = np.max(frame)
			image_input[0,0,t,c,:,:,:,0] = ((1/max_val) * frame * 65536).astype(np.int16)
	return image_input

def normalize_8bit(image_input):
	for c in range(image.shape[3]):
		for t in range(image.shape[2]):
			frame = (image[0,0,t,c,:,:,:,0]).astype(int) #can still be a z stack
			max_val = np.max(frame)
			image_input[0,0,t,c,:,:,:,0] = ((1/max_val) * frame * 255).astype(np.int8)
	return image_input

#image = czifile.CziFile("Image 8.czi").asarray()
#print (image.shape) # shape: [?,?,c,t,z,x,y,?]

#image = normalize(image)
#plt.imshow(image[0,0,:,0,10,:,:,0].transpose((1,2,0)),interpolation='nearest')
#plt.show()

for file in glob.glob("*.czi"):
	print(file)
	infile = czifile.CziFile(file)
	image = infile.asarray()

	meta = BeautifulSoup(infile.metadata(), "xml")
	test = meta.find("Scaling")
	scalings = test.find_all("Value") #XYZ
	scale_x = float(scalings[0].text)
	scale_y = float(scalings[1].text)
	scale_z = float(scalings[2].text)

	scale_bar = 5e-6 #m
	scale_bar_px = scale_bar/scale_y

	font = ImageFont.truetype("helvetica.ttf", 20)

	if (image.shape[3] != 1) or (image.shape[4]) != 1:
		image = normalize_8bit(image)
	else:
		image = normalize(image)


	for c in range(image.shape[2]):

		if (image.shape[3] != 1) or (image.shape[4]) != 1:
			gif = []
			for t in range(image.shape[3]):
				for z in range(image.shape[4]):
					img = Image.fromarray(image[0,0,c,t,z,:,:,0])
					draw = ImageDraw.Draw(img)
					height = z*scale_z * 1e6
					text = "c: " + str(c) + " t: " + str(t) + " z: " + "{:.2f}".format(height) + " µm"
					draw.text((20, 20), text, font=font)
					draw.rectangle( [(image[0,0,c,t,z,:,:,0].shape[0]-20, image[0,0,c,t,z,:,:,0].shape[0]-20), (image[0,0,c,t,z,:,:,0].shape[0]-20-scale_bar_px, image[0,0,c,t,z,:,:,0].shape[0]-25)], fill ="white")
					draw.text((image[0,0,c,t,z,:,:,0].shape[0]-int(scale_bar_px*0.5)-50,image[0,0,c,t,z,:,:,0].shape[0]-50), "{:.0f}".format(scale_bar*1e6) + " µm", font=font)

					gif.append(img)

			name = os.path.basename(file)
			frame_one = gif[0]
			frame_one.save("png_images/" + name +"_c" +str(c)+ ".gif", format="GIF", append_images=gif, save_all=True, loop=1, duration=100)
		else:
			name = os.path.basename(file)
			img = Image.fromarray(image[0,0,c,0,0,:,:,0])
			draw = ImageDraw.Draw(img)
			draw.rectangle( [(image[0,0,c,0,0,:,:,0].shape[0]-20, image[0,0,c,0,0,:,:,0].shape[0]-20), (image[0,0,c,0,0,:,:,0].shape[0]-20-scale_bar_px, image[0,0,c,0,0,:,:,0].shape[0]-25)], fill ="white")

			draw.text((image[0,0,c,0,0,:,:,0].shape[0]-int(scale_bar_px*0.5)-50,image[0,0,c,0,0,:,:,0].shape[0]-50), "{:.0f}".format(scale_bar*1e6) + " µm", font=font)

			img.save("png_images/" + name +"_c" +str(c)+ ".png")
