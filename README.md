
# Auto Cropping Script (CSV)
## Description
This project provides a script to process a CSV file containing image annotations and crop images based on the bounding box (bbox) information. The cropped images are then saved in a structured directory hierarchy based on the class name.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation
Install [PyCharm Community Edition](https://www.jetbrains.com/pycharm/download/?section=windows)

1. Create a new project:

![Screenshot (5)](https://github.com/user-attachments/assets/505ebcc0-a23f-41de-8e75-bd82759452ce)


2. Open settings and select "Python Intepreter" under your project. Click on the plus sign and search for "opencv-python" to install the OpenCV package:

![Screenshot (2)](https://github.com/user-attachments/assets/1bc46e42-2b96-404d-8a32-f3347c3db87d)
![Screenshot (6)](https://github.com/user-attachments/assets/a913794f-e252-47f4-84ee-5599aa880fb0)
![Screenshot (7)](https://github.com/user-attachments/assets/18c56eba-8351-470a-b263-fdf4a6077608)

3. Create a new Python file:

![Screenshot (4)](https://github.com/user-attachments/assets/7344ef74-ca51-4d8e-be36-91933edf2906)

## Usage
To use the script, you need to provide the path to the CSV file, the folder containing images, and the output folder where the cropped images will be saved.

    1. Update the csv_file_path, image_folder_path, and output_folder_path variables in the script with the appropriate paths.
    2. Run the script:

### Example
Here is an example of how to use the script:

    import os
    import cv2


    def crop_bbox(image_path, bbox):
        try:
            image = cv2.imread(image_path)
            if image is None:
                print(f"Error reading image: {image_path}")
                return None
            x1, y1, x2, y2 = bbox
            if x1 >= x2 or y1 >= y2:
                print(f"Invalid bbox coordinates for image {image_path}: {bbox}")
                return None
            cropped_image = image[int(y1):int(y2), int(x1):int(x2)]
            return cropped_image
        except Exception as e:
            print(f"Error cropping image {image_path}: {str(e)}")
            return None


    def process_csv_file(csv_file_path, image_folder_path, output_folder_path):
        class_counters = {}
        with open(csv_file_path, 'r') as csv_file:
            next(csv_file)  # Skip the header line
            for csv_line in csv_file:
                parts = csv_line.strip().split(',')
                image_filename = parts[0]
                image_path = os.path.join(image_folder_path, image_filename)
                if not os.path.exists(image_path) or not os.path.isfile(image_path):
                    print(f"Image file not found or not a file: {image_path}")
                    continue
                if len(parts) >= 8:
                    bbox = tuple(map(float, parts[2:6]))
                else:
                    print(f"Invalid annotation for image {image_path}: {csv_line}")
                    continue
                class_name = parts[1]  # Use parts[1] instead of parts[3]
                class_folder = os.path.join(output_folder_path, class_name)
                if not os.path.exists(class_folder):
                    os.makedirs(class_folder)
                if class_name not in class_counters:
                    class_counters[class_name] = 0
                bbox_int = (int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]))
                cropped_image = crop_bbox(image_path, bbox_int)
                if cropped_image is not None:
                    output_image_path = os.path.join(class_folder, f"{class_counters[class_name] + 1}.{image_filename.rsplit('.', 1)[1]}")
                    if cv2.imwrite(output_image_path, cropped_image):
                        print(f"Image saved successfully: {output_image_path}")
                    class_counters[class_name] += 1  # Increment counter for the class


    # Example usage
    csv_file_path = "/path/to/your/csv/file"
    image_folder_path = "/path/to/your/image/folder"
    output_folder_path = "/path/to/your/output/folder"
    process_csv_file(csv_file_path, image_folder_path, output_folder_path)

## License
This project is licensed under the [MIT License](https://www.mit.edu/~amini/LICENSE.md).



