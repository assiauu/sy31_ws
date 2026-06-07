from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([

        Node(
            package='detection_objets',
            executable='camera_node',
            output='screen'
        ),

        # Commande exacte qui fonctionne
        ExecuteProcess(
            cmd=[
                'ros2', 'run', 'image_transport', 'republish', 'compressed',
                '--ros-args',
                '-p', 'in_transport:=compressed',
                '-p', 'out_transport:=raw',
                '-r', 'in/compressed:=/turtlecam/image_raw/compressed',
                '-r', 'out:=/turtlecam/image_raw',
            ],
            output='screen'
        ),

        Node(
            package='detection_objets',
            executable='detector',
            output='screen',
        ),
        Node (
          package='detection_objets',
          executable='clusterer',
          output='screen',  
        ),
        Node (
          package='detection_objets',
          executable='intensity_filter',
          output='screen',  
        ),
        Node (
          package='detection_objets',
          executable='transformer',
          output='screen',  
        ),
         Node (
            package='detection_objets',
            executable='clusterer1',
            output='screen',
        ),


    ])