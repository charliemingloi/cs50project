import cv2
import pytesseract

# Load the image using OpenCV
image_path = 'random.jpeg'
image = cv2.imread(image_path)

cv2.imshow('Image',image)

# Convert the image to grayscale for better OCR results
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow('Gray',gray_image)
# Apply image preprocessing (e.g., thresholding, blurring) to enhance text
processed_image = cv2.GaussianBlur(gray_image, (7, 7), 3)
cv2.imshow('Gaussion', processed_image)
processed_image = cv2.threshold(processed_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
text = pytesseract.image_to_string(processed_image,config='--psm 6')
print(text)
cv2.imshow('Images', processed_image)
cv2.imwrite('newimg.png', processed_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

#https://stackoverflow.com/questions/44619077/pytesseract-ocr-multiple-config-options ,