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
