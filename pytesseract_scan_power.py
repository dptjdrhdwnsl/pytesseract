import pytesseract
import cv2
import matplotlib.pyplot as plt
import os
from PIL import Image
import re
import natsort

directory = "e:/1468/20230714"

# Retrieve the list of files in the directory, order by 가 안되고 그냥 읽어옴
files = os.listdir(directory)

# Filter out only image files based on extensions
image_files = [file for file in files if re.search(r"\.(jpg|jpeg|png)$", file, re.IGNORECASE)]

# Sort the image files using natural sort algorithm
image_files = natsort.natsorted(image_files)

# Tesseract 옵션 설정
custom_config = r'--oem 3 --psm 6 --tessdata-dir "C:/Program Files/Tesseract-OCR/tessdata"'
# 이미지에서 필요한 부분 좌표 설정
x = 1010  # 왼쪽 상단 x 좌표
y = 170  # 왼쪽 상단 y 좌표
width = 115  # 자를 부분의 너비
height = 455  # 자를 부분의 높이

total_sum = 0  # Initialize the total sum

previous_numbers = None

for i in range(len(image_files)):
    image_file = image_files[i]

    # Create the full file path
    img_path = os.path.join(directory, image_file)

    # Read the image
    img = cv2.imread(img_path)

    if img is not None:
        print(f"Processing image: {image_file}")

        # 이미지에서 필요한 부분 자르기
        crop_image = img[y:y + height, x:x + width]

        # Convert the image to PIL format
        pil_image = Image.fromarray(crop_image)

        # Apply OCR and extract numbers
        result = pytesseract.image_to_string(pil_image, config=custom_config)

        # Extract numbers using regular expression
        numbers = re.findall(r'\d{1,3}(?:,\d{3})*', result)

        # Remove commas from the extracted numbers and convert them to integers
        numbers = [int(num.replace(',', '')) for num in numbers]

        if previous_numbers is not None:
            unique_numbers = [num for num in numbers if num not in previous_numbers]
            iteration_sum = sum(unique_numbers)

            print(f"Image File Prev: {image_files[i - 1]}")
            print(f"Numbers Prev: {previous_numbers}")
            print(f"Image File Curr: {image_file}")
            print(f"Numbers Curr: {numbers}")
            print(f"Unique Numbers: {unique_numbers}")
            print(f"Sum: {iteration_sum}")
            print()

            total_sum += iteration_sum

        previous_numbers = numbers

        if i == 0:
            total_sum += sum(numbers)  # Include the sum of numbers from the first image

    else:
        print(f"Error reading image: {image_file}")

print(f"Total Sum: {total_sum}")
