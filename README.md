# opengl-doc-wrapper
A single file header that wraps glad with OpenGL docs. It's based on OpenGL 4.5 from [docs.gl](https://docs.gl/).
*Most* functions are covered but some might be missing. Extensions are not included. 

Other OpenGL versions may be added in the future. The older docs have more typos which makes them harder to parse :)

# Motivation
Not all IDEs are able to give code completion for OpenGL functions loaded by glad. This is not good, especially if you are a beginner like me. 
Here's an example of what might happen with neovim + clangd
![image](https://github.com/DaveH355/opengl-doc/assets/101005658/46997d64-232c-4930-b056-26067aa22376)

With the documentation wrapper, it can give better info
![image](https://github.com/DaveH355/opengl-doc/assets/101005658/94f6fe93-e2bb-44d5-9143-998b31a1e7dd)


# Usage
Get started by downloading the necessary files from this project's include folder. 
You can use the header alongside glad. You can remove it later without affecting your code. 
```c
#include <glad/glad.h>
#include "gldoc.h"
```

# Building
So you want to generate your own documentation wrapper. Awesome.

First go to the docs.gl [repo](https://github.com/BSVino/docs.gl/) and 
follow the instructions to build the needed html files.
Then copy the output folder `htdocs` to this project and execute `main.py`

Note due to typos, you may have to manually fix syntax errors. The docs also use MathJax for displaying math which 
does not translate well to plain text. The parser will warn about such cases. 
