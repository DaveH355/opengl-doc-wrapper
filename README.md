# OpenGL-header-doc
A single file header that wraps glad with OpenGL docs. It's based on OpenGL 4.5 core from [docs.gl](https://docs.gl/).
*Most* functions are included but a couple might be missing. Extensions are not included. 

Other OpenGL versions may be added in the future. The older docs have more typos which makes them harder to parse :)

# Motivation
Not all IDEs are able to give code completion for OpenGL functions loaded by glad. This is not good, especially if you are a beginner. 
Here's an example of what might happen with neovim + clangd
![image](https://github.com/DaveH355/opengl-doc/assets/101005658/46997d64-232c-4930-b056-26067aa22376)

With the header doc, it can give better info
![image](https://github.com/DaveH355/opengl-doc/assets/101005658/a4624818-5d29-4767-828b-055039c5d0b0)


# Usage
You can use this header alongside glad. You can remove it later without affecting your code. 
```c
#include <glad/glad.h>
#include "gldoc.h"
```
