# SQLalchemy & Flask: API Creation and Climate Analysis 

### Project description:
Using SQLAlchemy to do basic climate analysis and data exploration. Specifically using SQLAlchemy ORM queries, Pandas, and Matplotlib. 

Based on the above analysis, I have created a Flask API and based it on the ORM queries developed in the section above. The API includes the following routes: 
* **'/'** Route
* **'/home'** Route
* **'/api/v1.0/precipitation/'** Route
* **'/api/v1.0/stations'** Route
* **'/api/v1.0/tobs'** Route
* Dynamic routes (user based input):
    * **'/api/v1.0/start'** Route -> This will provide the minimum, maximum, and average temperature from the specified startdate onwards. 
    * **'/api/v1.0/start/end'** -> This will provide the minimum, maximum, and average temperature from the specified startdate to the specified end date. 


### Analysis Images
![line_chart](https://github.com/Kokolipa/sqlalchemy-challenge/blob/sqlalchamy/SurfsUp/Images/Fig_1.png)

![histogram](https://github.com/Kokolipa/sqlalchemy-challenge/blob/sqlalchamy/SurfsUp/Images/Fig_2.png)
#### Folder structure
``` yml
.
├── SurfsUp
│   ├── Images    
│   |   ├── Fig_1.png
│   |   ├── Fig_2.png               
│   ├── Resources
│   ├── hawaii_measurements.csv   
│   ├── hawaii_stations.csv 
│   ├── hawaii.sqlite      
│   ├── app.py
│   ├── climate_starter.ipynb
|___.gitignore               
|___README.md
``` 

