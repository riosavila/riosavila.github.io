*** Basket Simulated Data
*** 1st Sesons 
clear
** Randomize # of teams
global rteams = runiformint(45,65)
global seasons = runiformint(5,8)
set obs $rteams
 gen team_id = _n
** te
** market size
tempvar rmsize 
gen `rmsize' = runiform()
gen str market_size = "Large" if inrange(`rmsize', 0,0.5)
replace market_size = "Medium" if inrange(`rmsize', 0.50,.8)
replace market_size = "Small" if inrange(`rmsize', 0.8,1)
** Conference
tempvar rconf
bysort team_id: gen `rconf'=runiform()

gen str conference = "Eastern" if `rconf' <.5
replace conference = "Western" if `rconf' >.5
 
expand $seasons

bysort team_id: gen season = _n-1 + 2005

save team.dta, replace

*** Players
clear
set obs $rteams
gen team_id = _n
gen team_skill = abs(rnormal())/4
 
gen nmplayers = 20+(rpoisson(2))
expand $seasons
bysort team_id:gen season =  _n-1 + 2005


expand nmplayers 
bysort team_id season:gen player_id = _n
gen player_age_0 = round(17 + rchi2(2))
gen player_age   = player_age_0 + round(rpoisson(3))
gen years_in_league = player_age-player_age_0

*** Possition 
tempvar rpos
gen `rpos' = runiform()
gen     position = "Guard"   if inrange(`rpos', 0,0.4)
replace position = "Forward" if inrange(`rpos',.4,0.8)
replace position = "Center"  if inrange(`rpos',.8,1.0)



 *** Next its to "drop" players
** Assume each season players may Stay or Leave
tempvar type_player 
gen type_player = runiform()<.5
** Type 1 enters  (they could leave)
** type 2 leavers (they )
bysort team_id season player_id: gen leave = runiform()<.02
bysort team_id season player_id: gen enter = runiform()<.8
bysort team_id player_id (season): replace leave=1 if  leave[_n-1]==1
bysort team_id player_id (season): replace enter=1 if  enter[_n-1]==1
bysort team_id player_id (season): replace position = position[1]
bysort team_id player_id : replace player_age=player_age[_n-1]+1 if  _n>1

drop if leave == 1 & type_player ==0
drop if enter == 0 & type_player ==1

drop leave enter type_player

bysort team_id season:gen tp = _N

// injury 
gen inj_t = cond(position == "Guard", 1.1, cond(position == "Forward", 1.2, 1.4))
qui:sum tp
** Total Players should reduce
gen tp2 = (tp-10)/25
gen injury = rbinomial(10, (.05 + (player_age-17)/23*.1)*inj_t - 0.05*(tp-10)/25)


*** Performance
 

// Define parameters for PPG
gen B_ppg = 10
gen alpha_ppg = 25
gen beta_ppg = 15
gen t_p_ppg = 27
gen sigma_t_ppg = 5
gen c_ppg = 3

// Position weights for PPG
gen h_ppg = cond(position == "Guard", 5, cond(position == "Forward", 3, 0))

// Calculate PPG
gen points_per_game = B_ppg + alpha_ppg * exp(-((player_age- t_p_ppg)^2) / (2 * sigma_t_ppg^2)) + beta_ppg * (years_in_league / (years_in_league + c_ppg)) + h_ppg

// Define parameters for APG
gen B_apg = 3
gen alpha_apg = 20
gen beta_apg = 10
gen t_p_apg = 26
gen sigma_t_apg = 4
gen c_apg = 2

// Position weights for APG
gen h_apg = cond(position == "Guard", 10, cond(position == "Forward", 2, -2))

// Calculate APG
gen assists_per_game = B_apg + alpha_apg * exp(-((player_age- t_p_apg)^2) / (2 * sigma_t_apg^2)) + beta_apg * (years_in_league / (years_in_league + c_apg)) + h_apg

// Define parameters for RPG
gen B_rpg = 5
gen alpha_rpg = 20
gen beta_rpg = 12
gen t_p_rpg = 28
gen sigma_t_rpg = 6
gen c_rpg = 3


// Position weights for RPG
gen h_rpg = cond(position == "Guard", -3, cond(position == "Forward", 5, 10))

// Calculate RPG
gen rebounds_per_game = B_rpg + alpha_rpg * exp(-((player_age- t_p_rpg)^2) / (2 * sigma_t_rpg^2)) + beta_rpg * (years_in_league / (years_in_league + c_rpg)) + h_rpg 

drop *rpg *apg *ppg

foreach i in  assists_per_game rebounds_per_game points_per_game {
    qui:sum `i'
    replace `i' = (`i'-r(mean))/r(sd)
}
gen skill = team_skill + abs(rnormal())/3
foreach i in  assists_per_game rebounds_per_game points_per_game {   
    replace `i' = sqrt(exp(`i') + skill)
    sum `i'
    replace `i' = (`i'-r(min))/(r(max)-r(min))
}

replace points_per_game = points_per_game*(1-.02*injury^1.2)
replace assists_per_game = assists_per_game*(1-.04*injury^1.2)
replace rebounds_per_game = rebounds_per_game*(1-.08*injury^1.2)

gen performance = 10+100*exp((log(points_per_game+1) + log(assists_per_game+1) + log(rebounds_per_game+1))/2)
 
replace points_per_game = points_per_game*27*1.2
replace assists_per_game = assists_per_game*10*1.2
replace rebounds_per_game = rebounds_per_game*12*1.2
 
foreach i in  assists_per_game rebounds_per_game points_per_game {   
    replace `i' = round(`i'*100)/100
}
 
** Player

gen player_salary  = 1000*exp( 2*points_per_game/27 + 0.5*assists_per_game/10 + 1.5*rebounds_per_game/12 + 0.5*years_in_league/10 +  team_skill + skill + performance / 60 + rnormal()*.1)
 
save player.dta , replace
*** Team

bysort team_id season:egen team_performance=mean(points_per_game)
bysort team_id season:egen team_budget=sum(player_salary)

** 
keep season team_id team_performance points_per_game team_budget
bysort season team_id: gen tp = _N
bysort season team_id: egen mean_per = mean(points_per_game)
bysort season team_id: egen sd_per  = var(points_per_game)
replace sd_per = sqrt(sd_per/tp)

bysort season team_id: gen flag = _n==1
keep if flag ==1

gen prf = rnormal()*sd_per+mean_per

gsort season  -prf
by season : gen playoff_appearance = _n<=16

replace team_budget = round(team_budget/1000000,.01)
merge 1:1 team_id season using team.dta

save team_finl, replace

use player.dta
merge m:1 team_id season using team_finl, gen(m)