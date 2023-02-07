# Backend Coding Challenge

We appreciate you taking the time to participate and submit a coding challenge. In the next step we would like you to
create/extend a backend REST API for a simple note-taking app. Below you will find a list of tasks and limitations
required for completing the challenge.

### Application:

* Users can add, delete and modify their notes
* Users can see a list of all their notes
* Users can filter their notes via tags
* Users must be logged in, in order to view/add/delete/etc. their notes

* You don't have to use docker if you don't want, as long as the application builds locally is fine.

### The notes are plain text and should contain:

* Title
* Body
* Tags

### Optional Features 🚀

* [ ] Search contents of notes with keywords
* [ ] Notes can be either public or private
    * Public notes can be viewed without authentication, however they cannot be modified
* [ ] User management API to create new users

### Limitations:

* use Python / Django
* test accordingly

### What if I don't finish?

Try to produce something that is at least minimally functional. Part of the exercise is to see what you prioritize first when you have a limited amount of time. For any unfinished tasks, please do add `TODO` comments to your code with a short explanation. You will be given an opportunity later to go into more detail and explain how you would go about finishing those tasks.


### URLS:
#### home url: 127.0.0.1:8000 -> 
* Anonymouse user can see all public notes, but cannot create, update or delete
* Authenticated user can see all public notes and all his/her notes
    * He/She can filter notes by tag and id
    * He/She can search notes by keyword 

#### mynotes url: 127.0.0.1:8000/mynotes/add -> 
* Authenticated user can create note
#### mynotes url: 127.0.0.1:8000/mynotes/id -> 
* Authenticated user can update or delete note based on the request

#### tags url: 127.0.0.1:8000/tags -> 
* Authenticated user can see list of the tags or create or a tag based on the request

