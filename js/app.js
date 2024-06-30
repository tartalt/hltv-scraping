document.addEventListener('DOMContentLoaded', () => {
  fetch('js/teams.json')
    .then(response => response.json())
    .then(teams => {
      const teamButtonsLeft = document.getElementById('team-buttons-left');
      const teamButtonsRight = document.getElementById('team-buttons-right');

      teams.forEach(team => {
        const teamButtonLeft = createTeamButton(team, selectTeam1);
        const teamButtonRight = createTeamButton(team, selectTeam2);

        teamButtonsLeft.appendChild(teamButtonLeft);
        teamButtonsRight.appendChild(teamButtonRight);
      });
    });

  let selectedTeams = [null, null];
  let selectedMaps = [];
  let maxMaps = 0;

  function createTeamButton(team, selectFunction) {
    const teamButton = document.createElement('div');
    teamButton.classList.add('team-button');
    teamButton.innerHTML = `<img src="${team.logo_url}" alt="${team.team_name}">`;
    teamButton.addEventListener('click', () => selectFunction(team));
    return teamButton;
  }

  function selectTeam1(team) {
    selectedTeams[0] = team;
    updateSelectedTeams();
  }

  function selectTeam2(team) {
    selectedTeams[1] = team;
    updateSelectedTeams();
  }

  function updateSelectedTeams() {
    if (selectedTeams[0]) {
      document.getElementById('team1').classList.add('selected');
      document.getElementById('team1-logo').src = selectedTeams[0].logo_url;
      document.getElementById('team1-name').textContent = selectedTeams[0].team_name;
      document.getElementById('team1-score').textContent = "Score HLTV :"+selectedTeams[0].hltv_score ;
      document.getElementById('team1-link').href = `https://www.hltv.org/team/${selectedTeams[0].team_id}/${selectedTeams[0].team_name.toLowerCase()}`;
    } else {
      document.getElementById('team1').classList.remove('selected');
      document.getElementById('team1-link').href = "#";
    }

    if (selectedTeams[1]) {
      document.getElementById('team2').classList.add('selected');
      document.getElementById('team2-logo').src = selectedTeams[1].logo_url;
      document.getElementById('team2-name').textContent = selectedTeams[1].team_name;
      document.getElementById('team2-score').textContent = "Score HLTV :"+selectedTeams[1].hltv_score ;
      document.getElementById('team2-link').href = `https://www.hltv.org/team/${selectedTeams[1].team_id}/${selectedTeams[1].team_name.toLowerCase()}`;
    } else {
      document.getElementById('team2').classList.remove('selected');
      document.getElementById('team2-link').href = "#";
    }

    if (selectedTeams[0] && selectedTeams[1]) {
      document.querySelector('.bo-buttons').style.display = 'flex';
    } else {
      document.querySelector('.bo-buttons').style.display = 'none';
    }
  }

  function updateMaps() {
    const mapsContainer = document.getElementById('maps-container');
    mapsContainer.innerHTML = '';

    const maps = Object.keys(selectedTeams[0].map_scores);
    maps.forEach(map => {
      const mapElement = document.createElement('div');
      mapElement.classList.add('map');
      mapElement.innerHTML = `<img src="img/${map.toLowerCase()}.png" alt="${map}">`;
      mapElement.addEventListener('click', () => selectMap(mapElement, map));
      mapsContainer.appendChild(mapElement);
    });
  }

  function selectMap(mapElement, map) {
    if (mapElement.classList.contains('selected')) {
      mapElement.classList.remove('selected');
      selectedMaps = selectedMaps.filter(selectedMap => selectedMap !== map);
    } else if (selectedMaps.length < maxMaps) {
      mapElement.classList.add('selected');
      selectedMaps.push(map);
    }

    if (selectedMaps.length === maxMaps) {
      disableRemainingMaps();
      calculateMatchOutcome();
    } else {
      enableAllMaps();
    }
  }

  function disableRemainingMaps() {
    document.querySelectorAll('.map').forEach(mapElement => {
      if (!mapElement.classList.contains('selected')) {
        mapElement.classList.add('disabled');
      }
    });
  }

  function enableAllMaps() {
    document.querySelectorAll('.map').forEach(mapElement => {
      mapElement.classList.remove('disabled');
    });
  }

  function calculateMatchOutcome() {
    let team1Wins = 0;
    let team2Wins = 0;
    let team1TotalScore = 0;
    let team2TotalScore = 0;

    selectedMaps.forEach(map => {
      const team1MapScore = selectedTeams[0].map_scores[map];
      const team2MapScore = selectedTeams[1].map_scores[map];

      // Calculate the adjusted scores to ensure they are closer to 50%
      const totalScore = team1MapScore + team2MapScore;
      const team1AdjustedScore = (team1MapScore / totalScore) * 100;
      const team2AdjustedScore = (team2MapScore / totalScore) * 100;

      if (team1MapScore > team2MapScore) {
        team1Wins++;
      } else {
        team2Wins++;
      }

      team1TotalScore += team1AdjustedScore;
      team2TotalScore += team2AdjustedScore;
    });

    displayMatchOutcome(team1Wins, team2Wins, team1TotalScore / selectedMaps.length, team2TotalScore / selectedMaps.length);
  }

  function displayMatchOutcome(team1Wins, team2Wins, team1AvgScore, team2AvgScore) {
    const team1Element = document.getElementById('team1');
    const team2Element = document.getElementById('team2');

    document.getElementById('team1-percentage').textContent = `Victoire: ${team1AvgScore.toFixed(2)}%`;
    document.getElementById('team2-percentage').textContent = `Victoire: ${team2AvgScore.toFixed(2)}%`;

    if (team1Wins > team2Wins) {
      team1Element.classList.add('winner');
      team1Element.classList.remove('loser');
      team2Element.classList.add('loser');
      team2Element.classList.remove('winner');
    } else {
      team2Element.classList.add('winner');
      team2Element.classList.remove('loser');
      team1Element.classList.add('loser');
      team1Element.classList.remove('winner');
    }

    const matchResult = team1Wins > team2Wins ? `${selectedTeams[0].team_name} remporte le match!` : `${selectedTeams[1].team_name} remporte le match!`;
    document.getElementById('match-result').textContent = matchResult;
  }

  document.getElementById('bo1').addEventListener('click', () => {
    maxMaps = 1;
    updateMaps();
  });

  document.getElementById('bo3').addEventListener('click', () => {
    maxMaps = 3;
    updateMaps();
  });

  document.getElementById('bo5').addEventListener('click', () => {
    maxMaps = 5;
    updateMaps();
  });
  function resetSelection() {
    selectedTeams = [null, null];
    selectedMaps = [];
    maxMaps = 0;

    document.getElementById('team1').classList.remove('selected', 'winner', 'loser');
    document.getElementById('team1-logo').src = '';
    document.getElementById('team1-name').textContent = 'Équipe 1';
    document.getElementById('team1-score').textContent = '0%';
    document.getElementById('team1-percentage').textContent = 'Victoire: 0%';
    document.getElementById('team1-link').href = '#';

    document.getElementById('team2').classList.remove('selected', 'winner', 'loser');
    document.getElementById('team2-logo').src = '';
    document.getElementById('team2-name').textContent = 'Équipe 2';
    document.getElementById('team2-score').textContent = '0%';
    document.getElementById('team2-percentage').textContent = 'Victoire: 0%';
    document.getElementById('team2-link').href = '#';

    document.querySelector('.bo-buttons.hidden').style.display = 'none';
    document.getElementById('match-result').textContent = '';


    const mapsContainer = document.getElementById('maps-container');
    mapsContainer.innerHTML = '';
    document.querySelectorAll('.map').forEach(mapElement => {
      mapElement.classList.remove('selected', 'disabled');
    });
  }

  document.getElementById('reset-button').addEventListener('click', resetSelection);
});
