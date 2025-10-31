# Project Review

## Addressing Relevant Implications

### End-User Requirements

My end user wanted an easy was to track and manage clients, meetings, and follow-ups. The final product allows my stakeholder to view all clients, add meetings, which are then add onto the follow-ups dashboard. Priority levels were added so that important clients or deadlines can be easily noted. After some feedback I simplified navigation so each page is focused on a singular means, not many (one thing at a time). 

### Usability Implications

Making sure the system was quick and simple to use, I tested every page while entering some (obscure) example data. These checks included clients, meetings, and follow-ups all saved correctly and all saved in the correct places. Pico overflow was tested to be sure that my lists didn't break the layout (by being too large). My end user stated that it is a clear layout and easy to navigate between pages. 

### Functionality Implications

The system fully supports the pages: a client list, a form to add said clients, a add/schedule meeting, and a follow-up display list. Each page has its own defined purpose, and links smoothly to the next with no seen issue. All the data is also correctly placed in the correct SQLite tables


### Aesthetic Implications

To keep the design clean and easy, I used picoCss and later switched the base color to dark for a better contrast. Headings, count totals, and pico cards were centered to make the design feel less stretched. My enduser agreed that the new centered look appears to be more "business like" wherein it doesn't waste unneeded resources (in this case space).

### Accessibility Implications

Font size, color contrast, and page layout were put through testing. Because my stakeholder sometimes struggles with working the dark getting flash-banged at 12am, I ensured that the color of the webpage would be less straining and would aid in longer working sessions. Buttons and page links are very simple to see. 
---

## Overall Review

Replace these words with a brief review of how the project went in terms of:
- What went well? The structure of the app came together cleanly once the database and routes actually managed to connect. Each page worked as intended; clients, meetings, and follow-ups all worked well. Testing with my end user confirmed everything was good and well to use.
- What didn't go so well? Ran into quite a many issues with how meetings and follow-ups linked themselves together. Some minor changes made the whole webpage break when I tried to add a new feature too quickly. I also struggled a bit with the layout between the pages, escpecially before using picoCss properly (i.e. I was using list's alone without any article tag; expecting a different result than a blab of text) 
- How did the testing/trialling impact the final system? Testing helped me spot small usability problems that weren't obvious to me while coding- for example; text not centered, and priority not showing up properly if not poorly. Each test made the system a little bit better and more reliable to say the least. Feedback from my end user on these changes were no worse than gleeful amazement.
- What would you do differently if you could? If I had more time/committed my time better, I'd have likely added options to edit and delete clients or meetings. I'd also plan my database and overall 'plan of attack' for earlier rather than having an epiphany half way through. Overall, though, the webpage turned out well enough and works as intended

