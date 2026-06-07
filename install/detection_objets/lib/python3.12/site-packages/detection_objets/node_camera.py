from std_msgs.msg import String 

import rclpy
from rclpy.node import Node
import cv2
import numpy as np
from sensor_msgs.msg import CompressedImage

class CameraNode(Node):
    def __init__(self):
        super().__init__('camera_node') #nom nommer camera_node
        self.pub_couleur = self.create_publisher(String, 'couleur_detectee', 10)
        self.subscription = self.create_subscription(
            CompressedImage,
            'turtlecam/image_raw/compressed',
            self.image_callback,
            10
        )
        self.derniere_detection = ''
        self.dernier_affichage = self.get_clock().now()
        self.subscription  
         
    def image_callback(self, msg):
       # Vérifie si 2 secondes se sont écoulées
        maintenant = self.get_clock().now()
        duree = (maintenant - self.dernier_affichage).nanoseconds / 1e9
        if duree < 1.0:
           return
        self.dernier_affichage = maintenant
        np_arr = np.frombuffer(msg.data, np.uint8) #donc ca ca permet de rendre objet python
                                                    #contenu les octets en tableau numpy
        image_bgr = cv2.imdecode(np_arr, cv2.IMREAD_COLOR) #decodage de l'image a partir du tableau numpy 
                                                           #passe de octet a une image bgr chaque pixel est 
                                                           # representé par 3 octets (bleu, vert, rouge)
        #maintenant on convertie bgr en hsv parceque plus precis et plus simple 
        image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
        #definir les plages de couleurs pour le rouge et le bleu seulement fin ce qu'on a besoin pour projet 
        masque_rouge = cv2.bitwise_or(
          cv2.inRange(image_hsv, (0,   125, 80), (10,  255, 255)),  # rouge côté 0
          cv2.inRange(image_hsv, (170, 125, 100), (180, 255, 255))   
         ) 
        masque_bleu =cv2.inRange(image_hsv,(80,100,100), (130,255,255))
        #on doit maintenant afficher quel couleur est apparu dans l'image 
        pixels_rouges= cv2.countNonZero(masque_rouge)
        pixels_bleus = cv2.countNonZero(masque_bleu)
        if pixels_bleus > 3000:
            couleur = 'bleu'
        elif pixels_rouges > 3000:
            couleur = 'rouge'
        else:
            couleur = 'aucune'
        
        msg_couleur = String()
        msg_couleur.data = couleur
        self.pub_couleur.publish(msg_couleur)
def main(args=None):
    rclpy.init(args=args) #cette commande la permet de demarrer ROS2
    camera_node = CameraNode() 
    rclpy.spin(camera_node) #pour maintenir le noeud et qu'il dead pas 
    rclpy.shutdown() #quand tu fait ctrl+c c'est grace a cette fonctionne que le noeud s'arrete 
if __name__ == '__main__':
     main()