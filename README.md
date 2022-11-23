# SEAN
>*Development team: Anne Leemans (lead) & Fraukje Coopmans*



## Overview
The goal of this project is to develop off-the-shelf data-science products. We aim to make those products accesabable via a webinterface both for students and HU employees. The following image shows a rough outline of the project workflow.

![](images/sean-phases-flow.png)

As seen in the above schema the flow can be devided roughly three phases. 

### Phase A
Goal of the project is to create off the shelf data science products developt in pyhton (or any other languan
ge). These products can run as an independent app locally or can be trigger via an online UI. They can run independelty or can be combined. In the current working version we devloped two applications
1.  Sentiment analysis app:an algorithm that performs sentiment analysis on text with the aim of providing a sentiment score, specifically aimed at HU student-related data (STudent Information Point requests, open-ended questions from student questionnaires, HU twitter, etc.). This application takes a CSV file containing two columns, an id column and a text column. The text column is scanend through the sentiment analysis, an extra column is created with the sentiment score. A CSV with this extra column is than returned to the user. More info about this application can be found [here.](results\resultaten-versie-0.2.md)
2.  Emailthread to email app: this application splits email threads into seperate emails and saves them in seperate columns. It takes a csv file with two columns, an id column and a column with emailthreards. It splits the emailthread column an returns a csv file. 

As stated both apps can be run indepeldently from eachother but the output of the emailthread to email app can be used for the sentiment app aswell. 
The schema in the overview bullet shows a vew grayed out applictions. The projects aim is to create a framework where we can easliy add more products (applications in the future). We aim to build a grid where containers can be added (or detached) without impacting any of the outer containers in the grid. Even if there is an interdependence between containers, since the goals is that they are always capable of running indepedently (as for example the emailthread and sentiment analysis)

>NOTE! in phase A we develop the apps locally. These are python scripts that run on a local (or virutal) machine that con not be accesed via the web or any other interface. 


#### Sentiment analysis
Container apps
Current (working example) sentiment analyis 
More products can be developed 
Container apps that can be either hosted but work locally or combined (think email thread to email and sentiment analysis)


### Fase B
![](images/flask-logo.png)

Develop flask app (or maybe Django?)
First locally hosted for testing 


### Fase C

This is the first time we see the user 
Create UI 
Where do we host 
How does it interact with app
Azure function App with HTTP Trigger? More info [here](https://learn.microsoft.com/en-us/samples/azure-samples/flask-app-on-azure-functions/azure-functions-python-create-flask-app/)


