A simple application for generating dynamic shadows in Pygame

I was working on a simple top-down perspective game in Pygame and I got the idea that adding line-of-sight shadows would add an interesting element.
Initially, I tried filling the game screen with black squares that were programmatically hidden when in the player's LOS (inspired by Die Hard on the NES) but this was very slow and a bit annoying to write.
I discovered that drawing polygons was not only much faster performance-wise, it looked much better and was easier for me to write.

![image](https://github.com/mkenney90/pygame-shadows/assets/54040993/ccf31209-88c4-4d63-b17c-90cca3e61c2e)

