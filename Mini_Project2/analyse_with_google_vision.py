import io
import os
import glob
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
def analyze_images(path):
	client = vision.ImageAnnotatorClient()
	# The name of the image file to annotate
	WSI_MASK_PATH="path"
	wsi_mask_paths = glob.glob(os.path.join(WSI_MASK_PATH, '*.jpg'))
	wsi_mask_paths.sort()
	for image in wsi_mask_paths:
		file_name = os.path.join(
	    	os.path.dirname(__file__),
	    	image)
	# Loads the image into memory
		with io.open(file_name, 'rb') as image_file:
		    content = image_file.read()
		image = types.Image(content=content)
		# Performs label detection on the image file
		response = client.label_detection(image=image)
		labels = response.label_annotations
		print('Labels for'+file_name+':')
		for label in labels:
		    print(label.description)
analyze_images('testcase')

