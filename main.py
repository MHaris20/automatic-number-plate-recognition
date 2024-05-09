import cv2
import os
from datetime import datetime
from ultralytics import YOLO
import re
from ocr import Paddle
import csv

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

class CarPlateDetector:
    def __init__(self, image_folder, model_weights_path, class_list_path, csv_output_path, output_folder):
        self.image_folder = image_folder
        self.model = YOLO(model_weights_path)
        self.paddle = Paddle()
        self.csv_output_path = csv_output_path
        self.output_folder = output_folder
        
        # with open(class_list_path, "r") as f:
        #     self.class_list = f.read().split("\n")

        with open(csv_output_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['index', 'number_plate', 'time', 'date'])
            
    def contains_special_character(self, term):
        pattern = r'[^\w\s]'
        return re.search(pattern, term) is not None

    def detect_and_save_plates(self):
        image_files = [os.path.join(self.image_folder, f) for f in os.listdir(self.image_folder) if os.path.isfile(os.path.join(self.image_folder, f))]
        counter = 1
        for image_file in image_files:
            frame = cv2.imread(image_file)
            frame = cv2.resize(frame, (640, 640))
            results = self.model.predict(frame)
            a = results[0].boxes.data
            
            for index, row in enumerate(a):
                x1 = int(row[0])
                y1 = int(row[1])
                x2 = int(row[2])
                y2 = int(row[3])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                crop = frame[y1:y2, x1:x2]
                

                output_path = os.path.join(self.output_folder, f"cropped_{counter}.jpg")
                cv2.imwrite(output_path, crop)
                blurred_image = cv2.medianBlur(crop, 5)
                cv2.imwrite('blur.png', blurred_image)
                result = self.paddle.main(crop)
                if isinstance(result, list) and result:
                    if len(result) > 0 and isinstance(result[0], list) and len(result[0]) > 0:
                        terms = [item[1][0] for item in result[0] if isinstance(item, list) and len(item) > 1]
                        print("Terms:", terms)
                        filtered_terms = [term for term in terms if not self.contains_special_character(term)]
                        concatenated_terms = ' '.join(filtered_terms)
                        self.save_to_csv(concatenated_terms, counter)

                        
                    counter += 1

            cv2.imshow("RGB", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break  

    def save_to_csv(self, text, counter):

        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%Y-%m-%d")

        with open(self.csv_output_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([counter, text, current_time, current_date])

if __name__ == "__main__":
    detector = CarPlateDetector(
        image_folder='images', 
        model_weights_path='best.pt',
        class_list_path='data.txt',
        csv_output_path='output.csv',
        output_folder='cropped_images'
    )
    detector.detect_and_save_plates()

































































# import cv2
# import os
# from datetime import datetime
# from ultralytics import YOLO
# import re
# from ocr import Paddle
# import csv

# os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

# class CarPlateDetector:
#     def __init__(self, image_folder, model_weights_path, class_list_path, csv_output_path, output_folder):
#         self.image_folder = image_folder
#         self.model = YOLO(model_weights_path)
#         self.paddle = Paddle()
#         self.csv_output_path = csv_output_path
#         self.output_folder = output_folder
        
#         with open(class_list_path, "r") as f:
#             self.class_list = f.read().split("\n")

#         with open(csv_output_path, mode='w', newline='', encoding='utf-8') as file:
#             writer = csv.writer(file)
#             writer.writerow(['index', 'number_plate', 'time', 'date'])

#     def detect_and_save_plates(self):
#         image_files = [os.path.join(self.image_folder, f) for f in os.listdir(self.image_folder) if os.path.isfile(os.path.join(self.image_folder, f))]
#         counter = 1
#         for image_file in image_files:
#             frame = cv2.imread(image_file)
#             frame = cv2.resize(frame, (640, 640))
#             results = self.model.predict(frame)
#             a = results[0].boxes.data
            
#             for index, row in enumerate(a):
#                 x1 = int(row[0])
#                 y1 = int(row[1])
#                 x2 = int(row[2])
#                 y2 = int(row[3])
#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                 crop = frame[y1:y2, x1:x2]
                

#                 output_path = os.path.join(self.output_folder, f"cropped_{counter}.jpg")
#                 cv2.imwrite(output_path, crop)
#                 blurred_image = cv2.medianBlur(crop, 5)
#                 result = self.paddle.main(blurred_image)
#                 if isinstance(result, list) and result:
#                     if len(result) > 0 and isinstance(result[0], list) and len(result[0]) > 1 and isinstance(result[0][1], list) and len(result[0][1]) > 1:
#                         # input_str = result[0][1][1][0]
#                         input_str = result[0][1][1][0]
#                         self.save_to_csv(input_str, counter)
                        
#                         counter += 1

#             cv2.imshow("RGB", frame)
#             if cv2.waitKey(1) & 0xFF == 27:
#                 break  

#     def save_to_csv(self, text, counter):

#         current_time = datetime.now().strftime("%H:%M:%S")
#         current_date = datetime.now().strftime("%Y-%m-%d")

#         with open(self.csv_output_path, mode='a', newline='', encoding='utf-8') as file:
#             writer = csv.writer(file)
#             writer.writerow([counter, text, current_time, current_date])

# if __name__ == "__main__":
#     detector = CarPlateDetector(
#         image_folder='images', 
#         model_weights_path='best.pt',
#         class_list_path='data.txt',
#         csv_output_path='output.csv',
#         output_folder='cropped_images'
#     )
#     detector.detect_and_save_plates()
