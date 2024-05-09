from paddleocr import PaddleOCR


class Paddle:
    def __init__(self) -> None:
        pass
    
    def main(self,cropped_image):
        ocr_instance = PaddleOCR(lang='en', use_gpu=True)
        cropped = cropped_image 
        print("Number plate", ":")
        try:
            result = ocr_instance.ocr(cropped)
            print(result)
        except TypeError as e:
            print("No text detected.")
        
        return result
