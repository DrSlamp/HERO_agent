import os
from gym.envs.registration import register

# Allowing environment to have sounds
if "SDL_AUDIODRIVER" in os.environ:
    del os.environ["SDL_AUDIODRIVER"]

register(
    id="Hero-v0",
    entry_point="gym_environments.envs:HeroEnvV0",
)

register(
    id="Hero-v1",
    entry_point="gym_environments.envs:HeroEnvV1",
)
