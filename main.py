from drafter import (
    route,
    Page,
    Button,
    TextBox,
    Header,
    start_server
)
from dataclasses import dataclass
from bakery import assert_equal
import random

@dataclass
class Dive:
    name:str
    number:int
    position:str
    DD:float
    
    
@dataclass
class Diver:
    name:str
    year:str
    dive_list:list[Dive]
    score:float
    place:int

@dataclass
class State:
    entries: list[Diver]
    round_num: int
    diver_num: int
    event_scores: list[list[float]]
    
@route
def index(state: State):
    """loads home page"""
    return Page(
        state,
        [
            "Dive Meet Simulator",
            Button("Start Meet", start_meet)
        ]
    )


@route
def score_page(state: State):
    
    """loads a page where you imput scores"""

    current_diver = state.entries[state.diver_num]

    return Page(state, [
        f"Round {state.round_num + 1}",
        f"Diver: {current_diver.name}",
        f"Dive: {current_diver.dive_list[state.round_num].name}",

        TextBox("score1"),
        TextBox("score2"),
        TextBox("score3"),
        TextBox("score4"),
        TextBox("score5"),

        Button("Submit Scores", save_scores)
    ])



@route
def save_scores(state: State,
                score1: str,
                score2: str,
                score3: str,
                score4: str,
                score5: str):
    
    """After inputing socores, this will save them and check they are correct"""

    scores = [
        float(score1),
        float(score2),
        float(score3),
        float(score4),
        float(score5)
    ]

    for score in scores:
        if score < 0 or score > 10:
            return score_page(state)

    
    state.event_scores.append(scores)

    
    state.diver_num += 1

    
    if state.diver_num < len(state.entries):
        return score_page(state)

    
    run_round(
        state.entries,
        state.round_num,
        state.event_scores
    )

    
    state.round_num += 1
    state.diver_num = 0
    state.event_scores = []
    

    return leaderboard(state)
    

@route
def start_meet(state: State) -> Page:
    
    """from home page, this begins the meet by loading score_page"""
    
    state.round_num = 0
    state.diver_num = 0
    state.event_scores = []

    for diver in state.entries:
        diver.score = 0
        diver.place = 0

    return score_page(state)

@route
def leaderboard(state: State) -> Page:
    """Display the current competition standings."""
    content = [
        f"Results After Round {state.round_num}"
    ]

    for diver in state.entries:
        content.append(
            f"{diver.place}. {diver.name} — {round(diver.score, 1)}"
        )

    if state.round_num < 6:
        content.append(
            Button("Start Next Round", start_next_round)
        )
    else:
        content.append("Competition Complete!")
        content.append(
            Button("View Final Results", final_results)
        )

    return Page(state, content)

@route
def start_next_round(state: State) -> Page:
    
    """after a round is complete this will move on to the next score page"""
    
    state.diver_num = 0
    state.event_scores = []

    return score_page(state)

@route
def final_results(state: State) -> Page:
    """Display the final competition results."""
    content = [
        Header("Final Competition Results"),
        "Congratulations to all competitors!"
    ]

    for diver in state.entries:
        content.append(
            f"{diver.place}. {diver.name}: {round(diver.score, 1)}"
        )

    content.append(Button("Return Home", "index"))

    return Page(state, content)







""" these were for unit testing only
d105C = Dive("forward 2-1/2 somersault", 105, "tuck", 2.2)
d105B = Dive("forward 2-1/2 somersault", 105, "pike", 2.4)
d107C = Dive("forward 3-1/2 somersault", 107, "tuck", 2.8)
d109C = Dive("forward 4-1/2 somersault", 109, "tuck", 3.8)
d203B = Dive("back 1-1/2 somersault", 203, "pike", 2.2)
d205B = Dive("back 2-1/2 somersault", 205, "pike", 3.0)
d207C = Dive("back 3-1/2 somersault", 207, "tuck", 3.6)
d303B = Dive("reverse 1-1/2 somersault", 303, "pike", 2.3)   
d305B = Dive("reverse 2-1/2 somersault", 305, "pike", 3.0)
d307C = Dive("reverse 3-1/2 somersault", 307, "tuck", 3.5)
d405B = Dive("inward 2-1/2 somersault", 405, "pike", 3.0)
d407B = Dive("inward 3-1/2 somersault", 407, "pike", 3.7)
d5154B = Dive("forward 2 somersaults 2 twists", 5154, "pike", 3.4)
d5337D = Dive("reverse 1-1/2 somersaults 3-1/2 twists", 5337, "free", 3.5)
d5255D = Dive("back 1-1/2 somersaults 2-1/2 twists", 5255, "free", 3.6)
d5156B = Dive("forward 2 somersaults 3 twists", 5156, "pike", 3.8)

diver_1 = Diver("Jordan Rezepka", "senior",[d109C, d207C, d307C, d407B, d5156B, d5337D], 0,0)

diver_2 = Diver("Carson Tyler", "junior", [d107C, d205B, d305B, d405B, d5154B, d5337D],0,0)

diver_3 = Diver("Luke Forester","junior",[d105B, d207C, d303B, d407B, d5255D, d5156B],0,0)

diver_4 = Diver("Matteo santoro","freshman",[d109C, d205B, d307C, d405B, d5154B, d5255D],0,0)

diver_5 = Diver("Bennett Greene","sophmore",[d105C, d107C, d305B, d407B, d5337D, d5156B],0,0)

diver_6 = Diver("Moritz Wesemenn","senior",[d109C, d207C, d307C, d407B, d5337D, d5156B],0,0)

diver_7 = Diver("Josh Hedberg","sophmore",[d207C, d307C, d407B, d5154B, d5255D, d5337D],0,0)



bad_scores = [0.0, 0.5, 1.0, 1.5, 2.0]

mid_scores = [2.5, 3.0, 3.5, 4.0]

ok_scores = [4.5, 5.0, 5.5]

good_scores = [6.0, 6.5, 7.0, 7.5]

great_scores = [8.0, 8.5, 8.0,8.0,8.5]

amazing_scores = [9.5,9.5,9.5,9.0,9.0,9.0,9.5]

perfect_scores = [10.0,10.0,10.0,10.0,10.0]

"""



""" might not need? ask prof    
Directions == [
    1: "front",
    2: "back",
    3: "reverse",
    4: "inward"    
]

Positions == [
    A: "straight",
    B: "pike",
    C: "tuck",
    D: "free"
]

def dive_num_to_name(number:int, position:str)->str:
    direction = ""
    if number[0] == 5:
    """
    
def get_judges_score(scores:list[float])->float:
    
    """ this function is meant to get the middle three of the judges scores
Paramater: num_judges: int (this will be given by an input, and represents how many judges there are),
scores: list[float] (a list of judges scores from 0-10)

returns: float (this is the three middle scores added together)
"""
    sorted_scores = sorted(scores)
    first_score = (len(sorted_scores)-3)//2
    total_score = sum(sorted_scores[first_score:first_score + 3])
    return total_score


assert_equal(
    get_judges_score([4.0, 4.5, 4.5]), 13.0)

assert_equal(
    get_judges_score([4.0, 5.0, 4.5, 4.5, 4.0]), 13.0)

assert_equal(
    get_judges_score([4.0, 4.5, 4.5, 5.0, 5.0, 3.5, 4.5] ), 13.5)


    
    
def score_dive(dive:Dive, scores:list[float])->float:
    
    """This function scores a given dive by multiplying its DD by the sum
of its middle three scores

paramater: dive:Dive (the dive being scored), scores:list[float], num_judges:int
(both needed for finding the middle three score)

returns: the total score for that dive
"""

    judges_scores = get_judges_score(scores)
    return round(dive.DD * judges_scores, 2)

"""this unit test was not possible without global constants. it does work, but not when the
constants are in docstrings

assert_equal(
    score_dive(d107C, [4.0, 4.5, 4.5, 5, 5, 3.5, 4.5]), 37.8)
        
assert_equal(
    score_dive(d405B, [4.5, 5, 5, 5, 5.0]), 45.0)
    
assert_equal(
    score_dive(d5156B, [6.0, 5, 5.5, 5, 4.5]), 58.9)

"""



                                 
def run_round(entries:list[Diver], round_num:int,event_scores:list[list[float]])->list[Diver]:
    
    """ This function runs one round of diving and produces a list of divers from first place to last and assighnes a score
pramaters: entries:list[Diver] (all of the divers entered in the competition), round_num:int (this will be
updated after every round so all 6 round can be ran), event_scores:list[list[float]] (this is a list of a list of scores given
in the order of diving)

returns: returns a list of divers in the order of highes to lowest score
"""
    diver_scores = []

    
    for i in range(len(entries)):
        round_score = score_dive(
            entries[i].dive_list[round_num],
            event_scores[i])

        total_score = entries[i].score + round_score
        diver_scores.append([entries[i], total_score])

    
    for i in range(len(diver_scores)):
        highest_index = i

        for j in range(i + 1, len(diver_scores)):
            if diver_scores[j][1] > diver_scores[highest_index][1]:
                highest_index = j

        
        temporary = diver_scores[i]
        diver_scores[i] = diver_scores[highest_index]
        diver_scores[highest_index] = temporary

   
    sorted_entries = []

    for i in range(len(diver_scores)):
        diver = diver_scores[i][0]
        diver.score = diver_scores[i][1]
        diver.place = i + 1
        sorted_entries.append(diver)

    return sorted_entries

assert_equal(
    run_round(
        [diver_1, diver_2, diver_3],
        0,
        [
            perfect_scores,  
            good_scores,     
            ok_scores        
        ]
    ),
    [
        Diver("Jordan Rezepka", "senior",
              [d109C, d207C, d307C, d407B, d5156B, d5337D],
              114.0, 1),

        Diver("Carson Tyler", "junior",
              [d107C, d205B, d305B, d405B, d5154B, d5337D],
              54.60, 2),

        Diver("Luke Forester", "junior",
              [d105B, d207C, d303B, d407B, d5255D, d5156B],
              36.0, 3)
    ]
)
 
 

initial_state = State(
    [
        diver_1,
        diver_2,
        diver_3,
        diver_4,
        diver_5,
        diver_6,
        diver_7
    ],
    0,      
    0,      
    []      
)
 
 
start_server(initial_state)
