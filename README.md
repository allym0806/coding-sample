
### Introduction
This code sample explores the relationship between the implementation of the Infrastructure Investment and Jobs Act (IIJA) and the changes in Unemployment Rate in the US. Following the COVID-19 pandemic, the US has experienced a significant increase in unemployment rates. In November of 2021, the IIJA was signed into law by President Biden, investing $16.7 billion to improve infrastructure and create job opportunities. As each state received different amounts of funding, this study utilizes the differences to investigate the impact of these fundings on reducing unemployment rates for each state using the OLS model. 

### Datasets
This analysis employs 2 datasets: the first is iija_projects.xlsx, which includes a list of all projects funded by IIJA with details on their respective state, amount, category of industry, and such. The second dataset will be retrieved through Fred to create df_ur, which includes monthly unemployment rates of each state from 2021 to 2022. 

### Analysis
The OLS model is used, with IIJA funding dollar amount by state as independent variable, and percent change in unemployment rate by state as dependent variable. The intercept of -26.04 indicates that when no funding is present, unemployment rate is expected to decrease by 26.04% on average. The coefficient for funding is -9.08e-10, which implies that for every one-dollar increase in IIJA funding, there is an associated decrease of 9.08e-10 percent in the change in unemployment rates. However, the p-value for FUNDING is 0.106, indicating that the result is not statistically significant. 

### Conclusion
In summary, the regression analysis does not find IIJA funding to be a statistically significant predictor of the change in unemployment rates between 2021 and 2022. There may be multicollinearity issues that have impacted regression results, and there may be other more accurate methods, such as looking at the impact of IIJA on employment in specific industries. Future research may perform more accurate analyses by resolving these issues. 
