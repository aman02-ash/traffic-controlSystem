import React from 'react';

const SummaryPanel = ({ trafficState }) => {
  const { laneStates, activeGreenLane, timer } = trafficState || {
    laneStates: {},
    activeGreenLane: 'N/A',
    timer: 0,
  };

  const getHighestScoreLane = () => {
    if (!laneStates || Object.keys(laneStates).length === 0) return { name: 'N/A', score: 0 };
    let highestScore = -1;
    let highestLane = 'N/A';
    Object.entries(laneStates).forEach(([lane, data]) => {
      if (data.score > highestScore) {
        highestScore = data.score;
        highestLane = lane;
      }
    });
    return { name: highestLane.replace('_', ' ').toUpperCase(), score: highestScore };
  };

  const highest = getHighestScoreLane();

  return (
    <section className="summary-panel">
      <h2>Dashboard Summary</h2>
      <div className="summary-grid">
        <div className="summary-item">
          <span className="summary-label">Total Lanes:</span>
          <span className="summary-value">4</span>
        </div>
        <div className="summary-item">
          <span className="summary-label">Active Lane:</span>
          <span className="summary-value">{activeGreenLane ? activeGreenLane.replace('_', ' ').toUpperCase() : 'N/A'}</span>
        </div>
        <div className="summary-item">
          <span className="summary-label">Highest Score Lane:</span>
          <span className="summary-value">{highest.name}</span>
        </div>
        <div className="summary-item">
          <span className="summary-label">Highest Score Value:</span>
          <span className="summary-value">{highest.score}</span>
        </div>
        <div className="summary-item">
          <span className="summary-label">Current Timer:</span>
          <span className="summary-value">{timer}s</span>
        </div>
      </div>
    </section>
  );
};

export default SummaryPanel;
