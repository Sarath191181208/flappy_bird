[![Run on Repl.it](https://repl.it/badge/github/Sarath191181208/Template_Generator)](https://repl.it/github/Sarath191181208/Template_Generator)

# AI Flappy bird

Ahh! The classic flappy bird game where you could just tap the screen & avoid the pipes. It was so great back then. I tried to use NEAT Algorithm to create an AI capable of playing flappy bird.

# Description

This project mainly uses NEAT algorithm to achieve the task of AI playing the game. All the players are scored based on their distance therefore more distance intrun gives more score. Thus, more chance of having an offspring.

## Demo

![Image](https://github.com/Sarath191181208/Template_Generator/blob/master/images/Screenshot.png)

## Features

- AI playing the game of Flappy bird.
- Save the current best fit model for the current generation.

## Run Locally

Clone the project

```bash
  git clone
```

Go to the project directory

```bash
  cd ./Template_Generator
```

Install dependencies

```bash
  pip3 install -r requirements.txt
```

Run the project Locally

```bash
  python main.py
```

## References

- [Code bullets video on Flappy bird AI](https://www.youtube.com/watch?v=WSW-5m8lRMs)
- [Tech with Tim's tutorial on how to build Flappy bird AI](https://www.youtube.com/playlist?list=PLzMcBGfZo4-lwGZWXz5Qgta_YNX3_vLS2)

## Hot keys

- S : Save the current leading offspring of this generation.

## Further Work

- [ ] Select screen.
- [ ] select the saved generation & see it play.
- [ ] Allow the human to play with the AI.

## Requirements

- python `Make sure to add to path`
- pygame `pip3 install pygame`
- tkinter `default`
- pyinstaller `pip3 install pyinstaller` this is to create an exe alternatively you can use auto-py-to-exe `pip install auto-py-to-exe`
- colorama `pip3 install colorama`

## Authors

- [Sarath](https://www.github.com/https://github.com/Sarath191181208)
