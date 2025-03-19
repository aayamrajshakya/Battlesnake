# Battlesnake
Battlesnake project for CSE 3683: AI Fundamentals

## How to run
1) Initiate 3 tmux terminal sessions
2) Run the custom snake script in the 1st session:
```bash
python main.py --port <unused port; port1>
```
3) Run the AI snake script in the 2nd session:
```bash
python main.py --port <unused port; port2>
```
4) Start the Battlesnake game in the 3rd session:
```bash
./battlesnake play -W 11 -H 11 --name "Jack Sparrow" --url http://127.0.0.1:<port1> --name "snake2" --url http://127.0.0.1:<port2> --browser
```