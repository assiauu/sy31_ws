import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String 


class Detector(Node):
    def __init__(self):
        super().__init__("detector")

        self.bridge = CvBridge()
        self.pub = self.create_publisher(Image, "detections", 10)
        self.couleur_detectee = ""

        # TODO: Determine min and max pixel values
        
        # ...
        self.create_subscription(String, "couleur_detectee", self.couleur_callback, 10)
        self.sub = self.create_subscription(Image, "turtlecam/image_raw", self.callback, 10)

    def callback(self, msg: Image):
        """Process the images going on image_rect"""

        # Convert ROS -> OpenCV
        try:
            img = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError as e:
            self.get_logger().warn(f"ROS->OpenCV {e}")
            return
        

        
        hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        masque_rouge = cv2.bitwise_or(
          cv2.inRange(hsv, (0,   100, 80), (10,  255, 255)),  # rouge côté 0
          cv2.inRange(hsv, (170, 100, 100), (180, 255, 255))   
         ) 
        masque_bleu =cv2.inRange(hsv,(80,100,100), (130,255,255))
        pixels_rouges= cv2.countNonZero(masque_rouge)
        pixels_bleus = cv2.countNonZero(masque_bleu)
        if pixels_bleus > 6000:
           img_out=self.detect(img,masque_bleu,hsv)
        elif pixels_rouges > 6000:
            img_out = self.detect(img,masque_rouge,hsv)
        else :
            img_out=img
        
        # Convert OpenCV -> ROS
        try:
            format = "bgr8" if img_out.ndim == 3 else "mono8"
            msg_out = self.bridge.cv2_to_imgmsg(img_out, format)
        except CvBridgeError as e:
            self.get_logger().warn(f"ROS->OpenCV {e}")
            return

        self.pub.publish(msg_out)

    def couleur_callback(self, msg: String):
        self.couleur_detectee = msg.data 

    def detect(self, img, mask, couleur):
       
        # Morphologie pour couper les connexions fines (doigts)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  kernel, iterations=7)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=7)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return img

        cnt = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(cnt)
        if area <= 500:
            return img

        perimeter = cv2.arcLength(cnt, True)
        if perimeter == 0:
            return img

        circularity = 4 * np.pi * area / (perimeter ** 2)

        if circularity > 0.80 and area > 3000:
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            cv2.circle(img, (int(x), int(y)), int(radius), (0, 255, 0), 2)
            forme= "cercle"
        else:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            forme= "rectangle"
            
        cv2.putText(img, forme, (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
        cv2.putText(img, self.couleur_detectee, (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
        return img

    '''def detect(self, img: np.ndarray,mask,hsv) -> np.ndarray:
        # TODO: Filter pixels based on their value
        contours,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        #img=cv2.drawContours(img,contours,-1,(0,0,255),3)
        if contours:
            biggest=max(contours,key=cv2.contourArea)
            if cv2.contourArea(biggest) >500:
                img=cv2.drawContours(img,[biggest],-1,(255,0,0),3)
        return img'''


def main(args=None):
    import rclpy

    rclpy.init(args=args)
    node = Detector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()