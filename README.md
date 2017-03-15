# CU-me - CUNY Scheduling Simplified.

A long-term project finally in its first stage of completion.

Making a class schedule every semester at a CUNY campus is a nightmare. Juggling between RateMyProfessors, the abysmal UI of CUNYFirst, a schedule visualization site like FreeCollegeScheduleMaker, and DegreeAudit makes scheduling a daunting, annoying experience that students have to go through each semester.

CU-me aims to fix these issues :) Maybe not all of them, but, hopefully, it makes things a bit easier.
## What's already been done
* Integration with DegreeWorks: the left tab shows you a glorious list of classes you still need to complete to graduate (based on your DegreeAudit). Classes with full codes like CSCI 12700 are clickable and it will automatically search the course catalog for that course for the most recent term.
* Integration with CUNYFirst search: completely bypassing the CUNYFirst login, you can search for any class at any CUNY campus.
* Integration with RateMyProfessors: each class returned from a search has an overall rating for a professor and the professor's hardness rating (this only works for professors that are in the RateMyProfessors database, of course. Sorry, 'Staff' has no ratings).

The schedule you create gets saved to a PostgreSQL database, so all edits to your schedule are secure.
You can download the schedule as an image by clicking on the small download button.
## What's yet to be done
* Saving the schedule name to the database. Yes, I honestly thought of this one while making this list, so it should be done soon.
* Saving the schedule name to the downloaded image. I tinkered with this for a bit, but couldn't get it to work. Have to get back to it.
* Hiding the optional parts of the search form until the user needs them. They take up a lot of space and most people won't use many of the other search filters.
* *Very Important* A progress indicator. This one's not fair. I have a local build of this site for development, on which this works. When you're logging in or searching, it updates you with a quirky text message as it's going through the process. I implemented it with global variables, which don't work for a multi-worker gunicorn setup that I have on the production build. I tried using Celery, but abandoned it temporarily because it was so finnicky. I'm so sad that I have this one working, but nobody can see it yet :( stick around.

Now. I managed to bypass CUNYFirst search, but I had to sacrifice one crucial thing to make it work. When you add a class to the schedule, you don't get the list of labs, recitation, or discussions if it is a combined section class. This information can only be accessed by logging in and selecting the class while logged in. I mean, as far as I know. Anyway, this is a *BIG* problem. Hopefully, I can figure something out.

If you want to read how I did it, this is the [tech readme](https://github.com/bhernandev/CUNYsecond/blob/master/TECH_README.md).
