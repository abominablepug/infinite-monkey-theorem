# Infinite Monkey Theorem

<img width="939" height="704" alt="screenshot_2026-02-16_23-15-16" src="https://github.com/user-attachments/assets/cad13426-c6c3-428f-8499-418106390539" />

## What is it?
The Infinite Monkey Theorem is a commonly cited theorem which posits that if a monkey were to hit a key at random on a typewriter for eternity, eventually it would write every and any given text including the full works of William Shakespeare in order. Its more generalized conclusion is that any infinite sequence of completely random and independent events will result in infinitely many occurrences. For example, it is physically possible that if an apple were to be placed in a vacuum and then decay it could eventually completely restore itself back to its original form. If you want to learn more about this theorem visit the wikipedia page [here](https://en.wikipedia.org/wiki/Infinite_monkey_theorem).
## What's this project?
This project is a way to simulate the infinite monkey theorem within a docker image locally. After setting up the docker image you can open the website in your browser and begin the monkey's typewriting journey. Well, you can also end it whenever you want and send him back to square one if you're a heartless ruthless human being. These can all be done with the provided buttons to start the typing, stop the typing, and reset. From there you can also see which words the monkey has successfully written, how many times it's written that word, and when it wrote it. By checking the found words category you'll see all of those human words and can sort or search through them to find your favorites. To save on RAM the letters are not all saved and neither are the words. Instead the words are saved in a seperate JSON file meaning that it will persist even if the monkey dies ☹️. **Warning!!! IF YOU LEAVE THE DOCKER RUNNING THE SIZE OF THE JSON FILE WILL CONTINUE GROWING**.
## Purpose
The purpose of this docker image is simple: monkey yearns to become next shakespeare. In reality, I needed something for my idling raspberry pi 5 to do and I thought that this was the perfect task to waste perfectly good resources while making something fun. Realistically, there's no need for this and it solves no problems but not everything has to and who knows maybe the monkey will create the cure for cancer, end world hunger, or bring world peace. There's no way to rule it out until you give the monkey the typewriter and let it write!
## Setup
To setup the project on your own server ort computer do the following:
1. Clone the repo using your preferred method
1. `cd infinite-monkey-theorem`
1. Edit the `docker-compose.yml`:
    * Update the `PUBLIC_BACKEND_URL` to you server's IP.
    * Adjust the ports for the frontend (5173) and backend (8000) if they're already in use.
1. run `docker compose up -d`
1. Open the website in your browser at the frontend port you set and enjoy!
#### Disclaimer
The monkey is untested. It is very possible it types slurs or vulgar/explicit language. Statistically it's possible for it to type out some of the most heinous things in the entire world so just be warned.

#### Future features
* [ ] smart monkey (instead of random it has the probability of each letter + space)
* [ ] central server for all docker instances to report to
* [ ] text checker (see how close you are to recreating a text... not in order ofc)
* [ ] sentence maker (use words as building blocks to make your own monkey texts)

