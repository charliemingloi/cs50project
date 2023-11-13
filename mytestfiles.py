import cv2
import pytesseract

def image_to_text():
    # Load the image using OpenCV
    image_path = 'random.jpeg'
    image = cv2.imread(image_path)

    # Convert the image to grayscale for better OCR results
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply image preprocessing to enhance text
    processed_image = cv2.GaussianBlur(gray_image, (7, 7), 3)
    processed_image = cv2.threshold(processed_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Use Tesseract OCR to extract text
    text = pytesseract.image_to_string(processed_image, config='--psm 7')

    # Perform additional post-processing if needed
    newtext = ""
    count = 0
    for i in range(len(text)):
        if text[i].isalpha():
            newtext += text[i]
        elif count == 0 and text[i].isdigit():
            count += 1
            newtext += " "
            newtext += text[i]
        elif text[i].isdigit():
            count += 1
            newtext += text[i]

    return newtext

# Specify the path to your image


# Call the function and print the result

