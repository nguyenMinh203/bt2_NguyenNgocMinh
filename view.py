from PyQt6.QtWidgets import QLabel, QGridLayout, QWidget
from PyQt6.QtGui import QPixmap, QImage
import cv2

class ImageDisplayView(QWidget):
    def __init__(self):
        super().__init__()

        # Tạo layout dạng lưới
        self.layout = QGridLayout()

        # Mảng chứa các QLabel để hiển thị ảnh gốc và các kết quả xử lý của từng ảnh
        self.image_labels = []

        # Khởi tạo QLabel cho mỗi ảnh (ảnh gốc, Sobel, LoG)
        for i in range(3):  # 3 ảnh khác nhau
            original_label = QLabel(self)
            sobel_label = QLabel(self)
            log_label = QLabel(self)

            # Thêm các QLabel vào mảng
            self.image_labels.append({
                'original': original_label,
                'sobel': sobel_label,
                'log': log_label
            })

            # Thêm các QLabel vào layout dạng lưới
            row = i * 2  # Mỗi ảnh chiếm 2 hàng
            self.layout.addWidget(original_label, row, 0)  # Ảnh gốc ở cột đầu tiên
            self.layout.addWidget(sobel_label, row, 1)     # Kết quả Sobel ở cột thứ hai
            self.layout.addWidget(log_label, row, 2)       # Kết quả LoG ở cột thứ ba

        # Cài đặt layout
        self.setLayout(self.layout)
        self.setWindowTitle('Hiển thị 3 ảnh gốc và kết quả xử lý')

    def resize_image(self, image, max_width=300, max_height=300):
        """Thay đổi kích thước ảnh để phù hợp với màn hình (tối đa 300x300 pixels)"""
        height, width = image.shape[:2]

        # Tính toán tỷ lệ thu nhỏ ảnh
        scaling_factor = min(max_width / width, max_height / height)

        # Thực hiện thay đổi kích thước ảnh theo tỷ lệ tính được
        new_width = int(width * scaling_factor)
        new_height = int(height * scaling_factor)
        resized_image = cv2.resize(image, (new_width, new_height))

        return resized_image

    def display_image(self, label, image):
        """Hiển thị ảnh lên QLabel sau khi thay đổi kích thước"""
        resized_image = self.resize_image(image)
        height, width = resized_image.shape
        bytes_per_line = width
        q_img = QImage(resized_image.data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)
        pixmap = QPixmap.fromImage(q_img)
        label.setPixmap(pixmap)

    def display_processed_images(self, images):
        """
        Hiển thị tất cả các ảnh gốc và các kết quả xử lý Sobel và LoG trên giao diện.
        `images` là danh sách chứa các từ điển với các khóa: 'original', 'sobel', 'log'.
        """
        for i, image_dict in enumerate(images):
            self.display_image(self.image_labels[i]['original'], image_dict['original'])
            self.display_image(self.image_labels[i]['sobel'], image_dict['sobel'])
            self.display_image(self.image_labels[i]['log'], image_dict['log'])
