import cv2
from cv2.typing import Scalar


class ImageProcessor:
    def __init__(self, image_path: str):
        self.image_path = image_path
        self.image: cv2.typing.MatLike | None = None

    def read_image(self) -> None:
        try:
            self.image = cv2.imread(self.image_path, cv2.IMREAD_UNCHANGED)
            if self.image is None:
                raise FileNotFoundError(f"Image not found at path: {self.image_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to read image: {e}")

    def overlay_grid(
        self,
        interval: int = 50,
        bgr_color: Scalar = (0, 0, 255),  # BGR format
        enable_ticks: bool = True,
    ) -> None:
        if self.image is None:
            raise RuntimeError("Image not loaded. Call read_image() first.")
        height, width = self.image.shape[:2]
        for x in range(0, width, interval):
            cv2.line(self.image, (x, 0), (x, height), color=bgr_color, thickness=1)
        for y in range(0, height, interval):
            cv2.line(self.image, (0, y), (width, y), color=bgr_color, thickness=1)
        if enable_ticks:
            for x in range(0, width, interval):
                cv2.putText(
                    self.image,
                    str(x),
                    (x + 2, 15),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.4,
                    bgr_color,
                    1,
                )
            for y in range(0, height, interval):
                cv2.putText(
                    self.image,
                    str(y),
                    (2, y - 2),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.4,
                    bgr_color,
                    1,
                )

    def save_image(self, output_path: str) -> None:
        if self.image is None:
            raise RuntimeError("Image not loaded. Call read_image() first.")
        try:
            cv2.imwrite(output_path, self.image)
        except Exception as e:
            raise RuntimeError(f"Failed to save image: {e}")
