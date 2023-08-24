from controller import Supervisor
from controller import Robot
from controller import GPS
import math
import random
from controller import Field
import time
import numpy as np
from gym.spaces import Discrete, Box, Dict, Tuple, MultiBinary, MultiDiscrete 
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from gym import Env
from stable_baselines3.common.callbacks import BaseCallback
import os

def actionspace_to_wheel_speeed(np_array):
    output = (int(np_array.argmax())-(len(np_array)/2-1/2))/(len(np_array)/2-1/2)
    if int(np_array.argmax()) < (len(np_array)/2-1/2):
        sign = -1
    else:
        sign = 1
    output = abs(output**(8/5))*sign
    return output

class robot_env(Env):
    def __init__(self):
        # create the Robot instance.
        self.robot = Supervisor()
        self.robot_node = self.robot.getSelf()
        # get the time step of the current world.
        self.timestep = 20
        
        
        self.motors_max_speed_radians = 2*math.pi
        self.left_motor = self.robot.getDevice("motor_L_A")
        self.right_motor = self.robot.getDevice("motor_R_A")
        self.left_back_motor = self.robot.getDevice("motor_L_B")
        self.right_back_motor = self.robot.getDevice("motor_R_B")
        
        self.left_motor.setPosition(float("inf"))
        self.left_motor.setVelocity(0.0)
        
        self.right_motor.setPosition(float("inf"))
        self.right_motor.setVelocity(0.0)
        
        self.left_back_motor.setPosition(float("inf"))
        self.left_back_motor.setVelocity(0.0)
        
        self.right_back_motor.setPosition(float("inf"))
        self.right_back_motor.setVelocity(0.0)
        
        self.motors_max_speed_radians = math.pi*3
       
        
        self.ball_node = self.robot.getFromDef('baller')
        
        
        
        
        self.stacked_frames = 3
        self.observation = np.zeros(shape=(self.stacked_frames,17))
        
        self.steps = 0
        self.max_steps = 2000
        
        
        self.action_space = Box(-1, 1, shape=(10,),dtype=np.float32)

        self.observation_space = Box(-3.4028234663852886e+38, 3.4028234663852886e+38, shape=(self.observation.shape),dtype=np.float32)
        
        
        
        

    def step(self,action):
        self.steps += 1
        
        left_motor_control = action[:5]
        right_motor_control = action[5:]

        left_motor_speed = actionspace_to_wheel_speeed(left_motor_control)
        right_motor_speed = actionspace_to_wheel_speeed(right_motor_control)

    
        self.right_motor.setVelocity(right_motor_speed*self.motors_max_speed_radians)
        self.left_motor.setVelocity(left_motor_speed*self.motors_max_speed_radians)
        self.right_back_motor.setVelocity(right_motor_speed*self.motors_max_speed_radians)
        self.left_back_motor.setVelocity(left_motor_speed*self.motors_max_speed_radians)
        
        self.robot.step(self.timestep)
        
        
        
        
        robot_pos = self.robot_node.getPosition()
        ball_pos = self.ball_node.getPosition()
        ball_velocity = self.ball_node.getVelocity()
        robot_velocity = self.robot_node.getVelocity()
        
        
        robot_to_ball = [ball_pos[0]-robot_pos[0],ball_pos[1]-robot_pos[1],ball_pos[2]-robot_pos[2]]
        vzdalenost_od_koule = (robot_to_ball[0]**2+robot_to_ball[1]**2+robot_to_ball[2]**2)**(1/2)
        
        
        
        dot_product = robot_to_ball[0]*robot_velocity[0]+robot_to_ball[1]*robot_velocity[1]
        absolute_product = ((robot_velocity[0]**2+robot_velocity[1]**2)**(1/2))*((robot_to_ball[0]**2+robot_to_ball[1]**2)**(1/2))
        z_product = robot_to_ball[0]*robot_velocity[1]-robot_to_ball[1]*robot_velocity[0]
        sign = z_product/abs(z_product)
        
        robot_velcity_angle_vs_robot_to_ball_angle = math.acos(dot_product/absolute_product)*sign
        
        # angle betwen two vectors
        
        one_observation = np.asarray([[
            robot_velcity_angle_vs_robot_to_ball_angle,
            vzdalenost_od_koule,
            robot_to_ball[0],
            robot_to_ball[1],
            robot_to_ball[2],
            robot_pos[0],
            robot_pos[1],
            robot_pos[2],
            ball_pos[0],
            ball_pos[1],
            ball_pos[2],
            robot_velocity[0],
            robot_velocity[1],
            robot_velocity[2],
            ball_velocity[0],
            ball_velocity[1],
            ball_velocity[2],]])
            
        self.observation = np.append(self.observation,one_observation,axis = 0)
        if len(self.observation) > self.stacked_frames:
            self.observation = self.observation[1:]
        
        reward = (ball_pos[2]-0.1)
        
        done = False
        if (self.steps > self.max_steps):
            done = True
        
        info = {}
        return self.observation,reward,done,info
    
    def render():
        pass
    
    
       
    def reset(self):
        self.robot.simulationResetPhysics()

        robot_reset_position = [0,0,0.05]
        ball_reset_position = [0.6,0,0.1]
        robot_reset_rotation = [0.707106,-0.707106,1.32679e-06,3.14159]
        new_robot_position = [0.5*random.random()-0.25,0.5*random.random()-0.25,0.08]
        new_ball_position = [2*random.random()-1,2*random.random()-1,0.13]
        new_robot_rotation = [0,0,1,(2*random.random()-1)*math.pi]



        self.left_motor.setVelocity(0.0)
        self.right_motor.setVelocity(0.0)
        
        
        robot_node = self.robot.getSelf()
        robot_position = robot_node.getField("translation")
        robot_position.setSFVec3f(robot_reset_position)
        
        robot_rotation = robot_node.getField("rotation")
        robot_rotation.setSFRotation(robot_reset_rotation)
        
        ball_node = self.robot.getFromDef('baller')
        ball_position = ball_node.getField("translation")
        ball_position.setSFVec3f(ball_reset_position)
       
       
        
        robot_pos = self.robot_node.getPosition()
        ball_pos = self.ball_node.getPosition()
        robot_to_ball = [ball_pos[0]-robot_pos[0],ball_pos[1]-robot_pos[1],ball_pos[2]-robot_pos[2]]
        vzdalenost_od_koule = (robot_to_ball[0]**2+robot_to_ball[1]**2+robot_to_ball[2]**2)**(1/2)
        reward = 1-vzdalenost_od_koule
        
        self.observation = np.zeros(self.observation.shape)
        self.steps = 0
        
        return self.observation
    



class TrainAndLoggingCallback(BaseCallback):

    def __init__(self, check_freq, save_path, verbose=1):
        super(TrainAndLoggingCallback, self).__init__(verbose)
        self.check_freq = check_freq
        self.save_path = save_path

    def _init_callback(self):
        if self.save_path is not None:
            os.makedirs(self.save_path, exist_ok=True)

    def _on_step(self):
        if self.n_calls % self.check_freq == 0:
            model_path = os.path.join(self.save_path, 'best_model_{}'.format(self.n_calls))
            self.model.save(model_path)

        return True





robot_env = robot_env()

dir_id = time.time()
learning_rate = 0.0001
timesteps = 2_000_000
info = f"test{dir_id}_lr={learning_rate}"

CHECKPOINT_DIR = f'C:/Users/david/Desktop/webots/train/{timesteps}_timesteps_{info}_{dir_id}'
LOG_DIR = f'C:/Users/david/Desktop/webots/logs/{timesteps}_timesteps_{info}_{dir_id}'

callback = TrainAndLoggingCallback(check_freq=10000, save_path=CHECKPOINT_DIR)


#print(check_env(robot_env))
model = PPO("MlpPolicy", robot_env, tensorboard_log=LOG_DIR, verbose=1, learning_rate=learning_rate)
model.learn(total_timesteps=(timesteps), callback=callback)
# get the time step of the current world.

    





