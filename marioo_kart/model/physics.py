"""Car physics constants and the terrain grip scale.

All the values of this module are expressed in the simulation units used by
the game: distances are in pixels, speeds in pixels per second, accelerations
in pixels per second squared and angles in radians.

Every grip value of every terrain must be multiplied by :data:`GRIP_SCALE`.
The multiplication is performed once, in :meth:`model.terrain.Terrain.grip_coefficient`.
"""

GRIP_SCALE = 0.87

# Longitudinal behaviour.
ENGINE_ACCELERATION = 330.0
REVERSE_ACCELERATION = 175.0
BRAKE_DECELERATION = 540.0
MAX_SPEED = 520.0
MAX_REVERSE_SPEED = 170.0

# Air friction: the velocity is damped by AIR_DRAG * speed every second.
AIR_DRAG = 0.0014

# Steering.
STEER_RATE = 2.65
STEER_FULL_SPEED = 120.0
MAX_STEER_ANGLE = 0.6
STEER_SMOOTHING = 12.0

# A drift starts above the terrain drift threshold and stops below
# DRIFT_EXIT_RATIO times this threshold (hysteresis avoids flickering).
DRIFT_EXIT_RATIO = 0.55

# Boost pads.
BOOST_ACCELERATION = 300.0
BOOST_DURATION = 1.2
BOOST_COOLDOWN = 0.45

# Visual speed conversion.
SPEED_DISPLAY_FACTOR = 0.36