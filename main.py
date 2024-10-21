import sys
from PyQt6.QtWidgets import QApplication
from model import ImageProcessorModel
from view import ImageDisplayView
from controller import ImageProcessorController

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Danh sách tên ảnh cần xử lý
    images = ['ngoctrinh.jpg', 'phongcanh.jpg', 'yte.jpg']
    models = []

    # Khởi tạo các mô hình xử lý cho từng ảnh
    for image in images:
        try:
            model = ImageProcessorModel(image)
            models.append(model)
        except FileNotFoundError as e:
            print(e)

    # Khởi tạo view và controller
    view = ImageDisplayView()
    controller = ImageProcessorController(models, view)

    # Xử lý và hiển thị ảnh
    controller.process_and_display_images()
    view.show()

    sys.exit(app.exec())
