### CU-me is a Django server with an NGINX server on top.
For the list of dependencies and libraries I use, check [requirements.txt](https://github.com/bhernandev/CUNYsecond/blob/master/requirements.txt).

Being Django most of my code is written in Python.

#### Logging in
*Implemented in [apiRequests.py](https://github.com/bhernandev/CUNYsecond/blob/master/cume/api/apiRequests.py)*
Every time a user logs in, a request is sent to the server, which opens up a Selenium browser window that naviagates to CUNYPortal, inputs the user's login info, goes to DegreeAudit from there, scrapes all of the still required classes and finally returns the schedule page with JSON of the required classes.
I do save the person's CUNYPortal username and hashed password in the PostgreSQL database to save added classes.
`Selenium` is a robobrowser library. I needed Selenium because after trying to work with CUNY sites through Requests and other libraries, none of them stored the necessary cookie and session data for CUNY to return proper content. Selenium actually imitates a real browser, so it actually logs in and everything works.
I use `PhantomJS` as Selenium's webdriver. It is a headless browser, incredibly lightweight and fast compared to Chrome or Firefox.
#### Searching
*Implemented in [apiRequests.py](https://github.com/bhernandev/CUNYsecond/blob/master/cume/api/apiRequests.py)*
Searching works basically the same way as logging in. When a user submits the search form, the page sends and AJAX request to the server. The server then opens a new Selenium browser and goes to the guest CUNYFirst search page, fills the search form with the user input, scrapes the results, for each professor tries to get his or her RateMyProfessors (I'll call it RMP) ratings, and then returns a JSON response.
#### Filling the search form
*Implemented in [searchForm.py](https://github.com/bhernandev/CUNYsecond/blob/master/cume/search/searchForm.py)*
Terms change, departments are added, so the CUNYFirst search form changes. For example, Lehman still doesn't have a list of departments for the 2017 Fall term, which, I think, means they haven't added a course catalog for Fall 2017 yet. Maybe they did when you're reading this, but I promise you it was blank! Anyway, to update my form based on the CUNYFirst form, I just run a daily `cron` task, which scrapes the search form with Selenium.
#### Drawing the schedule
*Implemented in [canvas.js](https://github.com/bhernandev/CUNYsecond/blob/master/cume/static/schedule/js/canvas.js)*
The schedule is actually a combination of multiple canvases drawn on top of each other. One canvas has the vertical lines separating the days of the week. A second canvas has horizontal lines separating the different times. And then, a new canvas is overlayed for each class added. Actually, if a class meets 3 times a week, 3 new canvases will be added, AND three more canvases, which have the `onhover` info like RMP ratings and so on. So yeah...a lot of canvases. I checked many libraries and this was the best solution for me.
If you add a class outside the schedule times or days, it redraws itself appropriately. Adding and deleting classes performs that action on the corresponding canvas element. So if you delete a class, it just deletes its canvases. It also sends an AJAX request (for addition or deletion of a class) to the server to add or delete that class from the user's classes in the PostgreSQL DB.
