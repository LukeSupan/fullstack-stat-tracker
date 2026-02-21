# Stack Tracker
This is intended to be used socially; if you are hardcore about your specific stats, there are online trackers that do this better.
This specifically tracks:
- Stats for comps of you and your stack
- Stats for role specific comps of you and your stack
- Matchups between you and others in games where you play each other (Rocket League for example)
- Individual stats overall and role-based

---


## Match Entry Formatting:
Your first line should always be a tag. If you know how you can add these yourself, but the currently existing ones and their input are as follows:
- hero_shooter -> Tank/DPS/Support/Result
- hero_shooter_versus -> Tank/DPS/Support/Result|Tank/DPS/Support/Result

- lanes -> Side/Mid/Result
- lanes_detailed -> Left/Mid/Right/Result

- generic -> Players/Result
- generc_versus -> Player/Result|Player/Result

- moba -> Top/Jungle/Mid/ADC/Support/Result

>Games with _versus are for you vs other people you know. An example for generic_versus would be custom games in Rocket League.


### Example
These are examples of hero_shooter. You can add as many players as you want to each role using commas, but the number of roles is preset.
```
tank,tank2(mvp)/dps1,dps2/support1,support2/win

tank,tank2(key),tank3,tank4/dps1/support1(mvp)/loss
```

- **commas**(``,``) are separators for multiple players in a role.
- **slashes**(``/``) are separators for different roles.
- **(mvp) and (key)** are tags that can be applied to one player, stats for them will be shown if present.
- You must fill all slots with something BUT ->
- Use `none` to fill slots that would be empty (randoms).
- One game per line, then go to a newline, each line should end with either win or loss. Ignore draws, I can add them if requested, but I didn't see the point.

## Examples of a lanes input file
```
lanes
luke,aiden,jr(mvp)/alex(key)/loss
none/mar,kayla(key)/win
luke,mar/none/win
luke,mar/aiden,ray,kayla,dalton/win
```

## Running the tracker
To run the file, all you need is a formatted input filem you can use the lanes example above to test.
You will then need to change line 32 of tracker.py to fit your input file.
```
with open("games.txt") as f:
```

Simply drag your text file into the download folder and change games.txt to the name of your file, and it will work.
