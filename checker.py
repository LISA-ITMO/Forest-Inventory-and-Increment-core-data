from pycocotools.coco import COCO
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np


class CocoImageViewer:
    """
    Класс для визуализации изображений и аннотаций из COCO-формата

    Атрибуты:
        coco (COCO): Экземпляр COCO с загруженными аннотациями
    """

    def __init__(self, annotation_file: str):
        """
        Инициализация класса CocoImageViewer

        Args:
            annotation_file (str): Путь к JSON-файлу аннотаций COCO
        """
        self.coco = COCO(annotation_file)

    def visualize_image(self, img_id: int) -> None:
        """
        Отображение одного изображения с аннотациями

        Args:
            img_id (int): ID изображения в COCO
        """
        image_info = self.coco.loadImgs(img_id)[0]
        image_path = image_info["file_name"]

        image = plt.imread(image_path)

        plt.figure(figsize=(8, 6))
        plt.imshow(image)
        plt.axis("off")

        ann_ids = self.coco.getAnnIds(imgIds=img_id)
        annotations = self.coco.loadAnns(ann_ids)

        for ann in annotations:
            segmentation = ann["segmentation"][0]
            poly = Polygon(
                np.array(segmentation).reshape(-1, 2),
                edgecolor="r",
                fill=False,
                linewidth=2
            )
            plt.gca().add_patch(poly)

        print("Press close image window to see next image")
        plt.show()

    def visualize_all_images(self) -> None:
        """
        Отображение изображений с аннотациями из COCO
        """
        image_ids = self.coco.getImgIds()
        print(f"{len(image_ids)} images")

        for img_id in image_ids:
            self.visualize_image(img_id)


if __name__ == "__main__":
    viewer = CocoImageViewer("result.json")
    viewer.visualize_all_images()