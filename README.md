# muse
Beta API
UI: https://xd.adobe.com/view/704a027d-7062-42b8-8e86-7863382e7131-2519/

# To Do

Hey Shawn, there's a couple challenges I've been facing that I think might be better to solve than the payments issue:
1. I've been doing the demo by remoting in to my PC and the lag isn't great. Can we get it hooked up to an URL? We already own vuca.ai
2. If we can just put a password on the web page that should secure things momentarily. I'm only demoing it with people I really trust.
3. Right now the entire sequence needs to be generated before you can see anything. I think it'd be better if it can generate bit by bit while it's going. Kind of like talktotransformer used to do. https://news.ycombinator.com/item?id=20749037

- [ ] Connect "vuca.ai" URL
- [ ] Password protect URL
- [ ] Set up API on preemptible P4 GPUs (Or better, your call) on Google Kubernetes Engine
- [ ] Main: Create generic “Change Applications” button/modal component

## Docker

1. ```npm run download-models``` or ```npm run download-models:all``` - Download default models (only once)
2. ```npm run docker:build``` - Build the image from the code   
3. ```npm run docker:create``` - Create and start the container 
4. ```npm run docker:start``` - Start stopped container    
5. ```npm run docker:stop``` - Stop the container  
6. ```npm run docker:remove``` - Remove the container  
