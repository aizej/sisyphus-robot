# sisyphus-robot
A simulated robot in WEBOTS learns how to push a ball up the hill using PPO

![world_sreanshot](https://github.com/aizej/sisyphus-robot/assets/61479273/5afdc343-01af-429f-a3c0-1eeea04d99d2)

Recently I had an idea to make Ai recreate the recent Sisyphus meme so I searched for a robotic simulation program that could run on my PC (not isac-sim) and I found WEBOTS.
It's free and it has built-in robot and environment building options. Plus it also has good integration with python.

the result:
https://github.com/aizej/sisyphus-robot/assets/61479273/beb0de8b-8c38-4fa4-8d05-defa096d9a97



In webots we need to create controller file that is used in the robot Normally this file can not interact with the world only through sensors and the robot but for this simulation, I used the supervisor controller. That allowed me to get any information and interact with the objects in the scene.

Then I used stable baselines 3 gym and created a custom environment:
1) initialization:
  Here we set up some variables as the max speed of our wheels and get all the objects to interact with

![init_function_world_part](https://github.com/aizej/sisyphus-robot/assets/61479273/c9f23292-2eb6-448e-ac71-f46141767040)

  After that, we will set up our network's observation space, action space,steps per round, and stacked frames.
  We usually should stack frames with increased time between them but because One frame already has 17 variables after some testing, we decided that the last 3 frames should be enough.
  
![init_function_network_part](https://github.com/aizej/sisyphus-robot/assets/61479273/51eeddd8-dd9e-42df-b77a-5d89506607b7)


2) Step function:
   This function takes in the actions of our neural network, sends them to our robot, and does one frame of physical simulation.
   
   The action space is in this situation array of 10 split into two.
   One array for the right side and one for the left side.
   I didn't implement action space for every wheel because I didn't see any benefits in it.
   Then this smaller array is put into a function that normalizes it to {-1,1}
   and input as speed to our motors.

![step_1_how_we_drive](https://github.com/aizej/sisyphus-robot/assets/61479273/6eec7a6a-cb8d-48ff-8865-e53c40c5e328)


  This function normalizes an array of any size to  {-1,1} action space:



![drive_functio![drive_function_exuation](https://github.com/aizej/sisyphus-robot/assets/61479273/c108b8b6-1542-4e0e-b78f-76382ac193d9)
n_graph](https://github.com/aizej/sisyphus-robot/assets/61479273/3e33d654-a78b-4414-8e58-39aff85d38fe)

And here is the implementation of that:

![wheel_speed_function](https://github.com/aizej/sisyphus-robot/assets/61479273/9b16fd02-8ac2-4bf3-a9d4-095c6fe57209)









