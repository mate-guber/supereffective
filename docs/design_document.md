
## Project overview
This is an educational web app teaching users about pokémon type matchups and what information is worth understanding about Pokémon that are currently popular. A typical user would be someone who is interested in getting more familiar with Pokémon VGC as a beginner or low-intermediate player. This project aims to provide a personalized learning experience by learning what a user struggles with then recommending tailored exercises to eliminate those gaps in knowledge.

## Goals and non-goals
Goals:
* Teach type matchups through adaptive drills 
* Teach speed tier basics 
* Weight question frequency toward meta-relevant Pokémon using live usage data 
* Use knowledge tracing to personalize learning 

Non-goals:
* This project does not give real-time advice for in-game situations 
* It does not evaluate or suggest team compositions 
* It does not simulate full game state and evaluate decisions dynamically 
* It does not teach users through curated, authored questions 

Stretch goals for future versions:
* Teach common Pokémon sets 
* Teach damage thresholds 

## Architecture overview
The architecture has five clear components:
- Data pipeline
- Database
- Question generation engine
- DKT model (Deep Knowledge Tracing)
- Web application — FastAPI backend with Jinja2 frontend

First data is pulled from pokeAPI and showdown stats about type matchups and the current meta pokemon and their speeds/type combinations. This information is stored in a database alongside user data. A python question generation engine takes the raw data from the database and programmatically constructs questions from it. A simple frontend displays the questions and records the user's answers. These answers then get sent back to be stored in the database, and are used as input for a DKT model. This model learns about the user and decides what questions to surface next.

## Data sources and data model
Sources:
**PokeAPI**: Has extensive information regarding pokemon games, species, types, mechanics, etc.
Excellent source of static information. Most relevant to the project are types and species, used to build type interaction matrix and determine speed stats.

**Showdown stats**: Monthly usage statistics broken down into different formats. Can extract most popular pokemon and their moves, items, abilities, spreads, teammates. Will govern which type combinations and speed stats will need to be weighted higher for each month.

Model:
**Type** - Stores a single Pokemon type. Needs a name. Needs a list of relations to other types: 
deals -> double, half, no damage
incoming <- double, half, no damage

**Pokemon** - stores a single pokemon species. Needs a name, a speed stat, and a list of types. (Up to 2 types) 

**Meta data** - stores information about usage statistics. Needs a pokemon name, usage percentage, month, and format.

**Content data** - stores concepts and questions: 
* **Concept** - the unit of knowledge being tracked. Has a category, a description, and a difficulty level perhaps.
* **Question** - a surface presentation of a concept. Has a text field, an answer, and a foreign key linking it to exactly one concept.

**User data** - stores information about the user's account and associated answer history. 
- **User** - has a unique identifier and account credentials.
- **Answer record** - foreign key to user, foreign key to question, correct or incorrect, timestamp.

## ML component
The project uses a DKT model, which essentially has one job: given a user's answer history, what is the probability that they know each concept?

The input for this model is the user's answer history in order - a sequence of interactions that record whether they got a concept correct or not.
The output is a probability between 0 and 1 for every concept in the system, representing the model's belief about whether the user knows that concept. 
The question engine selects the next question based on these probabilities. (low-probability concepts are prioritized)

The model is implemented as an LSTM-based neural network in PyTorch. It is trained on user interaction sequences using binary cross-entropy loss, where the model is penalised for incorrectly predicting whether the user knew the next concept tested.

A significant weakness of this approach is its susceptibility to the cold start problem. To counteract this issue, a weighted question selection approach can be adopted (based on meta-relevance) until sufficient real user data accumulates. Another viable option is to generate synthetic training data to bootstrap the model.

## Build phases
**Phase 1 - Data Groundwork** 
Pull relevant data from PokeAPI and Smogon, then store those in a database. Since the first feature is going to be the type-matchup drills, I will need this data as a base to get started on that. I will probably need the last month's Smogon usage stats as well, so that the question engine can have a baseline for how to select for now.

**Phase 2 - Question Engine** 
Build the type matchup question generator. It should select questions based on the meta-weighting. 

**Phase 3 - User Interface**
A simple web interface is needed to display the questions and record the answers so a response can be given.

**Phase 4 - User Functionality** 
Implement an account system that stores relevant information about the user, including their answer history.

**Phase 5 - DKT Model** 
Build and train the DKT model in PyTorch. Connect its predictions to the question engines selection method.

**Phase 6 - Daily Training** 
Implement the daily training session feature and clean up the frontend. Add the onboarding quiz and a form of user progress tracking.

**Phase 7 - Speed Tiers** 
Add the next concept to the system, speed tiers. Pull and store relevant data from PokeAPI.

## Key decisions and reasoning

I chose Pokemon VGC as the domain for this project because there is a large amount of well-structured data publicly available, and I have enough domain knowledge to confidently make good design decisions.

I decided to write the project in Python because there is a mature ecosystem of frameworks and libraries that support both the machine learning and web app components of the project, and because I have substantial prior experience with the language. 

I considered Django and Flask as backend frameworks but ultimately chose FastAPI for the project. It is a fast and modern framework that is commonly used in ML serving contexts, which makes it a great fit. 

For the frontend I considered React but decided to go with Jinja2 because the added complexity wasn't justified for the goals of this project. Building a frontend agnostic core allows me to replace the UI in the future without much effort. 

I decided to use DKT over a simpler approach, like a weighted counter, because it captures the relationships between underlying concepts, which fits the educational nature of the project much better. This approach has a cold start problem however, which I mitigate by having new users fill out an onboarding quiz that gives the model a more informed starting point as well as adopting a meta-weighted question selection approach until sufficient real user data accumulates.

The target of this project are beginners and low-intermediate players because the knowledge being drilled is foundational to the domain, thus it's most impactful at the beginner level. For newer players the lack of memorisation of static information poses a significant bottleneck, one that more experienced players have already cleared through their experiences with the game.

I excluded team composition analysis from the project because the underlying synergies between different pokemon can't easily be quantified and solving that issue lies beyond the scope of this project. Similarly, I decided to exclude real-time match advice as well because an automated system can't feasibly reason about a game state with sufficient accuracy due to these underlying synergies and the simple fact that Pokemon is a game of imperfect information. I feel that such a system would compromise the educational nature of this project. 

I decided to push the implementation of the additional topic of speed tiers to the last phase of development because it allowed me to focus on building a solid foundation first and highlighted the benefit and importance of building a decoupled, modular solution. This foundation allows for easier extensibility in the future. 