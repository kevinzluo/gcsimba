# scope

the goal is to create build the following, in order of importance:
- a library that enables game damage simulation for a small number of characters
- a script that can read in a conf that runs the sim for that conf (maybe unnecessary)

# features
- create a variety of characters
- use their skills and abilities
- weapon effects and artifact

# character list
- ht, xq/yelan, xiangling, bennett, sucrose/kazuha (at least one vv user), zhongli, mona
- homa catch mist af ttds favs 

# artifact list
2p/4p
- cw, no, esf, shim, glad, 

# attributes that must be tracked

## character
- base atk, 
- weapon needs access to character base stats
- weapon needs atk%

## weapons
- fav weapons

# general mechanics
- EGT, energy mechanics
 
## test dummy



# I WILL NOT
- have specific framecounts

# damage calculation engine
## reaction processing, aura tracking


# imagined use
- 

# random notes
- how should character actions work?
I think characters should be given access to the game engine. their actions should then insert actions into the game queue. we will also have actions called user input actions. the way we will process the user input list is to always make sure there is at least one user action queued up within the game engine queue at all times. they will be placed at every timepoint in which the character can act, which is a game state property. so, for example, when a hutao with xq ult has a normal attack buffered, the way this works is as follows
[user_input_attack] -> [attack start (triggers can_act off), attack contact, attack_can_cancel (can_act still off, dash cancelable now on)] -> [xingqiu sword queued from attack start, attack contact, attack_can_cancel ] (game state now with can_act off)

how do I make sure the attack animation end gets deleted if I dash cancel or jump cancel?
- one way is to make it so that the game state knows the current active character action, essentially we'd just trigger the animation end early and play the dash/jump event instead
- I still think the animation end event should be emplaced by the can_cancel event (?)

- how should metaevent listeners work?
So xingqiu's ult needs to listen for the normal attack start metaevent. how can I make this available to the game state itself?
one option is to have metaevent broadcasters have a parent attribute. whenever the event listener receives an event, it further propagates it to its parent. 
how should it be structured?
essentially, each character action should trigger some assortment of events; an metaevent listener will contain a list of methods that are called whenever a certain event is triggered. (like a dict or something)
each method in the character def should then have a wrapper ?? that calls events?? no maybe not. instead each event in the queue should call metaevents when they are processed; I don't know if that's the right way to do it. like there are definitely some consequences of events (like character died or smth) that should call the event themselves (so when the character hp is zero, you'd call character.died or something, and this would broadcast some event)

what are some other events we will need to listen for, so we can better understand how they should behave?
- kazuha/sucrose/vv should have on-swirl event listeners. 
- somebody like guoba, which is an entity, needs to know when they hit the enemy so they can apply res shred. how will we implement this?
- fischl needs to listen for certain reactions being triggered also
so how should reactions be processed?
- for amp reactions, there should not be an additional thing placed into the queue
- but for transformative ones, there SHOULD be one; so therefore these are easy to listen for
- what if you wanted something to trigger on vape though, like some abyss effect?
- the aura engine, which handles ICDs, should have an event broadcaster too, whose parent is the broadcaster for the game engine; it should be able to call this event
- i guess the hangup is when the meta events should be broadcasted - should they be when a certain event is evaluated in the queue, or should it be called by the method call itself. 
- i think we should give ourselves the option for both, and just figure out a way that makes processing this clean. 
- so how should a given method trigger an event? 
- we could have a decorator that basically takes in the event handler for the class and events to trigger at the beginning/end
- what needs to get passed in when an event is triggered?
    - sometimes nothing (like for xingqiu)
    - sometimes the event owner and their stats (like for kaz/succ), as well as the reaction type? (like swirl events)
    - what about metaevents triggered by an event? how should they be broadcasted up? one way is to just directly broadcast them to the global event handler; 
    - what even is the point of having anything other than just the global event handler? why do we need ones per character?
        - what types of things would we want to place a listener on the character rather than just listening to the global state and then reading off the relevant character?
        - xiangling n5 bomb thing? 
        - tbh there really isn't a good reason to have it, but it's not like we lose much by having them, since the propagate up to the parent anyways. 

need to somehow also count the number of normals a character is currently in - should be part of the character state

what is the game engine supposed to do when it takes off the next event? is there really a difference between events and metaevents? 
- yes -- someone like furina who wants to listen to hp change metaevents -- hp change is not a true event in game, it's more like a consequence of an event
- but in the case of xq, we're literally creating like an attack start, attack contact, attack can be dash cancelled, attack end sequence of events -- and these are real events... so what's the line? i feel like events are like really about the game state, metaevents are more like about character metadata; but then if we're listening to an on attack start metaevent, this is triggered only by the on attack start event... the on attack start event needs to do other lifting, like disabling action
- ok so what are we doing with the next event in the queue?
- events probably also need their own types
- we have damage events, animation events, reaction events all of which need to be handled differently; buff expiry event
- so when I see a buff expiry event, what do I need to know? I need to know which buff I need to remove, and which characters to clear it from

ok something like fav or sac
- we should be listening to the character there, specifically listening to whether or not they crit
- but critting is processed by the game engine...
- or like mistsplitter, the buff gets placed based on whether or not you've done a skill (ok this is fine, the skill call should have )

wait what the fuck, when a character method gets called, it returns an event right? or I guess it can place events by itself
maybe the buff from homa should be an actual buff and not a stat modification on the weapon?
character actions add to the input queue, not the event queue

artifact sets are just buffs + bonus stat objects

# the general framework
minimum featureset:
- artifact sets: 4NO, 4CW, 4ESF
- characters: hutao, xingqiu
- weapons: homa, fav sword, mistsplitter
major engineering difficulties
- timed duration buffs
- xingqiu ult on-normal-start listener
- aura and internal cooldown
- energy

1. Game engine stores 2 things of importance: a user input queue and an Event priority queue; also tracks whether or not the user can currently act
2. if can act, consumes the next user input item
3. User input item then can queue up events (like if its an Attack input, then this queues up a normal-start, normal-contact, normal-is-cancellable, normal-end)
4. Meanwhile, the event priorityqueue is consumed - each event comes with a `modify_state` method. events can then further emit metaevents
5. Various buffs are able to listen to metaevents and act if a given metaevent is triggered -- here, xingqiu's ult listens for a normal-start metaevent
6. buff expiry will be dealt with by inserting a clear-buff event into the queue at the correct future duration.



