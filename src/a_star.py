from utils.image_manipulator import Image_Manipulator

class A_Star:
    def __init__(self, image: Image_Manipulator):
        self.open_list = []
        self.closed_list = []
        self.image = image
        
a_star = A_Star(image)


