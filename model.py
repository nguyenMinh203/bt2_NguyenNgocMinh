import cv2
import numpy as np
import os

class ImageProcessorModel:
    def __init__(self, image_name):
        # Sử dụng đường dẫn đầy đủ tới folder "D:/taive"
        image_path = os.path.join("D:/taive", image_name)
        self.image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # Kiểm tra nếu ảnh không được đọc thành công
        if self.image is None:
            raise FileNotFoundError(f"Không thể đọc ảnh từ {image_path}")

    def negative_image(self):
        return 255 - self.image

    def contrast_image(self):
        alpha = 2.0  # hệ số tăng độ tương phản
        return cv2.convertScaleAbs(self.image, alpha=alpha, beta=0)

    def log_transform(self):
        # Chuẩn hóa giá trị pixel vào khoảng [0, 1] để tránh overflow
        normalized_image = self.image / 255.0
        epsilon = 1e-5  # giá trị nhỏ để tránh log(0)
        log_image = np.log(1 + normalized_image + epsilon)
        log_image = log_image * (255 / np.log(1 + 1 + epsilon))  # Tính toán lại thang giá trị
        return np.clip(np.array(log_image * 255, dtype=np.uint8), 0, 255)

    def equalize_histogram(self):
        return cv2.equalizeHist(self.image)

    def sobel_edge_detection(self):
        # Tính toán gradient theo hướng x và y bằng toán tử Sobel
        sobelx = cv2.Sobel(self.image, cv2.CV_64F, 1, 0, ksize=3)  # Theo hướng x
        sobely = cv2.Sobel(self.image, cv2.CV_64F, 0, 1, ksize=3)  # Theo hướng y

        # Tổng hợp gradient từ cả hai hướng
        sobel_combined = np.sqrt(sobelx ** 2 + sobely ** 2)

        # Chuẩn hóa kết quả về khoảng [0, 255] để hiển thị rõ hơn
        sobel_combined = cv2.normalize(sobel_combined, None, 0, 255, cv2.NORM_MINMAX)

        # Trả về kết quả dưới dạng uint8
        return np.uint8(sobel_combined)

    def log_edge_detection(self):
        # Làm mượt ảnh với bộ lọc Gaussian trước khi sử dụng toán tử Laplacian
        blurred = cv2.GaussianBlur(self.image, (3, 3), 0)

        # Sử dụng toán tử Laplacian để tính toán gradient thứ hai
        log = cv2.Laplacian(blurred, cv2.CV_64F)

        # Chuẩn hóa kết quả về khoảng [0, 255] để hiển thị rõ hơn
        log = np.absolute(log)
        log = cv2.normalize(log, None, 0, 255, cv2.NORM_MINMAX)

        # Trả về kết quả dưới dạng uint8
        return np.uint8(log)
