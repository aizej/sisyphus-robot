# sisyphus-robot
A simulated robot in WEBOTS learns how to push a ball up the hill using PPO

![world_sreanshot](https://github.com/aizej/sisyphus-robot/assets/61479273/5afdc343-01af-429f-a3c0-1eeea04d99d2)

Recently I had an idea to make Ai recreate the recent Sisyphus meme so I searched for a robotic simulation program that could run on my PC (not isac-sim) and I found WEBOTS.
It's free and it has built-in robot and environment building options. Plus it also has good integration with python.

the result:
video:
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


![drive_exuation](https://github.com/aizej/sisyphus-robot/assets/61479273/2ddae8c0-157e-4b6d-86d2-366e50fd451b)
![drive_function_graph](https://github.com/aizej/sisyphus-robot/assets/61479273/323cb82a-e95b-4c04-b9d2-ddac8041fa14)


  And here is the implementation of that:
  (I only switched the power to 8/5 instead of 9/5)

![wheel_speed_function](https://github.com/aizej/sisyphus-robot/assets/61479273/9b16fd02-8ac2-4bf3-a9d4-095c6fe57209)

 Now we need to get all the positions and the angles of the robot and the boulder:

 ![angle_calculation_implementaion](https://github.com/aizej/sisyphus-robot/assets/61479273/2c11ce1e-73d1-43de-a4e2-9710938a9675)


To get the rotation I thought I could get the rotation right from webots and just subtract it from the direction from the robot to the boulder.
but the one that I could access from webots was not usable so I decided to calculate it from the robot's speed using the dot product and z product.
Here the last row is the awnser for the least positive or negative angle to the right direction (to the boulder)

![angle_calculation_graph](https://github.com/aizej/sisyphus-robot/assets/61479273/7af3c3b2-18fe-42bf-a84c-b74ab8022244)

Then we pass the current steps information to observation and stack it so we can pass it to the network:

![observation](https://github.com/aizej/sisyphus-robot/assets/61479273/76c308e4-05fd-4a91-9eee-8fef1dcb40fb)

Then it's important to choose a good reward function. So I chose something simple:
The reward will be how high the ball currently is.

![reward](https://github.com/aizej/sisyphus-robot/assets/61479273/4fa5962b-0bf1-40fd-b7c6-f9220dc99879)

And set done to true if we complete the last step of the episode:

![done_function](https://github.com/aizej/sisyphus-robot/assets/61479273/5ff8316e-14b8-4fde-ad6e-f96e5e6955eb)

3) The reset function:

We set the robot back to its starting position the ball to its starting position and reset the step counter.

![reset_function](https://github.com/aizej/sisyphus-robot/assets/61479273/413801e9-1c2f-48ed-99e4-36aa21937312)

After all that we create a logger and start learning with PPO!

Reward:

![reward_screanshot](https://github.com/aizej/sisyphus-robot/assets/61479273/443485fd-cae6-4989-b310-42ee9b2f457b)


video:
https://github.com/aizej/sisyphus-robot/assets/61479273/51f89076-8945-44d4-a4f2-4477627e9179

   







