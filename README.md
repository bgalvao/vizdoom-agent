# Reinforcement Learning Royale?

I don't really know what to call this project as of now.
I want to present cute graphics in a kawaii webpage and all that.
The goal is to compare at least two algorithms:
- [ ] Distributed Deep Q-Network 
- [x] Emergent Tangled Program Graphs ^1
- [ ] Neuroevolution

and common to all:
- [ ] use a [world model](https://worldmodels.github.io/).

In a first instance, these will be tested against a single environment,
[ViZDoom](http://vizdoom.cs.put.edu.pl/). Some time later I'd love to do 
put these to the test and multi-task with OpenAI's Universe.

## Presentation

All shall be published in a webpage hosted by a branch of this repo.


## Running this

Dockerfiles are in the `/docker` folder and follow mainly what's written in the [vizdoom docker directory](https://github.com/mwydmuch/ViZDoom/tree/master/docker).

So after building it, to run it, run

```bash
git clone https://gitlab.com/bgalvao/rl.git
cd rl/docker/vizdoom/
sudo docker build -t rl .
cd ../..
sudo docker run  -ti --net=host -e DISPLAY=${DISPLAY} --privileged --rm -v $(pwd):/home/vizdoom/dev rl
```

Inside the docker image, remember to invoke `python3 cxxx.py`.


^1 Stephen Kelly and Malcolm I. Heywood. 2017.
_Multi-task learning in Atari video games with emergent tangled program graphs_.
In Proceedings of the Genetic and Evolutionary Computation Conference
(GECCO '17). ACM, New York, NY, USA, 195-202.
DOI: https://doi.org/10.1145/3071178.3071303 
