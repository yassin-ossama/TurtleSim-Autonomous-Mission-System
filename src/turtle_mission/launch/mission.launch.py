
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess



def generate_launch_description():
    ld = LaunchDescription()

    sim_node = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='sim',
        output='screen'
    )

    destination_server_node = Node(
        package='turtle_mission',
        executable='validate_server',
        name='destination_server',
        output='screen'
    )

    navigate_server_node = Node(
        package='turtle_mission',
        executable='action_server',
        name='navigate_server',
        output='screen'
    )

    # Run the client separately to enter x and y manually each time:
    # ros2 run turtle_mission destination_client

    ld.add_action(sim_node)
    ld.add_action(destination_server_node)
    ld.add_action(navigate_server_node)

    return ld
