import pyrfuniverse.attributes as attr
from pyrfuniverse.side_channel.side_channel import (
    IncomingMessage,
    OutgoingMessage,
)
import pyrfuniverse.utils.rfuniverse_utility as utility


def parse_message(msg: IncomingMessage) -> dict:
    this_object_data = attr.base_attr.parse_message(msg)
    this_object_data['number_of_joints'] = msg.read_int32()
    # Position
    this_object_data['positions'] = _parse_raw_list_3(msg.read_float32_list())
    # RotationEuler
    this_object_data['rotations'] = _parse_raw_list_3(msg.read_float32_list())
    # RotationQuaternion
    this_object_data['quaternion'] = _parse_raw_list_4(msg.read_float32_list())
    # Velocity
    this_object_data['velocities'] = _parse_raw_list_3(msg.read_float32_list())
    # Each joint position
    this_object_data['joint_positions'] = msg.read_float32_list()
    # Each joint velocity
    this_object_data['joint_velocities'] = msg.read_float32_list()
    # Whether all parts are stable
    this_object_data['all_stable'] = msg.read_bool()
    this_object_data['move_done'] = msg.read_bool()
    this_object_data['rotate_done'] = msg.read_bool()
    if msg.read_bool() is True:
        this_object_data['gravity_forces'] = msg.read_float32_list()
        this_object_data['coriolis_centrifugal_forces'] = msg.read_float32_list()
        this_object_data['drive_forces'] = msg.read_float32_list()
    return this_object_data


def _parse_raw_list_3(raw_list):
    length = len(raw_list)
    assert length % 3 == 0
    number_of_parts = length // 3
    norm_list = []
    for j in range(number_of_parts):
        transform = [raw_list[3 * j], raw_list[3 * j + 1], raw_list[3 * j + 2]]
        norm_list.append(transform)

    return norm_list


def _parse_raw_list_4(raw_list):
    length = len(raw_list)
    assert length % 4 == 0
    number_of_parts = length // 4
    norm_list = []
    for j in range(number_of_parts):
        transform = [raw_list[4 * j], raw_list[4 * j + 1], raw_list[4 * j + 2], raw_list[4 * j + 3]]
        norm_list.append(transform)

    return norm_list


def SetJointPosition(kwargs: dict) -> OutgoingMessage:
    """Set the target positions for each joint in a specified articulation body.
    Args:
        Compulsory:
        index: The index of articulation body, specified in returned message.
        joint_positions: A list inferring each joint's position in the specified acticulation body.

        Optional:
        speed_scales: A list inferring each joint's speed scale. The length must be the same with joint_positions.
    """
    compulsory_params = ['id', 'joint_positions']
    optional_params = ['speed_scales']
    utility.CheckKwargs(kwargs, compulsory_params)

    msg = OutgoingMessage()
    joint_positions = kwargs['joint_positions']
    num_joints = len(joint_positions)

    msg.write_int32(kwargs['id'])
    msg.write_string('SetJointPosition')
    msg.write_int32(num_joints)
    msg.write_float32_list(kwargs['joint_positions'])
    if 'speed_scales' in kwargs.keys():
        assert num_joints == len(kwargs['speed_scales']), \
            'The length of joint_positions and speed_scales are not equal.'
        msg.write_float32_list(kwargs['speed_scales'])
    else:
        msg.write_float32_list([1.0 for i in range(num_joints)])

    return msg


def SetJointPositionDirectly(kwargs: dict) -> OutgoingMessage:
    """Set the target positions for each joint in a specified articulation body. Note that this function will move
       all joints directrly to its target joint position, and ignoring the physical effects during moving.
    Args:
        Compulsory:
        index: The index of articulation body, specified in returned message.
        joint_positions: A list inferring each joint's position in the specified acticulation body.
    """
    compulsory_params = ['id', 'joint_positions']
    optional_params = []
    utility.CheckKwargs(kwargs, compulsory_params)

    msg = OutgoingMessage()
    joint_positions = kwargs['joint_positions']
    num_joints = len(joint_positions)

    msg.write_int32(kwargs['id'])
    msg.write_string('SetJointPositionDirectly')
    msg.write_int32(num_joints)
    msg.write_float32_list(kwargs['joint_positions'])

    return msg


def SetJointPositionContinue(kwargs: dict) -> OutgoingMessage:
    compulsory_params = ['id', 'interval', 'time_joint_positions']
    optional_params = []
    utility.CheckKwargs(kwargs, compulsory_params)

    msg = OutgoingMessage()

    time_joint_positions = kwargs['time_joint_positions']
    num_times = len(time_joint_positions)
    num_joints = len(time_joint_positions[0])
    interval = kwargs['interval']

    msg.write_int32(kwargs['id'])
    msg.write_string('SetJointPositionContinue')
    msg.write_int32(num_times)
    msg.write_int32(num_joints)
    msg.write_int32(interval)
    for i in range(num_times):
        msg.write_float32_list(time_joint_positions[i])

    return msg


def SetJointVelocity(kwargs: dict) -> OutgoingMessage:
    compulsory_params = ['id', 'joint_velocitys']
    optional_params = []
    utility.CheckKwargs(kwargs, compulsory_params)

    msg = OutgoingMessage()
    joint_velocitys = kwargs['joint_velocitys']
    num_joints = len(joint_velocitys)

    msg.write_int32(kwargs['id'])
    msg.write_string('SetJointVelocity')
    msg.write_int32(num_joints)
    msg.write_float32_list(kwargs['joint_velocitys'])

    return msg


def AddJointForce(kwargs: dict) -> OutgoingMessage:
    compulsory_params = ['id', 'joint_forces']
    optional_params = []
    utility.CheckKwargs(kwargs, compulsory_params)

    msg = OutgoingMessage()
    joint_positions = kwargs['joint_positions']
    num_joints = len(joint_positions)

    msg.write_int32(kwargs['id'])
    msg.write_string('AddJointForce')
    msg.write_int32(num_joints)
    for i in range(num_joints):
        msg.write_float32(joint_positions[i][0])
        msg.write_float32(joint_positions[i][1])
        msg.write_float32(joint_positions[i][2])

    return msg


def AddJointForceAtPosition(kwargs: dict) -> OutgoingMessage:
    compulsory_params = ['id', 'joint_forces', 'forces_position']
    optional_params = []
    utility.CheckKwargs(kwargs, compulsory_params)

    msg = OutgoingMessage()
    joint_positions = kwargs['joint_forces']
    forces_position = kwargs['forces_position']
    num_joints = len(joint_positions)

    msg.write_int32(kwargs['id'])
    msg.write_string('AddJointForceAtPosition')
    msg.write_int32(num_joints)
    for i in range(num_joints):
        msg.write_float32(joint_positions[i][0])
        msg.write_float32(joint_positions[i][1])
        msg.write_float32(joint_positions[i][2])
        msg.write_float32(forces_position[i][0])
        msg.write_float32(forces_position[i][1])
        msg.write_float32(forces_position[i][2])

    return msg


def AddJointTorque(kwargs: dict) -> OutgoingMessage:
    compulsory_params = ['id', 'joint_torque']
    optional_params = []
    utility.CheckKwargs(kwargs, compulsory_params)

    msg = OutgoingMessage()
    joint_torque = kwargs['joint_torque']
    num_joints = len(joint_torque)

    msg.write_int32(kwargs['id'])
    msg.write_string('AddJointTorque')
    msg.write_int32(num_joints)
    for i in range(num_joints):
        msg.write_float32(joint_torque[i][0])
        msg.write_float32(joint_torque[i][1])
        msg.write_float32(joint_torque[i][2])

    return msg


# only work on unity 2022.1+
def GetJointInverseDynamicsForce(kwargs: dict) -> OutgoingMessage:
    compulsory_params = ['id']
    optional_params = []
    utility.CheckKwargs(kwargs, compulsory_params)

    msg = OutgoingMessage()
    msg.write_int32(kwargs['id'])
    msg.write_string('GetJointInverseDynamicsForce')
    return msg


def SetImmovable(kwargs: dict) -> OutgoingMessage:
    compulsory_params = ['id', 'immovable']
    optional_params = []
    utility.CheckKwargs(kwargs, compulsory_params)

    msg = OutgoingMessage()
    msg.write_int32(kwargs['id'])
    msg.write_string('SetImmovable')
    msg.write_bool(kwargs['immovable'])
    return msg


def MoveForward(kwargs: dict) -> OutgoingMessage:
    compulsory_params = ['id', 'distance', 'speed']
    optional_params = []
    utility.CheckKwargs(kwargs, compulsory_params)

    msg = OutgoingMessage()
    msg.write_int32(kwargs['id'])
    msg.write_string('MoveForward')
    msg.write_float32(kwargs['distance'])
    msg.write_float32(kwargs['speed'])
    return msg


def MoveBack(kwargs: dict) -> OutgoingMessage:
    compulsory_params = ['id', 'distance', 'speed']
    optional_params = []
    utility.CheckKwargs(kwargs, compulsory_params)

    msg = OutgoingMessage()
    msg.write_int32(kwargs['id'])
    msg.write_string('MoveBack')
    msg.write_float32(kwargs['distance'])
    msg.write_float32(kwargs['speed'])
    return msg


def TurnLeft(kwargs: dict) -> OutgoingMessage:
    compulsory_params = ['id', 'angle', 'speed']
    optional_params = []
    utility.CheckKwargs(kwargs, compulsory_params)

    msg = OutgoingMessage()
    msg.write_int32(kwargs['id'])
    msg.write_string('TurnLeft')
    msg.write_float32(kwargs['angle'])
    msg.write_float32(kwargs['speed'])
    return msg


def TurnRight(kwargs: dict) -> OutgoingMessage:
    compulsory_params = ['id', 'angle', 'speed']
    optional_params = []
    utility.CheckKwargs(kwargs, compulsory_params)

    msg = OutgoingMessage()
    msg.write_int32(kwargs['id'])
    msg.write_string('TurnRight')
    msg.write_float32(kwargs['angle'])
    msg.write_float32(kwargs['speed'])
    return msg


def EnabledNativeIK(kwargs: dict) -> OutgoingMessage:
    compulsory_params = ['id', 'enabled']
    optional_params = []
    utility.CheckKwargs(kwargs, compulsory_params)

    msg = OutgoingMessage()
    msg.write_int32(kwargs['id'])
    msg.write_string('EnabledNativeIK')
    msg.write_bool(kwargs['enabled'])
    return msg


def IKTargetDoMove(kwargs: dict) -> OutgoingMessage:
    compulsory_params = ['id', 'position', 'duration']
    optional_params = ['speed_based', 'relative']
    utility.CheckKwargs(kwargs, compulsory_params)
    msg = OutgoingMessage()
    msg.write_int32(kwargs['id'])
    msg.write_string('IKTargetDoMove')
    msg.write_float32(kwargs['position'][0])
    msg.write_float32(kwargs['position'][1])
    msg.write_float32(kwargs['position'][2])
    msg.write_float32(kwargs['duration'])
    if 'speed_based' in kwargs:
        msg.write_bool(kwargs['speed_based'])
    else:
        msg.write_bool(True)
    if 'relative' in kwargs:
        msg.write_bool(kwargs['relative'])
    else:
        msg.write_bool(False)
    return msg


def IKTargetDoRotateQuaternion(kwargs: dict) -> OutgoingMessage:
    compulsory_params = ['id', 'quaternion', 'duration']
    optional_params = ['speed_based', 'relative']
    utility.CheckKwargs(kwargs, compulsory_params)
    msg = OutgoingMessage()
    msg.write_int32(kwargs['id'])
    msg.write_string('IKTargetDoRotateQuaternion')
    msg.write_float32(kwargs['quaternion'][0])
    msg.write_float32(kwargs['quaternion'][1])
    msg.write_float32(kwargs['quaternion'][2])
    msg.write_float32(kwargs['quaternion'][3])
    msg.write_float32(kwargs['duration'])
    if 'speed_based' in kwargs:
        msg.write_bool(kwargs['speed_based'])
    else:
        msg.write_bool(True)
    if 'relative' in kwargs:
        msg.write_bool(kwargs['relative'])
    else:
        msg.write_bool(False)
    return msg


def IKTargetDoComplete(kwargs: dict) -> OutgoingMessage:
    compulsory_params = ['id']
    optional_params = []
    utility.CheckKwargs(kwargs, compulsory_params)

    msg = OutgoingMessage()
    msg.write_int32(kwargs['id'])
    msg.write_string('IKTargetDoComplete')
    return msg


def IKTargetDoKill(kwargs: dict) -> OutgoingMessage:
    compulsory_params = ['id']
    optional_params = []
    utility.CheckKwargs(kwargs, compulsory_params)

    msg = OutgoingMessage()
    msg.write_int32(kwargs['id'])
    msg.write_string('IKTargetDoKill')
    return msg