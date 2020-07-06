CheapShot
===
CheapShot is a tool which can detect potentially toxic tweets from any Twitter account.

### Usage
Firstly, ensure that all the requirements are installed. The CheapShot.py file takes one of three arguments:

| Argument | Shortform | Description                                                                                                |
|----------|-----------|------------------------------------------------------------------------------------------------------------|
| --user   | -u        | Search for toxic tweets for single user by username                                                        |
| --file   | -f        | Search for toxic tweets for multiple users by txt file containing list of usernames seperated by a newline |
| --help   | -h        | Show descriptions for options                                                                              |


### How it works
CheapShot uses Twint to source the tweets from a user and then filters them through [IBM's toxic comment classifier](https://github.com/IBM/MAX-Toxic-Comment-Classifier) to discover potentially toxic comments.
The toxic comment classifier employs a state-of-the-art pre-trained BERT-Base, English Uncased model to detect potentially toxic comments, it then seperate them into 6 different toxicity types: Toxic, Severe Toxic, Obscene, Threat, Insult and Identity hate.


### Requirements
* [MAX-Toxic-Comment-Classifier docker image](https://github.com/IBM/MAX-Toxic-Comment-Classifier#deploy-from-docker-hub)
* Twint
* Pandas
* BeautifulSoup
