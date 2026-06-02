#SY31 - Détection d'objets
## Description
Projet ROS2 de détection d'objets avec un TurtleBot3.
Le robot utilise sa caméra et son LiDAR pour identifier 
différents objets (cartons rouges, bleus, panneaux...).

## Prérequis
- ROS2 Jazzy
- Python 3
- OpenCV : `pip install opencv-python`
- NumPy : `pip install numpy`

## Structure du projet
sy31_ws/
├── src/
│   └── detection_objets/
│       └── detection_objets/
│           └── node_camera.py   # noeud détection couleur
├── bags/                        # fichiers bag pour les tests
└── README.md

## Lancer le projet

### 1. Builder le workspace
```bash
cd ~/sy31_ws
colcon build
echo "source ~/sy31_ws/install/setup.bash >> ~/bashrc"
source ~/.bashrc
```

### 2. Lancer le bag
```bash
ros2 bag play ~/sy31_ws/bags/objets/ --loop 
```

### 3. Lancer le noeud caméra
```bash
ros2 run detection_objets camera_node
```

## Auteurs
