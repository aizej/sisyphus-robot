# sisyphus-robot
A simulated robot in WEBOTS learns how to push a ball up the hill using PPO

Recently I had an idea to make Ai recreate the recent Sisyphus meme so I searched for a robotic simulation program that could run on my PC (not isac-sim) and I found WEBOTS.
It's free and it has built-in robot and environment building options. Plus it also has good integration with python.

the result:
https://github.com/aizej/sisyphus-robot/assets/61479273/beb0de8b-8c38-4fa4-8d05-defa096d9a97




In webots we need to create controller file that is used in the robot Normally this file can not interact with the world only through sensors and the robot but for this simulation, I used the supervisor controller. That allowed me to get any information and interact with the objects in the scene.

Then I used stable baselines 3 gym and created a custom environment:
1) initialization:
![init_function_world_part](https://github.com/aizej/sisyphus-robot/assets/61479273/c9f23292-2eb6-448e-ac71-f46141767040)


