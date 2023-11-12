# IEDA-2010-web-scraping
 Web scraping scripts for IEDA 2010 project on student flow
### Aim of the repo
- To solve the allocation problem of charger station, our team has to first identify the *cost* associated with each location (to be determined / classified in a later stage).
- We consider *number of students* in each location as the major cost associated with each location, since it makes sense to consider the aggregated time cost of students to travel to a specific charger station.
- Therefore, our team has to obtain the number of students in each classroom / lift / building each week, which can be obtained through web scraping on the *Class Schedule & Quota* website of UST.
### Assumptions
- To simplify things, we assume users **already signed in** UST with their desired browser.
- For simplicity, we handle the case of "varying classroom throughout the semsmter" loosely, considering only the first classroom assignment.
### Design
- Travel to the [root directory](https://w5.ab.ust.hk/wcq/cgi-bin/2310/), obtain a list of subjects (e.g., "ACCT", "AESF", "AIAA"...). Notice that the letters should be all capital.
- For each `subject`, the the *sub-directory* can be obtained by appending "subject/`subject`" to the root directory.
- Perform scraping in the page of each subject and append the result to a single excel file.
- Lastly, aggregate the raw data in excel.