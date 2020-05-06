Steps to run :
1. Make sure you have python3 & pip3. If not upgrade to both.
2. Then ``sh setup.sh``. That should start the server.
3. Go to ``http://0.0.0.0:5000/graphql``
4. Type the below api use cases into the graphQL query tool.
5. You can do the same thing using curl command or Postman or any rest client as well.


**Disclaimer** 

**A lot of things that make this code production ready are pending. For example, SQL injection prevention, bad input handling in some cases and adding tests.**


Use the same resolver for all 4 cases. 

There are four columns to use : 
1. groupBy - Format : ["os", "channel"] - optional
2. orderBy - Format : ["channel desc", "os asc"] - optional 
3. sumOf - Format : ["impressions", "revenue"] - You can put these output into ordering clause by 
    using orderBy: ["impressions_sum desc" , "revenue_sum asc"]
4. filterBy - Format: ["country='CA'", "os='android'"]
5. fromTime - Format : "YYYY-mm-dd"
6. toTime - Format : "YYYY-mm-dd"
7. ratioOf - Format: ["spend:installs", "impressions:clicks] - These translate to sum(spend)/sum(installs) 
    for the given grouping. You can put these output into ordering clause by using 
    orderBy: ["spend_by_installs desc", "impressions_by_clicks asc"].

api use case: 1

``
{
  analyzeTrackingRecords(groupBy: ["os", "country"], orderBy: ["channel desc"], sumOf: ["impressions", "clicks"], fromTime: "2017-5-10", toTime: "2017-05-20") {
    column {
      key
      value
    }
  }
}
``

api use case: 2

``
{
  analyzeTrackingRecords(groupBy: ["date"], orderBy: ["date asc"], sumOf: ["installs"], fromTime:"2017-05-23", toTime:""){
    column{
      key
      value
    }
  }
}
``

api use case: 3

``
{
  analyzeTrackingRecords(groupBy: ["os"], orderBy: ["os asc"], sumOf: ["revenue"], fromTime:"2017-06-01", toTime:"2017-06-01"){
    column{
      key
      value
    }
  }
}
``

api use case: 4 

``
{
  analyzeTrackingRecords(groupBy: ["os"], orderBy: ["spend_by_installs desc"], sumOf: ["revenue"], fromTime:"2017-06-01", toTime:"2017-06-01", ratioOf: ["spend:installs"]){
    column{
      key
      value
    }
  }
}
``
