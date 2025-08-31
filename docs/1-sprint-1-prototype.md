# Sprint 1 - A Working UI Prototype


## Sprint Goals

Develop a prototype that simulates the key functionality of the system, then test and refine it so that it can serve as the model for the next phase of development in Sprint 2.

[Figma](https://www.figma.com/) is used to develop the prototype.


---

## Initial Database Design

The initial plan is to use a database with three connected tables: 
-Clients; for storing names, contact details, status, and personal notes. 
-Meetings; links to specific clients, with fields such as date, time, type (what type of client e.g. active, inactive), and (very importantly) notes. 
-Follow-ups; also linked to a specific client, with fields such as follow-up type (e.g. catchup, phone call), priority, and status (complete, ongoing, cancelled).

![SCREENSHOT OF DB DESIGN](<img width="2206" height="568" alt="image" src="https://github.com/user-attachments/assets/0b7447dd-c488-45e6-8f67-2c445ff80d64" />
)


---

## UI 'Flow'

The first stage of prototyping was to explore how the UI might 'flow' between states, based on the required functionality.

This Figma demo shows the initial design for the UI 'flow':

<iframe style="border: 1px solid rgba(0, 0, 0, 0.1);" width="450" height="800" src="https://embed.figma.com/proto/LJ3z7bs0P09xXtjfMEZnVb/Untitled?node-id=2-3625&scaling=min-zoom&content-scaling=fixed&page-id=0%3A1&starting-point-node-id=2%3A3761&embed-host=share" allowfullscreen></iframe>

The first figma prototype was built to test how the app would flow from page to page- starting at the client management dashboard, then into scheduling meetings, and finally to setting up follow-ups.


---


### Testing

After getting feedback from my stakeholder He stated stated the system should ultimately help answer these three main questions:

Who have I seen?
What was the result of that interaction?
What action is needed?
>I want all clients in a searchable list - even ones I couldn't previously sell. It's important to keep track of everyone.
>I also need to see outcomes and follow-ups - calls, catchups, ect; everything all in one place for each client.
>Personal notes matter- those small details/idiosyncrasies help me remember who prefers what, or what makes each client happy.
>Overall, its important to remember that I do not need or want a complex system - I just need something organized that lets me store client info, track interactions, and manage the next steps easier.

### Changes / Improvements

I added a section to show outcomes of meetings and follow-ups (canceled, complete ect), status for client (i.e. active or inactive), next actions added for follow-ups
After getting feedback, I made several changes to improve the design and make it more useful: 
-Added a searchable client list that includes all clients (even ones who could not be previously be sold to) so they can be revisited later on
-Added a way to tag the result of each client interaction (e.g. successful, unsuccessful, follow-up needed)
-Created a dedicated section on the client page to track follow-ups such as calls, emails, or catch-ups (in person)
-Kept the entire layout minimal, based on my fathers comment: >Don't make it more complicated than it need to be


*FIGMA IMPROVED PROTOTYPE - PLACE THE FIGMA EMBED CODE HERE - MAKE SURE IT IS SET SO THAT EVERYONE CAN ACCESS IT* 
<iframe style="border: 1px solid rgba(0, 0, 0, 0.1);" width="450" height="800" src="https://embed.figma.com/design/VDWArkLE2on5nO451k5aHN/Untitled?node-id=0-1&embed-host=share" allowfullscreen></iframe>

---

## Refined UI Prototype

Having established the layout of the UI screens, the prototype was refined visually, in terms of colour, fonts, etc.

This Figma demo shows the UI with refinements applied:

*FIGMA REFINED PROTOTYPE - PLACE THE FIGMA EMBED CODE HERE - MAKE SURE IT IS SET SO THAT EVERYONE CAN ACCESS IT*

### Testing

Replace this text with notes about what you did to test the UI flow and the outcome of the testing.

### Changes / Improvements

Replace this text with notes any improvements you made as a result of the testing.

*FIGMA IMPROVED REFINED PROTOTYPE - PLACE THE FIGMA EMBED CODE HERE - MAKE SURE IT IS SET SO THAT EVERYONE CAN ACCESS IT*


---

## Sprint Review

Replace this text with a statement about how the sprint has moved the project forward - key success point, any things that didn't go so well, etc.

