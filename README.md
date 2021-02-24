## Vuca App
[Storybook](https://vuca.vercel.app/)


## Docker Scenarion

1. ```npm run download-models``` or ```npm run download-models:all``` - Download default models (only once)
1. ```npm run docker:build```
1. ```npm run docker:create``` - After build or after container removal
1. ```su -c "setenforce 0"``` - Disable selinux policies (Temporary) in case of "Permision denied" messages in the console
1. Open [Link](http://localhost:8000)
1. ```npm run docker:stop``` - To stop the container
1. ```npm run docker:start``` - To start after container stop
1. ```npm run docker:remove``` - To remove the container


```ls gpt_2/data``` - List all the models data

In case of stuck training, restart the server (```npm run docker:stop && npm run docker:start```) and go to model metadata(```vim gpt_2/data/models/MODEL_ID/_metadata.json```) and set training to false


## Docker

```npm run docker:build``` - Build the image from the code   
```npm run docker:create``` - Create and start the container  
```npm run docker:start``` - Start stopped container    
```npm run docker:stop``` - Stop the container  
```npm run docker:remove``` - Remove the container  
Open [Link](http://localhost:8000)

## Build prerequisites
```npm```, ```node```, ```python```

### Tested with
```
$ node -v
v12.19.0
```
```
$ npm -v
6.14.8
```
```
$ python --version
Python 3.7.9
```


### Steps

1. (*Recomended*) Set up python virtual enviroment
1. Run ```npm run install```
1. Run ```npm run download-models```
1. Run ```npm run build```
1. Run ```npm run start```

