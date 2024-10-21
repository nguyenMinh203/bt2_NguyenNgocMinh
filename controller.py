class ImageProcessorController:
    def __init__(self, models, view):
        self.models = models  # models là một danh sách chứa các mô hình cho từng ảnh
        self.view = view

    def process_and_display_images(self):
        """Thực hiện các thao tác dò biên và hiển thị"""
        processed_images = []

        # Duyệt qua từng model để xử lý ảnh
        for model in self.models:
            image_data = {
                'original': model.image,
                'sobel': model.sobel_edge_detection(),
                'log': model.log_edge_detection(),
            }
            processed_images.append(image_data)

        # Hiển thị tất cả các ảnh đã xử lý trên giao diện
        self.view.display_processed_images(processed_images)
