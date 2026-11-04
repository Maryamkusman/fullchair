## Road Map
Against the 10-step roadmap
Step	Status
1. Setup and first endpoint	✅ Done
2. Database models	✅ Done
3. API endpoints	Lesson given; confirm with pytest (8 passed)
4. Availability algorithm	Lesson given; confirm with pytest (15 passed)
5. AI agent (Claude tool use)	Not started
6. Chat interface	Not started
7. SMS (Twilio)	Not started
8. Background jobs (waitlist refill)	Not started
9. Dashboard (Next.js)	Not started
10. Ship it (Docker, CI, deploy)	Not started 
## What the App does 
autorespond to messages and use ai to fill add appointments and deal with cancellations and resheduling 

## Workflow

1. Open app -> 
2. login (connect text, instagram, google calander) 

Tabs: 
appointment -> pick salon, pick service, add client name and phone
configure -> add salons, add stylist, add services 
ai bot -> add csv or files for ai to organize it into your configure 
calander -> click to view upcoming schedule

3. Configure Tab 
    -> manual 
    -> AI configuration via upload 


4. Appointments
    1. "Cancel" 
            if text
                -> keyword "cancel" and ask appointment name
            manual 
                -> find appointment in calander 
                -> remove 
                -> message next client in line offering open spot if no then 

    2. "add" 
        -> check calander 
        -> respond with whats available 
        -> client response 
        -> go to "add appointment" and add the client name/number, service, salon


    -> resechedule
-> update via text/ instagram 

update google calander





