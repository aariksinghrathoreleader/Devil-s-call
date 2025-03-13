import cv2
import numpy as np

class ImageProcessor:
    def __init__(self):
        self.kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])

    def process_image(self, image_path):
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if image is None:
            raise ValueError("Could not read the image file.")

        image = cv2.resize(image, (300, 300))
        sharpened = cv2.filter2D(image, -1, self.kernel)

        edges = cv2.Canny(sharpened, 50, 150)
        return sharpened, edges

    def save_processed_images(self, sharpened, edges, output_path):
        cv2.imwrite(f"{output_path}_sharpened.jpg", sharpened)
        cv2.imwrite(f"{output_path}_edges.jpg", edges)

if __name__ == "__main__":
    processor = ImageProcessor()
    sharp, edge = processor.process_image("input.jpg")
    processor.save_processed_images(sharp, edge, "output")
    cv2.imshow("Sharpened Image", sharp)
    cv2.imshow("Edge Detection", edge)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
